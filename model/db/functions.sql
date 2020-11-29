-- Help function for getting occurrences of words - accumulate array: [4, 5, 1] => [4, 9, 10]
CREATE OR REPLACE FUNCTION accumulate(arr int8[])
    RETURNS int8[]
    LANGUAGE plpgsql
AS
$$
DECLARE
    total_count int8;
    buf_arr     int8[];
BEGIN
    total_count := 0;
    FOR i IN 1 .. array_upper(arr, 1)
        LOOP
            total_count = total_count + arr[i];
            buf_arr := array_append(buf_arr, total_count);
        END LOOP;
    RETURN buf_arr;
END
$$;

-- Help function - binary search algorithm for weighted word selection for the continuation of a phrase
CREATE OR REPLACE FUNCTION binary_search(arr int8[], elem float)
    RETURNS integer
    LANGUAGE plpgsql
AS
$$
DECLARE
    idx         int4;
    left_index  int4;
    right_index int4;
BEGIN
    left_index := 0;
    right_index := array_length(arr, 1) + 1;
    WHILE left_index < right_index - 1
        LOOP
            idx := (left_index + right_index) / 2;
            IF arr[idx] < elem THEN
                left_index := idx;
            ELSE
                right_index := idx;
            END IF;
        END LOOP;
    RETURN right_index;
END
$$;

-- Help function for getting occurrences of words - accumulate array: [4, 5, 1] => [4, 9, 10]
CREATE OR REPLACE FUNCTION accumulate(arr int8[]) RETURNS int8[]
    LANGUAGE plpgsql
AS
$$
DECLARE
    total_count integer;
    buf_arr     integer[];
BEGIN
    total_count := 0;
    FOR i IN 1 .. array_upper(arr, 1)
        LOOP
            total_count = total_count + arr[i];
            buf_arr := array_append(buf_arr, total_count);
        END LOOP;
    RETURN buf_arr;
END
$$;

