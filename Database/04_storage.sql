-- =====================================================
-- Physical Storage Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Physical storage location tracking
-- Dependencies: 00_init.sql
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- STORAGE_LOCATION: Physical storage locations for samples
-- =====================================================
CREATE TABLE culs.storage_location (
    storage_location_id SERIAL PRIMARY KEY,
    facility_name       VARCHAR(255),
    room                VARCHAR(100),
    cabinet             VARCHAR(100),
    shelf               VARCHAR(100),
    box                 VARCHAR(100),
    position_label      VARCHAR(100),
    notes               TEXT,

    -- Constraints
    CONSTRAINT storage_location_not_empty CHECK (
        facility_name IS NOT NULL OR
        room IS NOT NULL OR
        cabinet IS NOT NULL OR
        shelf IS NOT NULL OR
        box IS NOT NULL OR
        position_label IS NOT NULL
    )
);

-- Indexes
CREATE INDEX idx_storage_facility ON culs.storage_location(facility_name);
CREATE INDEX idx_storage_room ON culs.storage_location(room);
CREATE INDEX idx_storage_cabinet ON culs.storage_location(cabinet);
CREATE INDEX idx_storage_full_path ON culs.storage_location(facility_name, room, cabinet, shelf, box);

-- Comments
COMMENT ON TABLE culs.storage_location IS 'Hierarchical physical storage locations for samples';
COMMENT ON COLUMN culs.storage_location.facility_name IS 'Building or facility name';
COMMENT ON COLUMN culs.storage_location.position_label IS 'Specific position within box/shelf';

-- Helper function to generate full storage path
CREATE OR REPLACE FUNCTION culs.get_storage_path(loc_id INTEGER)
RETURNS TEXT AS $$
DECLARE
    path_parts TEXT[];
    result TEXT;
BEGIN
    SELECT ARRAY[facility_name, room, cabinet, shelf, box, position_label]
    INTO path_parts
    FROM culs.storage_location
    WHERE storage_location_id = loc_id;

    -- Remove NULL elements and join with ' > '
    SELECT string_agg(part, ' > ')
    INTO result
    FROM unnest(path_parts) AS part
    WHERE part IS NOT NULL;

    RETURN COALESCE(result, 'Unknown Location');
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION culs.get_storage_path IS 'Generate human-readable storage path from location ID';
