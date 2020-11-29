-- Table that uses in model training
CREATE TABLE temp_model
(
    state   int8[],
    follows int8,
    counter int8
);

-- Function for searching specific word (follow) for state in temporary table
CREATE FUNCTION follows_exist(model_state int8[], follow int8) RETURNS boolean
    LANGUAGE plpgsql
AS
$$
BEGIN
    IF (SELECT follows
        FROM temp_model
        WHERE state = model_state
          AND follows = follow
        LIMIT 1) IS NOT NULL THEN
        RETURN true;
    ELSE
        RETURN false;
    end if;
END
$$;

-- Update markov chain with new encoded sentence
CREATE OR REPLACE PROCEDURE update_chain(encoded_sentence int8[],
                                         state_size int4,
                                         begin_word int8,
                                         end_word int8)
    LANGUAGE plpgsql
AS
$$
DECLARE
    items     int8[];
    words     int8[];
    buf_state int8[];
    follow    int8;
BEGIN
    words := encoded_sentence;
    FOR t IN 1 .. state_size
        LOOP
            items := array_append(items, begin_word);
        END LOOP;
    FOR t IN 1 .. array_upper(words, 1)
        LOOP
            items := array_append(items, words[t]);
        END LOOP;
    items := array_append(items, end_word);

    FOR t IN 1 .. array_length(words, 1) + 1
        LOOP
            buf_state := array []::text[];
            FOR k IN t .. t + state_size - 1
                LOOP
                    buf_state := array_append(buf_state, items[k]);
                END LOOP;
            follow := items[t + state_size];

            IF follows_exist(buf_state, follow) THEN
                UPDATE temp_model
                SET counter = counter + 1
                WHERE state = buf_state
                  AND follows = follow;
            ELSE
                INSERT INTO temp_model(state, follows, counter)
                VALUES (buf_state, follow, 1);
            END IF;

        END LOOP;
END
$$;

-- Create markov chain table representation and usage functions
CREATE OR REPLACE PROCEDURE add_model(model_name text,
                                      end_word int8,
                                      hash_index boolean = true)
    LANGUAGE plpgsql
AS
$$
DECLARE
    cmd       text;
    table_row record;
BEGIN
    EXECUTE format('
            CREATE TABLE IF NOT EXISTS %s
            (
                state   int8[],
                choices int8[],
                cumdist int8[]
             )
            ', model_name);
    EXECUTE format('
            CREATE OR REPLACE FUNCTION chain_move_%s(chain_state int8[])
                RETURNS int8
                LANGUAGE plpgsql
            AS
            $move$
            DECLARE
                choices_arr int8[];
                cumdist_arr int4[];
                rand        float4;
            BEGIN
                SELECT choices, cumdist
                INTO choices_arr, cumdist_arr
                FROM %s
                WHERE array_eq(state, chain_state);
                rand := random() * cumdist_arr[array_upper(cumdist_arr, 1)];
                RETURN choices_arr[binary_search(cumdist_arr, rand)];
            END;
            $move$
            ', model_name, model_name);
    EXECUTE format('
            CREATE OR REPLACE FUNCTION chain_walk_%s(init_state int8[],
                                                     phrase_len int4)
                RETURNS int8[]
                LANGUAGE plpgsql
            AS
            $walk$
            DECLARE
                phrase   int8[];
                state    int8[];
                word     int8;
                end_word int8;
                i        int4;
            BEGIN
                end_word := %s;
                i := 0;
                state := init_state;
                word := chain_move_%s(state);
                WHILE word IS NOT NULL AND word <> end_word AND i < phrase_len
                    LOOP
                        phrase := array_append(phrase, word);
                        state := array_append(state[2:], word);
                        word := chain_move_%s(state);
                        i := i + 1;
                    END LOOP;
                RETURN phrase;
            END
            $walk$
            ', model_name, end_word, model_name, model_name);
    FOR table_row IN (SELECT state,
                             array_agg(follows) AS choices,
                             accumulate(array_agg(counter)) AS cumdist
                      FROM temp_model
                      GROUP BY state)
        LOOP
            IF table_row.cumdist IS NOT NULL THEN
                EXECUTE '
                    INSERT INTO chain_table(state, choices, cumdist)
                    VALUES ($1, $2, $3)'
                    USING table_row.state, table_row.choices, table_row.cumdist;
            END IF;
        END LOOP;

    -- Create model index
    cmd := 'CREATE %s INDEX IF NOT EXISTS pk_%s ON %s USING %s (state)';
    IF hash_index THEN
        cmd := format(cmd, '', model_name, model_name, 'hash');
    ELSE
        cmd := format(cmd, 'UNIQUE', model_name, model_name, 'btree');
    END IF;
    EXECUTE cmd;

    -- Clean up
    TRUNCATE TABLE temp_model;
END
$$;

-- Delete markov chain table representation
CREATE OR REPLACE PROCEDURE delete_model(model_name text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE 'DROP TABLE IF EXISTS ' || model_name;
    EXECUTE 'DROP FUNCTION IF EXISTS chain_move_' || model_name;
    EXECUTE 'DROP FUNCTION IF EXISTS chain_walk_' || model_name;
END
$$;
