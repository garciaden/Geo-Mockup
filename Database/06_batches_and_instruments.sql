-- =====================================================
-- Batches and Instruments Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Analytical batch and instrument management
-- Dependencies: 01_people_and_access.sql, 02_projects_and_membership.sql
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- MATERIAL_TYPE: Lookup table for reference material types
-- =====================================================
CREATE TABLE culs.material_type (
    material_type_id    SERIAL PRIMARY KEY,
    type_code           VARCHAR(20) NOT NULL UNIQUE,
    type_name           VARCHAR(100) NOT NULL,
    description         TEXT,

    -- Constraints
    CONSTRAINT material_type_code_valid CHECK (
        type_code IN ('standard', 'blank', 'control', 'spike', 'duplicate', 'matrix', 'other')
    )
);

-- Comments
COMMENT ON TABLE culs.material_type IS 'Lookup table for reference material types';

-- Insert default material types
INSERT INTO culs.material_type (type_code, type_name, description) VALUES
    ('standard', 'Standard', 'Certified reference standard'),
    ('blank', 'Blank', 'Procedural or method blank'),
    ('control', 'Control', 'Quality control material'),
    ('spike', 'Spike', 'Spiked sample for recovery testing'),
    ('duplicate', 'Duplicate', 'Duplicate sample for precision testing'),
    ('matrix', 'Matrix', 'Matrix reference material'),
    ('other', 'Other', 'Other reference material type');


-- =====================================================
-- MATERIAL_SOURCE: Lookup table for reference material sources
-- =====================================================
CREATE TABLE culs.material_source (
    material_source_id  SERIAL PRIMARY KEY,
    source_code         VARCHAR(50) NOT NULL UNIQUE,
    source_name         VARCHAR(255) NOT NULL,
    abbreviation        VARCHAR(50),
    website             VARCHAR(255),
    description         TEXT,

    -- Constraints
    CONSTRAINT material_source_website_format CHECK (
        website IS NULL OR website ~ '^https?://.*'
    )
);

-- Comments
COMMENT ON TABLE culs.material_source IS 'Lookup table for reference material suppliers/sources';
COMMENT ON COLUMN culs.material_source.source_code IS 'Unique source identifier (e.g., NIST, USGS, etc.)';

-- Insert common reference material sources
INSERT INTO culs.material_source (source_code, source_name, abbreviation, website) VALUES
    ('NIST', 'National Institute of Standards and Technology', 'NIST', 'https://www.nist.gov/'),
    ('USGS', 'United States Geological Survey', 'USGS', 'https://www.usgs.gov/'),
    ('NRC', 'National Research Council Canada', 'NRC', 'https://nrc.canada.ca/'),
    ('IAEA', 'International Atomic Energy Agency', 'IAEA', 'https://www.iaea.org/'),
    ('INTERNAL', 'Internal Laboratory Standard', 'Internal', NULL),
    ('OTHER', 'Other Source', 'Other', NULL);


-- =====================================================
-- ANALYTE: Lookup table for chemical analytes
-- =====================================================
CREATE TABLE culs.analyte (
    analyte_id          SERIAL PRIMARY KEY,
    analyte_code        VARCHAR(20) NOT NULL UNIQUE,
    analyte_name        VARCHAR(100) NOT NULL,
    chemical_formula    VARCHAR(50),
    cas_number          VARCHAR(20),  -- Chemical Abstracts Service number
    description         TEXT,

    -- Constraints
    CONSTRAINT analyte_cas_format CHECK (
        cas_number IS NULL OR cas_number ~ '^\d{1,7}-\d{2}-\d{1}$'
    )
);

-- Comments
COMMENT ON TABLE culs.analyte IS 'Lookup table for chemical analytes and elements';
COMMENT ON COLUMN culs.analyte.analyte_code IS 'Short code for analyte (e.g., SiO2, Al2O3, Fe, etc.)';
COMMENT ON COLUMN culs.analyte.cas_number IS 'CAS Registry Number (format: NNNNNNN-NN-N)';

-- Insert common analytes (expand as needed)
INSERT INTO culs.analyte (analyte_code, analyte_name, chemical_formula, cas_number) VALUES
    ('SiO2', 'Silicon Dioxide', 'SiO2', '7631-86-9'),
    ('Al2O3', 'Aluminum Oxide', 'Al2O3', '1344-28-1'),
    ('Fe2O3', 'Iron(III) Oxide', 'Fe2O3', '1309-37-1'),
    ('FeO', 'Iron(II) Oxide', 'FeO', '1345-25-1'),
    ('MgO', 'Magnesium Oxide', 'MgO', '1309-48-4'),
    ('CaO', 'Calcium Oxide', 'CaO', '1305-78-8'),
    ('Na2O', 'Sodium Oxide', 'Na2O', '1313-59-3'),
    ('K2O', 'Potassium Oxide', 'K2O', '12136-45-7'),
    ('TiO2', 'Titanium Dioxide', 'TiO2', '13463-67-7'),
    ('P2O5', 'Phosphorus Pentoxide', 'P2O5', '1314-56-3');


-- =====================================================
-- UNIT: Lookup table for measurement units
-- =====================================================
CREATE TABLE culs.unit (
    unit_id             SERIAL PRIMARY KEY,
    unit_code           VARCHAR(20) NOT NULL UNIQUE,
    unit_name           VARCHAR(100) NOT NULL,
    unit_type           VARCHAR(50) NOT NULL,  -- concentration, mass, volume, temperature, etc.
    description         TEXT,

    -- Constraints
    CONSTRAINT unit_type_valid CHECK (
        unit_type IN ('concentration', 'mass', 'volume', 'length', 'temperature', 'pressure', 'percentage', 'ratio', 'other')
    )
);

-- Comments
COMMENT ON TABLE culs.unit IS 'Lookup table for measurement units';
COMMENT ON COLUMN culs.unit.unit_type IS 'Type category for the unit';

-- Insert common units
INSERT INTO culs.unit (unit_code, unit_name, unit_type) VALUES
    ('ppm', 'Parts Per Million', 'concentration'),
    ('ppb', 'Parts Per Billion', 'concentration'),
    ('wt%', 'Weight Percent', 'percentage'),
    ('mg/L', 'Milligrams per Liter', 'concentration'),
    ('ug/L', 'Micrograms per Liter', 'concentration'),
    ('g', 'Grams', 'mass'),
    ('mg', 'Milligrams', 'mass'),
    ('mL', 'Milliliters', 'volume'),
    ('L', 'Liters', 'volume'),
    ('mm', 'Millimeters', 'length'),
    ('cm', 'Centimeters', 'length'),
    ('degC', 'Degrees Celsius', 'temperature'),
    ('ratio', 'Ratio', 'ratio');


-- =====================================================
-- BATCH: Analytical batch grouping
-- =====================================================
CREATE TABLE culs.batch (
    batch_id            SERIAL PRIMARY KEY,
    project_id          INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE RESTRICT,
    batch_code          VARCHAR(100) NOT NULL,
    started_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at        TIMESTAMP,
    qc_status           culs.qc_status NOT NULL DEFAULT 'pending',
    notes               TEXT,

    -- Constraints
    CONSTRAINT batch_code_unique_per_project UNIQUE (project_id, batch_code),
    CONSTRAINT batch_completion_after_start CHECK (
        completed_at IS NULL OR completed_at >= started_at
    )
);

-- Indexes
CREATE INDEX idx_batch_project ON culs.batch(project_id);
CREATE INDEX idx_batch_qc_status ON culs.batch(qc_status);
CREATE INDEX idx_batch_started_at ON culs.batch(started_at DESC);
CREATE INDEX idx_batch_code ON culs.batch(batch_code);

-- Comments
COMMENT ON TABLE culs.batch IS 'Analytical batch grouping for QC and workflow management';
COMMENT ON COLUMN culs.batch.batch_code IS 'Unique batch identifier within project';
COMMENT ON COLUMN culs.batch.qc_status IS 'pending|pass|fail|partial';


-- =====================================================
-- INSTRUMENT: Laboratory instruments
-- =====================================================
CREATE TABLE culs.instrument (
    instrument_id       SERIAL PRIMARY KEY,
    name                VARCHAR(255) NOT NULL,
    model               VARCHAR(255),
    serial_no           VARCHAR(100) UNIQUE,
    location            VARCHAR(255),
    status              culs.instrument_status NOT NULL DEFAULT 'active',

    -- Constraints
    CONSTRAINT instrument_name_not_empty CHECK (
        length(trim(name)) > 0
    )
);

-- Indexes
CREATE INDEX idx_instrument_status ON culs.instrument(status);
CREATE INDEX idx_instrument_location ON culs.instrument(location);
CREATE INDEX idx_instrument_name ON culs.instrument(name);

-- Comments
COMMENT ON TABLE culs.instrument IS 'Laboratory analytical instruments';
COMMENT ON COLUMN culs.instrument.status IS 'active|maintenance|retired';
COMMENT ON COLUMN culs.instrument.serial_no IS 'Manufacturer serial number (unique)';


-- =====================================================
-- REFERENCE_MATERIAL: Reference materials and standards
-- =====================================================
CREATE TABLE culs.reference_material (
    reference_material_id SERIAL PRIMARY KEY,
    material_type_id    INTEGER NOT NULL REFERENCES culs.material_type(material_type_id) ON DELETE RESTRICT,
    material_source_id  INTEGER REFERENCES culs.material_source(material_source_id) ON DELETE SET NULL,
    material_code       VARCHAR(100) NOT NULL,
    material_name       VARCHAR(255),
    lot_number          VARCHAR(100),
    certificate_number  VARCHAR(100),
    expiry_date         DATE,
    storage_conditions  TEXT,
    notes               TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT reference_material_code_unique UNIQUE (material_source_id, material_code)
);

-- Indexes
CREATE INDEX idx_reference_material_type ON culs.reference_material(material_type_id);
CREATE INDEX idx_reference_material_source ON culs.reference_material(material_source_id);
CREATE INDEX idx_reference_material_code ON culs.reference_material(material_code);
CREATE INDEX idx_reference_material_expiry ON culs.reference_material(expiry_date)
    WHERE expiry_date IS NOT NULL;

-- Comments
COMMENT ON TABLE culs.reference_material IS 'Reference materials and certified standards';
COMMENT ON COLUMN culs.reference_material.material_code IS 'Material identifier (e.g., NIST SRM 610)';
COMMENT ON COLUMN culs.reference_material.lot_number IS 'Manufacturer lot/batch number';
COMMENT ON COLUMN culs.reference_material.certificate_number IS 'Certificate of analysis number';


-- =====================================================
-- INSTRUMENT_CALIBRATION: Instrument calibration records
-- =====================================================
CREATE TABLE culs.instrument_calibration (
    calibration_id      SERIAL PRIMARY KEY,
    instrument_id       INTEGER NOT NULL REFERENCES culs.instrument(instrument_id) ON DELETE CASCADE,
    performed_by_user_id INTEGER REFERENCES culs.user(user_id) ON DELETE SET NULL,
    performed_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    calibration_method  VARCHAR(255),
    is_valid            BOOLEAN NOT NULL DEFAULT TRUE,
    valid_until         TIMESTAMP,
    file_id             INTEGER,  -- FK to FILE_ASSET (will be added later)
    notes               TEXT,

    -- Constraints
    CONSTRAINT calibration_valid_until_after_performed CHECK (
        valid_until IS NULL OR valid_until > performed_at
    )
);

-- Indexes
CREATE INDEX idx_calibration_instrument ON culs.instrument_calibration(instrument_id);
CREATE INDEX idx_calibration_performed_by ON culs.instrument_calibration(performed_by_user_id);
CREATE INDEX idx_calibration_performed_at ON culs.instrument_calibration(performed_at DESC);
CREATE INDEX idx_calibration_valid ON culs.instrument_calibration(instrument_id, is_valid)
    WHERE is_valid = TRUE;

-- Comments
COMMENT ON TABLE culs.instrument_calibration IS 'Instrument calibration and maintenance records';
COMMENT ON COLUMN culs.instrument_calibration.performed_by_user_id IS 'User who performed the calibration';
COMMENT ON COLUMN culs.instrument_calibration.calibration_method IS 'Calibration method or procedure used';
COMMENT ON COLUMN culs.instrument_calibration.is_valid IS 'Whether this calibration is currently valid';
COMMENT ON COLUMN culs.instrument_calibration.valid_until IS 'Expiration timestamp for this calibration';
COMMENT ON COLUMN culs.instrument_calibration.file_id IS 'Reference to calibration report file (FILE_ASSET)';


-- =====================================================
-- CALIBRATION_MEASUREMENT: Individual measurements within a calibration
-- =====================================================
CREATE TABLE culs.calibration_measurement (
    calibration_measurement_id SERIAL PRIMARY KEY,
    calibration_id      INTEGER NOT NULL REFERENCES culs.instrument_calibration(calibration_id) ON DELETE CASCADE,
    reference_material_id INTEGER REFERENCES culs.reference_material(reference_material_id) ON DELETE SET NULL,
    analyte_id          INTEGER REFERENCES culs.analyte(analyte_id) ON DELETE RESTRICT,
    unit_id             INTEGER REFERENCES culs.unit(unit_id) ON DELETE RESTRICT,
    expected_value      DECIMAL(15, 6),
    measured_value      DECIMAL(15, 6),
    uncertainty         DECIMAL(15, 6),
    recovery_percent    DECIMAL(5, 2),  -- Calculated: (measured/expected)*100
    passes_qc           BOOLEAN,
    measurement_order   INTEGER,
    notes               TEXT,

    -- Constraints
    CONSTRAINT calibration_measurement_uncertainty_positive CHECK (
        uncertainty IS NULL OR uncertainty >= 0
    ),
    CONSTRAINT calibration_measurement_recovery_valid CHECK (
        recovery_percent IS NULL OR (recovery_percent >= 0 AND recovery_percent <= 200)
    )
);

-- Indexes
CREATE INDEX idx_calibration_measurement_calibration ON culs.calibration_measurement(calibration_id);
CREATE INDEX idx_calibration_measurement_reference ON culs.calibration_measurement(reference_material_id);
CREATE INDEX idx_calibration_measurement_analyte ON culs.calibration_measurement(analyte_id);
CREATE INDEX idx_calibration_measurement_qc_fail ON culs.calibration_measurement(calibration_id, passes_qc)
    WHERE passes_qc = FALSE;

-- Comments
COMMENT ON TABLE culs.calibration_measurement IS 'Individual analyte measurements during instrument calibration';
COMMENT ON COLUMN culs.calibration_measurement.expected_value IS 'Certified or expected value for the analyte';
COMMENT ON COLUMN culs.calibration_measurement.measured_value IS 'Measured value during calibration';
COMMENT ON COLUMN culs.calibration_measurement.uncertainty IS 'Measurement uncertainty (±)';
COMMENT ON COLUMN culs.calibration_measurement.recovery_percent IS 'Percent recovery: (measured/expected)*100';
COMMENT ON COLUMN culs.calibration_measurement.passes_qc IS 'Whether measurement passes QC criteria';
COMMENT ON COLUMN culs.calibration_measurement.measurement_order IS 'Order of measurement within calibration run';
