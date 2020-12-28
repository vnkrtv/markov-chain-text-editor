-- Create model table index
CREATE OR REPLACE PROCEDURE create_model_table_index(model_name text, hash_index boolean)
LANGUAGE plpgsql
AS
    $$
    DECLARE
        cmd text;
    BEGIN
        cmd := 'CREATE %s INDEX IF NOT EXISTS pk_%s ON %s USING %s (state)';
        IF hash_index THEN
            cmd := format(cmd, '', model_name, model_name, 'hash');
        ELSE
            cmd := format(cmd, 'UNIQUE', model_name, model_name, 'btree');
        END IF;
        EXECUTE cmd;
    END
    $$;

-- Create markov chain table representation and usage functions
CREATE OR REPLACE PROCEDURE add_model(model_name text,
                                      end_word int8)
    LANGUAGE plpgsql
AS
$$
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
