-- =====================================================
-- Analysis Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Analytical workflow data (physical, geochem, imaging)
-- Dependencies: 01_people_and_access.sql, 05_samples.sql, 06_batches_and_instruments.sql
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- ANALYSIS: Parent analysis record (polymorphic)
-- =====================================================
CREATE TABLE culs.analysis (
    analysis_id             SERIAL PRIMARY KEY,
    sample_id               INTEGER NOT NULL REFERENCES culs.sample(sample_id) ON DELETE RESTRICT,
    analyst_user_id         INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE RESTRICT,
    instrument_id           INTEGER REFERENCES culs.instrument(instrument_id) ON DELETE SET NULL,
    batch_id                INTEGER REFERENCES culs.batch(batch_id) ON DELETE SET NULL,
    analysis_type           culs.analysis_type NOT NULL,
    parent_analysis_id      INTEGER REFERENCES culs.analysis(analysis_id) ON DELETE SET NULL,
    run_date                DATE NOT NULL DEFAULT CURRENT_DATE,
    status                  culs.analysis_status NOT NULL DEFAULT 'pending',
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT analysis_no_self_reference CHECK (
        parent_analysis_id IS NULL OR parent_analysis_id != analysis_id
    )
);

-- Indexes
CREATE INDEX idx_analysis_sample ON culs.analysis(sample_id);
CREATE INDEX idx_analysis_analyst ON culs.analysis(analyst_user_id);
CREATE INDEX idx_analysis_instrument ON culs.analysis(instrument_id);
CREATE INDEX idx_analysis_batch ON culs.analysis(batch_id);
CREATE INDEX idx_analysis_type ON culs.analysis(analysis_type);
CREATE INDEX idx_analysis_parent ON culs.analysis(parent_analysis_id);
CREATE INDEX idx_analysis_run_date ON culs.analysis(run_date DESC);
CREATE INDEX idx_analysis_status ON culs.analysis(status);

-- Comments
COMMENT ON TABLE culs.analysis IS 'Parent analysis record supporting physical, geochemical, and imaging analyses';
COMMENT ON COLUMN culs.analysis.analysis_type IS 'physical|geochem|imaging';
COMMENT ON COLUMN culs.analysis.status IS 'pending|processing|complete|failed';
COMMENT ON COLUMN culs.analysis.parent_analysis_id IS 'Self-reference for composite/derived analyses';


-- =====================================================
-- PHYSICAL_ANALYSIS: Physical analysis branch (1:1 with ANALYSIS)
-- =====================================================
CREATE TABLE culs.physical_analysis (
    analysis_id         INTEGER PRIMARY KEY REFERENCES culs.analysis(analysis_id) ON DELETE CASCADE,
    branch_code         VARCHAR(100) NOT NULL,

    -- Branch-specific normalized data would go in additional tables
    -- For now, this is a placeholder for the physical analysis type

    -- Constraints
    CONSTRAINT physical_branch_code_valid CHECK (
        branch_code IN (
            'macro_characteristics',
            'componentry',
            'particle_size_distribution',
            'max_clast_measurements',
            'density_measurements',
            'core_measurements',
            'cryptotephra'
        )
    )
);

-- Indexes
CREATE INDEX idx_physical_analysis_branch ON culs.physical_analysis(branch_code);

-- Comments
COMMENT ON TABLE culs.physical_analysis IS 'Physical analysis specialization (macro, componentry, particle size, etc.)';
COMMENT ON COLUMN culs.physical_analysis.branch_code IS 'Specific physical analysis workflow branch';


-- =====================================================
-- GEOCHEM_ANALYSIS: Geochemical analysis branch (1:1 with ANALYSIS)
-- =====================================================
CREATE TABLE culs.geochem_analysis (
    analysis_id         INTEGER PRIMARY KEY REFERENCES culs.analysis(analysis_id) ON DELETE CASCADE,
    method              VARCHAR(100) NOT NULL,

    -- Method-specific data would be normalized in additional tables

    -- Constraints
    CONSTRAINT geochem_method_valid CHECK (
        method IN (
            'ICP-MS',
            'XRF',
            'LA-ICP-MS',
            'EPMA',
            'SEM',
            'SIMS',
            'Micro-XRF',
            'Whole-XRF',
            'Solution-ICP-MS',
            'Geochronology'
        )
    )
);

-- Indexes
CREATE INDEX idx_geochem_analysis_method ON culs.geochem_analysis(method);

-- Comments
COMMENT ON TABLE culs.geochem_analysis IS 'Geochemical analysis specialization (ICP-MS, XRF, LA-ICP-MS, etc.)';
COMMENT ON COLUMN culs.geochem_analysis.method IS 'Analytical method used';


-- =====================================================
-- IMAGING_ANALYSIS: Imaging analysis branch (1:1 with ANALYSIS)
-- =====================================================
CREATE TABLE culs.imaging_analysis (
    analysis_id         INTEGER PRIMARY KEY REFERENCES culs.analysis(analysis_id) ON DELETE CASCADE,
    technique           VARCHAR(100) NOT NULL,

    -- Technique-specific data would be normalized in additional tables

    -- Constraints
    CONSTRAINT imaging_technique_valid CHECK (
        technique IN (
            'SEM',
            'MicroCT',
            'Optical',
            'BSE',
            'X-ray-Map',
            'Tomography',
            'Other'
        )
    )
);

-- Indexes
CREATE INDEX idx_imaging_analysis_technique ON culs.imaging_analysis(technique);

-- Comments
COMMENT ON TABLE culs.imaging_analysis IS 'Imaging analysis specialization (SEM, MicroCT, Optical, etc.)';
COMMENT ON COLUMN culs.imaging_analysis.technique IS 'Imaging technique used';


-- =====================================================
-- Trigger to ensure analysis type matches branch table
-- =====================================================
CREATE OR REPLACE FUNCTION culs.validate_analysis_branch()
RETURNS TRIGGER AS $$
DECLARE
    v_analysis_type culs.analysis_type;
BEGIN
    -- Get the analysis type
    SELECT analysis_type INTO v_analysis_type
    FROM culs.analysis
    WHERE analysis_id = NEW.analysis_id;

    -- Validate based on table name
    IF TG_TABLE_NAME = 'physical_analysis' AND v_analysis_type != 'physical' THEN
        RAISE EXCEPTION 'Analysis % must have type "physical" for PHYSICAL_ANALYSIS table', NEW.analysis_id;
    ELSIF TG_TABLE_NAME = 'geochem_analysis' AND v_analysis_type != 'geochem' THEN
        RAISE EXCEPTION 'Analysis % must have type "geochem" for GEOCHEM_ANALYSIS table', NEW.analysis_id;
    ELSIF TG_TABLE_NAME = 'imaging_analysis' AND v_analysis_type != 'imaging' THEN
        RAISE EXCEPTION 'Analysis % must have type "imaging" for IMAGING_ANALYSIS table', NEW.analysis_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_physical_analysis_type_check
    BEFORE INSERT OR UPDATE ON culs.physical_analysis
    FOR EACH ROW
    EXECUTE FUNCTION culs.validate_analysis_branch();

CREATE TRIGGER trg_geochem_analysis_type_check
    BEFORE INSERT OR UPDATE ON culs.geochem_analysis
    FOR EACH ROW
    EXECUTE FUNCTION culs.validate_analysis_branch();

CREATE TRIGGER trg_imaging_analysis_type_check
    BEFORE INSERT OR UPDATE ON culs.imaging_analysis
    FOR EACH ROW
    EXECUTE FUNCTION culs.validate_analysis_branch();
