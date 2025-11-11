-- =====================================================
-- Add Foreign Key Constraints
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Add FK constraints that depend on tables created in later scripts
-- Dependencies: All previous SQL scripts (00-09)
-- Run Last: Yes (10)
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- PROJECT_SAMPLE_BRIDGE: Add sample_id foreign key
-- =====================================================
-- This FK must be added after the sample table is created in 05_samples.sql
ALTER TABLE culs.project_sample_bridge
    ADD CONSTRAINT fk_project_sample_bridge_sample_id
    FOREIGN KEY (sample_id)
    REFERENCES culs.sample(sample_id)
    ON DELETE CASCADE;

COMMENT ON CONSTRAINT fk_project_sample_bridge_sample_id ON culs.project_sample_bridge
    IS 'Foreign key to sample table (added after sample table creation)';


-- =====================================================
-- Additional late-stage constraints can be added here
-- =====================================================
