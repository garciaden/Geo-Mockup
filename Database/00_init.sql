-- =====================================================
-- Database Initialization Script
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Create database, extensions, and schemas
-- Run First: Yes (00)
-- =====================================================

-- Create database (run as superuser if needed)
-- CREATE DATABASE culs_db;
-- \c culs_db

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";       -- Password hashing
CREATE EXTENSION IF NOT EXISTS "postgis";        -- Geographic data (for sample locations)

-- Create schemas for organization
CREATE SCHEMA IF NOT EXISTS culs;                -- Main application schema
CREATE SCHEMA IF NOT EXISTS audit;               -- Audit logging
CREATE SCHEMA IF NOT EXISTS files;               -- File management

-- Set default schema
SET search_path TO culs, public;

-- Create custom types/enums that will be used across tables
-- NOTE: user_status is now a lookup table (culs.user_status) instead of an ENUM
CREATE TYPE culs.visibility_level AS ENUM ('public', 'restricted', 'hidden');
CREATE TYPE culs.project_status AS ENUM ('active', 'archived');
CREATE TYPE culs.sample_status AS ENUM ('drafted', 'ingested', 'curated', 'retired');
CREATE TYPE culs.qc_status AS ENUM ('pending', 'pass', 'fail', 'partial');
CREATE TYPE culs.analysis_type AS ENUM ('physical', 'geochem', 'imaging');
CREATE TYPE culs.analysis_status AS ENUM ('pending', 'processing', 'complete', 'failed');
CREATE TYPE culs.instrument_status AS ENUM ('active', 'maintenance', 'retired');
CREATE TYPE culs.file_purpose_project AS ENUM ('doc', 'plan', 'export', 'misc');
CREATE TYPE culs.file_purpose_sample AS ENUM ('image', 'label', 'fieldnote', 'misc');
CREATE TYPE culs.file_purpose_analysis AS ENUM ('raw', 'processed', 'qc', 'report');
CREATE TYPE culs.audit_action AS ENUM ('insert', 'update', 'delete', 'export', 'transfer');
CREATE TYPE culs.export_format AS ENUM ('csv', 'xlsx', 'json', 'netcdf', 'zip');
CREATE TYPE culs.export_status AS ENUM ('pending', 'processing', 'done', 'failed');
CREATE TYPE culs.transfer_status AS ENUM ('pending', 'approved', 'rejected');

-- Grant schema usage
GRANT USAGE ON SCHEMA culs TO PUBLIC;
GRANT USAGE ON SCHEMA audit TO PUBLIC;
GRANT USAGE ON SCHEMA files TO PUBLIC;

COMMENT ON SCHEMA culs IS 'Main application schema for CULS';
COMMENT ON SCHEMA audit IS 'Audit logging and compliance tracking';
COMMENT ON SCHEMA files IS 'File asset management and references';
