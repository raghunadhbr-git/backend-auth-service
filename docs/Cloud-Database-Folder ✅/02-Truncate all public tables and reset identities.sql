-- =========================================================
-- Truncate ALL tables in PUBLIC schema
-- Reset sequences automatically
-- Safe for non-superuser accounts
-- =========================================================

DO
$$
DECLARE
    tables TEXT;
BEGIN

    -- Collect all tables in public schema
    SELECT string_agg(format('%I.%I', schemaname, tablename), ', ')
    INTO tables
    FROM pg_tables
    WHERE schemaname = 'public';

    IF tables IS NULL THEN
        RAISE NOTICE 'No tables found in public schema.';
        RETURN;
    END IF;

    -- Truncate all tables and reset identity sequences
    EXECUTE format(
        'TRUNCATE TABLE %s RESTART IDENTITY CASCADE;',
        tables
    );

    RAISE NOTICE 'All tables truncated and identities reset successfully.';

END
$$;

-- CTRL + Enter

