-- =====================================================
-- Sample Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Sample record management
-- Dependencies: 01_people_and_access.sql, 02_projects_and_membership.sql, 04_storage.sql
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- SAMPLE: Physical sample records
-- =====================================================
CREATE TABLE culs.sample (
    sample_id               SERIAL PRIMARY KEY,
    project_id              INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE RESTRICT,
    sample_code             VARCHAR(100) NOT NULL,
    collector_person_id     INTEGER REFERENCES culs.person(person_id) ON DELETE SET NULL,
    collection_date         DATE,
    location_text           TEXT,
    latitude                DECIMAL(10, 7),  -- -90 to 90
    longitude               DECIMAL(10, 7),  -- -180 to 180
    elevation_m             DECIMAL(10, 2),
    status                  culs.sample_status NOT NULL DEFAULT 'drafted',
    storage_location_id     INTEGER REFERENCES culs.storage_location(storage_location_id) ON DELETE SET NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT sample_code_unique_per_project UNIQUE (project_id, sample_code),
    CONSTRAINT sample_latitude_valid CHECK (
        latitude IS NULL OR (latitude >= -90 AND latitude <= 90)
    ),
    CONSTRAINT sample_longitude_valid CHECK (
        longitude IS NULL OR (longitude >= -180 AND longitude <= 180)
    )
);

-- Indexes
CREATE INDEX idx_sample_project ON culs.sample(project_id);
CREATE INDEX idx_sample_collector ON culs.sample(collector_person_id);
CREATE INDEX idx_sample_status ON culs.sample(status);
CREATE INDEX idx_sample_storage ON culs.sample(storage_location_id);
CREATE INDEX idx_sample_created_at ON culs.sample(created_at DESC);
CREATE INDEX idx_sample_code ON culs.sample(sample_code);

-- Geographic index (requires PostGIS)
-- Note: This creates a computed geometry column for efficient spatial queries
ALTER TABLE culs.sample ADD COLUMN geom GEOMETRY(Point, 4326);

CREATE OR REPLACE FUNCTION culs.update_sample_geom()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        NEW.geom := ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
    ELSE
        NEW.geom := NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sample_geom_update
    BEFORE INSERT OR UPDATE OF latitude, longitude ON culs.sample
    FOR EACH ROW
    EXECUTE FUNCTION culs.update_sample_geom();

CREATE INDEX idx_sample_geom ON culs.sample USING GIST(geom);

-- Full-text search
CREATE INDEX idx_sample_code_fts ON culs.sample USING gin(to_tsvector('english', sample_code));
CREATE INDEX idx_sample_location_fts ON culs.sample USING gin(to_tsvector('english', location_text));

-- Comments
COMMENT ON TABLE culs.sample IS 'Physical sample records with collection metadata';
COMMENT ON COLUMN culs.sample.sample_code IS 'Unique sample identifier within project';
COMMENT ON COLUMN culs.sample.status IS 'drafted|ingested|curated|retired';
COMMENT ON COLUMN culs.sample.latitude IS 'Collection location latitude (decimal degrees, WGS84)';
COMMENT ON COLUMN culs.sample.longitude IS 'Collection location longitude (decimal degrees, WGS84)';
COMMENT ON COLUMN culs.sample.elevation_m IS 'Elevation in meters above sea level';
COMMENT ON COLUMN culs.sample.geom IS 'PostGIS geometry point (auto-generated from lat/lon)';
