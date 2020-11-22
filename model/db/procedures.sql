-- Create index for markov chain table representation
CREATE OR REPLACE PROCEDURE create_model_table_index(model_name text, hash_index boolean = true)
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

-- Drop index for markov chain table representation
CREATE OR REPLACE PROCEDURE drop_model_table_index(model_name text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE 'DROP IF EXISTS INDEX pk_' || model_name;
END
$$;

-- Create markov chain table representation
CREATE OR REPLACE PROCEDURE add_model(model_name text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE 'CREATE TABLE IF NOT EXIST ' || model_name ||
            '(
                state   int8[],
                choices int8[],
                cumdist int4[]
             )';
END
$$;
