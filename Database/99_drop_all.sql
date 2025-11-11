-- =====================================================
-- Drop All Database Objects
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Clean up all database objects for fresh start
-- Usage: psql -U postgres -d culs_db -f 99_drop_all.sql
-- WARNING: This will DELETE ALL DATA!
-- =====================================================

\echo '================================================='
\echo 'CULS Database Cleanup - DROP ALL OBJECTS'
\echo '================================================='
\echo ''
\echo 'WARNING: This will permanently delete all data!'
\echo 'Press Ctrl+C to cancel, or press Enter to continue...'
\prompt 'Type YES to confirm: ' confirm

-- Check confirmation
\if :{?confirm}
    \if :confirm = 'YES'
        \echo 'Proceeding with cleanup...'
    \else
        \echo 'Confirmation failed. Aborting.'
        \quit
    \endif
\else
    \echo 'Confirmation required. Aborting.'
    \quit
\endif

\echo ''

-- Set error handling
\set ON_ERROR_STOP on

-- =====================================================
-- Drop all tables in reverse dependency order
-- =====================================================
\echo '>>> Dropping audit and request tables...'
DROP TABLE IF EXISTS audit.audit_log CASCADE;
DROP TABLE IF EXISTS culs.export_request CASCADE;
DROP TABLE IF EXISTS culs.project_transfer CASCADE;
\echo '✓ Audit and request tables dropped'

\echo '>>> Dropping file tables...'
DROP TABLE IF EXISTS files.analysis_file CASCADE;
DROP TABLE IF EXISTS files.sample_file CASCADE;
DROP TABLE IF EXISTS files.project_file CASCADE;
DROP TABLE IF EXISTS files.file_asset CASCADE;
\echo '✓ File tables dropped'

\echo '>>> Dropping analysis tables...'
DROP TABLE IF EXISTS culs.imaging_analysis CASCADE;
DROP TABLE IF EXISTS culs.geochem_analysis CASCADE;
DROP TABLE IF EXISTS culs.physical_analysis CASCADE;
DROP TABLE IF EXISTS culs.analysis CASCADE;
\echo '✓ Analysis tables dropped'

\echo '>>> Dropping batch and instrument tables...'
DROP TABLE IF EXISTS culs.instrument_calibration CASCADE;
DROP TABLE IF EXISTS culs.instrument CASCADE;
DROP TABLE IF EXISTS culs.batch CASCADE;
\echo '✓ Batch and instrument tables dropped'

\echo '>>> Dropping sample tables...'
DROP TABLE IF EXISTS culs.sample CASCADE;
\echo '✓ Sample tables dropped'

\echo '>>> Dropping storage tables...'
DROP TABLE IF EXISTS culs.storage_location CASCADE;
\echo '✓ Storage tables dropped'

\echo '>>> Dropping funding tables...'
DROP TABLE IF EXISTS culs.project_fund CASCADE;
DROP TABLE IF EXISTS culs.fund CASCADE;
\echo '✓ Funding tables dropped'

\echo '>>> Dropping project tables...'
DROP TABLE IF EXISTS culs.project_user CASCADE;
DROP TABLE IF EXISTS culs.project CASCADE;
\echo '✓ Project tables dropped'

\echo '>>> Dropping people and access tables...'
DROP TABLE IF EXISTS culs.user CASCADE;
DROP TABLE IF EXISTS culs.system_role CASCADE;
DROP TABLE IF EXISTS culs.person CASCADE;
\echo '✓ People and access tables dropped'

-- =====================================================
-- Drop functions
-- =====================================================
\echo '>>> Dropping functions...'
DROP FUNCTION IF EXISTS culs.get_storage_path(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS culs.update_sample_geom() CASCADE;
DROP FUNCTION IF EXISTS culs.validate_analysis_branch() CASCADE;
DROP FUNCTION IF EXISTS audit.protect_audit_log() CASCADE;
DROP FUNCTION IF EXISTS audit.log_change() CASCADE;
\echo '✓ Functions dropped'

-- =====================================================
-- Drop custom types
-- =====================================================
\echo '>>> Dropping custom types...'
DROP TYPE IF EXISTS culs.user_status CASCADE;
DROP TYPE IF EXISTS culs.visibility_level CASCADE;
DROP TYPE IF EXISTS culs.project_status CASCADE;
DROP TYPE IF EXISTS culs.sample_status CASCADE;
DROP TYPE IF EXISTS culs.qc_status CASCADE;
DROP TYPE IF EXISTS culs.analysis_type CASCADE;
DROP TYPE IF EXISTS culs.analysis_status CASCADE;
DROP TYPE IF EXISTS culs.instrument_status CASCADE;
DROP TYPE IF EXISTS culs.file_purpose_project CASCADE;
DROP TYPE IF EXISTS culs.file_purpose_sample CASCADE;
DROP TYPE IF EXISTS culs.file_purpose_analysis CASCADE;
DROP TYPE IF EXISTS culs.audit_action CASCADE;
DROP TYPE IF EXISTS culs.export_format CASCADE;
DROP TYPE IF EXISTS culs.export_status CASCADE;
DROP TYPE IF EXISTS culs.transfer_status CASCADE;
\echo '✓ Custom types dropped'

-- =====================================================
-- Drop schemas
-- =====================================================
\echo '>>> Dropping schemas...'
DROP SCHEMA IF EXISTS audit CASCADE;
DROP SCHEMA IF EXISTS files CASCADE;
DROP SCHEMA IF EXISTS culs CASCADE;
\echo '✓ Schemas dropped'

-- =====================================================
-- Drop extensions (optional - comment out if shared)
-- =====================================================
-- \echo '>>> Dropping extensions...'
-- DROP EXTENSION IF EXISTS postgis CASCADE;
-- DROP EXTENSION IF EXISTS pgcrypto CASCADE;
-- DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
-- \echo '✓ Extensions dropped'

-- =====================================================
-- Summary
-- =====================================================
\echo ''
\echo '================================================='
\echo 'Database Cleanup Complete!'
\echo '================================================='
\echo ''
\echo 'All CULS database objects have been removed.'
\echo 'You can now run 99_run_all.sql to recreate the database.'
\echo ''
