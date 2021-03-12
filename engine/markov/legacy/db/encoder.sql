-- Table for model encoder fitting
CREATE TABLE temp_encoder
(
    code int8,
    word text
);

-- CREATE OR REPLACE PROCEDURE update_encoder(encoded_sentence int8[])

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
    EXECUTE 'CREATE INDEX IF NOT EXISTS pk_code_' || model_name ||
                ' ON ' || model_name || '_encoder USING hash (code)';
    EXECUTE 'CREATE INDEX IF NOT EXISTS pk_word_' || model_name ||
                ' ON ' || model_name || '_encoder USING hash (word)';
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
