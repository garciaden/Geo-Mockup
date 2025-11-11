-- =====================================================
-- Funding Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Grant and funding source tracking
-- Dependencies: 02_projects_and_membership.sql
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- FUND: Funding sources and grants
-- =====================================================
CREATE TABLE culs.fund (
    fund_id             SERIAL PRIMARY KEY,
    sponsor_name        VARCHAR(255),
    grant_code          VARCHAR(100) UNIQUE,
    title               VARCHAR(500),
    start_date          DATE,
    end_date            DATE,
    notes               TEXT,

    -- Constraints
    CONSTRAINT fund_dates_valid CHECK (
        end_date IS NULL OR start_date IS NULL OR end_date >= start_date
    )
);

-- Indexes
CREATE INDEX idx_fund_sponsor ON culs.fund(sponsor_name);
CREATE INDEX idx_fund_grant_code ON culs.fund(grant_code);
CREATE INDEX idx_fund_dates ON culs.fund(start_date, end_date);

-- Comments
COMMENT ON TABLE culs.fund IS 'Funding sources and grant information';
COMMENT ON COLUMN culs.fund.grant_code IS 'Unique grant/award identifier';
COMMENT ON COLUMN culs.fund.sponsor_name IS 'Funding organization or sponsor';


-- =====================================================
-- PROJECT_FUND: Many-to-many relationship between projects and funding
-- =====================================================
CREATE TABLE culs.project_fund (
    project_id          INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE CASCADE,
    fund_id             INTEGER NOT NULL REFERENCES culs.fund(fund_id) ON DELETE RESTRICT,
    allocation_percent  DECIMAL(5,2),
    notes               TEXT,

    -- Constraints
    PRIMARY KEY (project_id, fund_id),
    CONSTRAINT project_fund_allocation_valid CHECK (
        allocation_percent IS NULL OR (allocation_percent >= 0 AND allocation_percent <= 100)
    )
);

-- Indexes
CREATE INDEX idx_project_fund_fund_id ON culs.project_fund(fund_id);

-- Comments
COMMENT ON TABLE culs.project_fund IS 'Project funding source associations';
COMMENT ON COLUMN culs.project_fund.allocation_percent IS 'Percentage of project funded by this source (0-100)';
