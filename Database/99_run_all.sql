-- =====================================================
-- Master Execution Script
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Run all DDL scripts in correct order
-- Usage: psql -U postgres -d culs_db -f 99_run_all.sql
-- =====================================================

\echo '================================================='
\echo 'CULS Database Setup - Master Script'
\echo '================================================='
\echo ''

-- Set error handling
\set ON_ERROR_STOP on

-- Display execution info
\echo 'Database:' :DBNAME
\echo 'User:' :USER
\echo 'Started:' `date`
\echo ''

-- =====================================================
-- Step 0: Database Initialization
-- =====================================================
\echo '>>> Step 0: Initializing database and extensions...'
\i 00_init.sql
\echo '✓ Database initialized'
\echo ''

-- =====================================================
-- Step 1: People and Access Control
-- =====================================================
\echo '>>> Step 1: Creating people and access control tables...'
\i 01_people_and_access.sql
\echo '✓ People and access tables created'
\echo ''

-- =====================================================
-- Step 2: Projects and Membership
-- =====================================================
\echo '>>> Step 2: Creating project and membership tables...'
\i 02_projects_and_membership.sql
\echo '✓ Project tables created'
\echo ''

-- =====================================================
-- Step 3: Funding
-- =====================================================
\echo '>>> Step 3: Creating funding tables...'
\i 03_funding.sql
\echo '✓ Funding tables created'
\echo ''

-- =====================================================
-- Step 4: Physical Storage
-- =====================================================
\echo '>>> Step 4: Creating storage location tables...'
\i 04_storage.sql
\echo '✓ Storage tables created'
\echo ''

-- =====================================================
-- Step 5: Samples
-- =====================================================
\echo '>>> Step 5: Creating sample tables...'
\i 05_samples.sql
\echo '✓ Sample tables created'
\echo ''

-- =====================================================
-- Step 6: Batches and Instruments
-- =====================================================
\echo '>>> Step 6: Creating batch and instrument tables...'
\i 06_batches_and_instruments.sql
\echo '✓ Batch and instrument tables created'
\echo ''

-- =====================================================
-- Step 7: Analysis
-- =====================================================
\echo '>>> Step 7: Creating analysis tables...'
\i 07_analysis.sql
\echo '✓ Analysis tables created'
\echo ''

-- =====================================================
-- Step 8: Files
-- =====================================================
\echo '>>> Step 8: Creating file asset tables...'
\i 08_files.sql
\echo '✓ File tables created'
\echo ''

-- =====================================================
-- Step 9: Audit and Requests
-- =====================================================
\echo '>>> Step 9: Creating audit and request tables...'
\i 09_audit_and_requests.sql
\echo '✓ Audit and request tables created'
\echo ''

-- =====================================================
-- Summary
-- =====================================================
\echo '================================================='
\echo 'Database Setup Complete!'
\echo '================================================='
\echo ''
\echo 'Summary:'

-- Count tables per schema
SELECT
    schemaname,
    COUNT(*) as table_count
FROM pg_tables
WHERE schemaname IN ('culs', 'audit', 'files')
GROUP BY schemaname
ORDER BY schemaname;

\echo ''
\echo 'All tables created successfully!'
\echo 'Completed:' `date`
\echo ''
