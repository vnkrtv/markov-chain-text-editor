-- Create indexes encoder table
CREATE OR REPLACE PROCEDURE create_encoder_indexes(model_name text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE 'CREATE INDEX IF NOT EXISTS pk_code_' || model_name ||
                ' ON ' || model_name || '_encoder USING hash (code)';
    EXECUTE 'CREATE INDEX IF NOT EXISTS pk_word_' || model_name ||
                ' ON ' || model_name || '_encoder USING hash (word)';
END
$$;

-- Drop indexes for encoder table
CREATE OR REPLACE PROCEDURE drop_encoder_indexes(model_name text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE 'DROP IF EXISTS INDEX pk_code_' || model_name;
    EXECUTE 'DROP IF EXISTS INDEX pk_word_' || model_name;
END
$$;

-- Create encoder table and loading function
CREATE OR REPLACE PROCEDURE add_encoder(model_name text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE format('
            CREATE TABLE IF NOT EXISTS %s_encoder
            (
                code int8,
                word text
             )
            ', model_name);
END
$$;

-- Delete encoder table
CREATE OR REPLACE PROCEDURE delete_encoder(model_name text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE 'DROP TABLE IF EXISTS ' || model_name || '_encoder';
END
$$;

SELECT COUNT(*) FROM test_model;
