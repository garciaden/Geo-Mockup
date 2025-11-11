-- =====================================================
-- File Asset Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Digital file management and associations
-- Dependencies: 01_people_and_access.sql, 02_projects_and_membership.sql, 05_samples.sql, 07_analysis.sql
-- =====================================================

SET search_path TO files, culs, public;

-- =====================================================
-- FILE_ASSET: Digital file records
-- =====================================================
CREATE TABLE files.file_asset (
    file_id                 SERIAL PRIMARY KEY,
    uri                     TEXT NOT NULL,  -- s3://bucket/key or /nas/path/to/file
    filename                VARCHAR(255) NOT NULL,
    mime_type               VARCHAR(100),
    byte_size               BIGINT,
    checksum_sha256         CHAR(64),  -- SHA256 hash (64 hex chars)
    uploaded_by_user_id     INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE RESTRICT,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT file_uri_not_empty CHECK (
        length(trim(uri)) > 0
    ),
    CONSTRAINT file_byte_size_positive CHECK (
        byte_size IS NULL OR byte_size >= 0
    ),
    CONSTRAINT file_checksum_format CHECK (
        checksum_sha256 IS NULL OR checksum_sha256 ~ '^[a-f0-9]{64}$'
    )
);

-- Indexes
CREATE INDEX idx_file_uploaded_by ON files.file_asset(uploaded_by_user_id);
CREATE INDEX idx_file_created_at ON files.file_asset(created_at DESC);
CREATE INDEX idx_file_mime_type ON files.file_asset(mime_type);
CREATE INDEX idx_file_checksum ON files.file_asset(checksum_sha256) WHERE checksum_sha256 IS NOT NULL;
CREATE INDEX idx_file_filename ON files.file_asset USING gin(to_tsvector('english', filename));

-- Comments
COMMENT ON TABLE files.file_asset IS 'Digital file asset records with storage URIs';
COMMENT ON COLUMN files.file_asset.uri IS 'Storage URI (s3://... or file system path)';
COMMENT ON COLUMN files.file_asset.checksum_sha256 IS 'SHA256 hash for integrity verification';


-- =====================================================
-- PROJECT_FILE: Project file associations
-- =====================================================
CREATE TABLE files.project_file (
    project_id          INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE CASCADE,
    file_id             INTEGER NOT NULL REFERENCES files.file_asset(file_id) ON DELETE CASCADE,
    purpose             culs.file_purpose_project NOT NULL DEFAULT 'misc',

    -- Constraints
    PRIMARY KEY (project_id, file_id)
);

-- Indexes
CREATE INDEX idx_project_file_file_id ON files.project_file(file_id);
CREATE INDEX idx_project_file_purpose ON files.project_file(purpose);

-- Comments
COMMENT ON TABLE files.project_file IS 'Files associated with projects';
COMMENT ON COLUMN files.project_file.purpose IS 'doc|plan|export|misc';


-- =====================================================
-- SAMPLE_FILE: Sample file associations
-- =====================================================
CREATE TABLE files.sample_file (
    sample_id           INTEGER NOT NULL REFERENCES culs.sample(sample_id) ON DELETE CASCADE,
    file_id             INTEGER NOT NULL REFERENCES files.file_asset(file_id) ON DELETE CASCADE,
    purpose             culs.file_purpose_sample NOT NULL DEFAULT 'misc',

    -- Constraints
    PRIMARY KEY (sample_id, file_id)
);

-- Indexes
CREATE INDEX idx_sample_file_file_id ON files.sample_file(file_id);
CREATE INDEX idx_sample_file_purpose ON files.sample_file(purpose);

-- Comments
COMMENT ON TABLE files.sample_file IS 'Files associated with samples';
COMMENT ON COLUMN files.sample_file.purpose IS 'image|label|fieldnote|misc';


-- =====================================================
-- ANALYSIS_FILE: Analysis file associations
-- =====================================================
CREATE TABLE files.analysis_file (
    analysis_id         INTEGER NOT NULL REFERENCES culs.analysis(analysis_id) ON DELETE CASCADE,
    file_id             INTEGER NOT NULL REFERENCES files.file_asset(file_id) ON DELETE CASCADE,
    purpose             culs.file_purpose_analysis NOT NULL DEFAULT 'misc',

    -- Constraints
    PRIMARY KEY (analysis_id, file_id)
);

-- Indexes
CREATE INDEX idx_analysis_file_file_id ON files.analysis_file(file_id);
CREATE INDEX idx_analysis_file_purpose ON files.analysis_file(purpose);

-- Comments
COMMENT ON TABLE files.analysis_file IS 'Files associated with analyses';
COMMENT ON COLUMN files.analysis_file.purpose IS 'raw|processed|qc|report';


-- =====================================================
-- Add foreign key to INSTRUMENT_CALIBRATION
-- =====================================================
ALTER TABLE culs.instrument_calibration
    ADD CONSTRAINT fk_calibration_file
    FOREIGN KEY (file_id)
    REFERENCES files.file_asset(file_id)
    ON DELETE SET NULL;

CREATE INDEX idx_calibration_file ON culs.instrument_calibration(file_id);

COMMENT ON COLUMN culs.instrument_calibration.file_id IS 'Calibration report file reference';
