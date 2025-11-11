-- =====================================================
-- Projects and Membership Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Project management and user assignments
-- Dependencies: 01_people_and_access.sql
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- PROJECT: Research projects
-- =====================================================
CREATE TABLE culs.project (
    project_id          SERIAL PRIMARY KEY,
    owner_user_id       INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE RESTRICT,
    title               VARCHAR(500) NOT NULL,
    slug                VARCHAR(200) NOT NULL UNIQUE,  -- URL-friendly identifier
    description         TEXT,
    visibility          culs.visibility_level NOT NULL DEFAULT 'restricted',
    status              culs.project_status NOT NULL DEFAULT 'active',
    start_date          DATE,
    end_date            DATE,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT project_dates_valid CHECK (
        end_date IS NULL OR start_date IS NULL OR end_date >= start_date
    ),
    CONSTRAINT project_slug_format CHECK (
        slug ~ '^[a-z0-9-]+$'
    )
);

-- Indexes
CREATE INDEX idx_project_owner ON culs.project(owner_user_id);
CREATE INDEX idx_project_status ON culs.project(status);
CREATE INDEX idx_project_visibility ON culs.project(visibility);
CREATE INDEX idx_project_created_at ON culs.project(created_at DESC);
CREATE INDEX idx_project_slug ON culs.project(slug);

-- Full-text search
CREATE INDEX idx_project_title_fts ON culs.project USING gin(to_tsvector('english', title));
CREATE INDEX idx_project_description_fts ON culs.project USING gin(to_tsvector('english', description));

-- Comments
COMMENT ON TABLE culs.project IS 'Research projects containing samples and analyses';
COMMENT ON COLUMN culs.project.slug IS 'URL-friendly unique identifier (lowercase, hyphens only)';
COMMENT ON COLUMN culs.project.visibility IS 'public|restricted|hidden';
COMMENT ON COLUMN culs.project.status IS 'active|archived';


-- =====================================================
-- PROJECT_USER: Many-to-many relationship between projects and users
-- =====================================================
CREATE TABLE culs.project_user (
    project_id          INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE CASCADE,
    user_id             INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE CASCADE,
    project_role        VARCHAR(50) NOT NULL,
    is_primary          BOOLEAN NOT NULL DEFAULT FALSE,
    assigned_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    removed_at          TIMESTAMP,

    -- Constraints
    PRIMARY KEY (project_id, user_id),
    CONSTRAINT project_user_role_valid CHECK (
        project_role IN ('owner', 'admin', 'collaborator', 'viewer')
    ),
    CONSTRAINT project_user_removed_after_assigned CHECK (
        removed_at IS NULL OR removed_at >= assigned_at
    )
);

-- Indexes
CREATE INDEX idx_project_user_user_id ON culs.project_user(user_id);
CREATE INDEX idx_project_user_role ON culs.project_user(project_role);
CREATE INDEX idx_project_user_is_primary ON culs.project_user(is_primary) WHERE is_primary = TRUE;
CREATE INDEX idx_project_user_active ON culs.project_user(project_id, user_id) WHERE removed_at IS NULL;

-- Comments
COMMENT ON TABLE culs.project_user IS 'User assignments to projects with project-specific roles';
COMMENT ON COLUMN culs.project_user.project_role IS 'owner|admin|collaborator|viewer (per-project role)';
COMMENT ON COLUMN culs.project_user.is_primary IS 'Primary collaborator flag for attribution';
COMMENT ON COLUMN culs.project_user.removed_at IS 'Timestamp when user was removed (NULL = active)';


-- =====================================================
-- PROJECT_SAMPLE_BRIDGE: Many-to-many relationship between projects and samples
-- =====================================================
-- NOTE: This table enables samples to be shared across multiple projects.
-- The sample table still has a direct project_id FK for the "owning" project,
-- but this bridge table allows additional projects to reference the same sample.
CREATE TABLE culs.project_sample_bridge (
    project_id          INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE CASCADE,
    sample_id           INTEGER NOT NULL,  -- FK will be created after sample table exists
    is_owner            BOOLEAN NOT NULL DEFAULT FALSE,
    access_level        VARCHAR(50) NOT NULL DEFAULT 'read',
    added_at            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    added_by_user_id    INTEGER REFERENCES culs.user(user_id) ON DELETE SET NULL,
    removed_at          TIMESTAMP,
    notes               TEXT,

    -- Constraints
    PRIMARY KEY (project_id, sample_id),
    CONSTRAINT project_sample_access_level_valid CHECK (
        access_level IN ('read', 'write', 'admin')
    ),
    CONSTRAINT project_sample_removed_after_added CHECK (
        removed_at IS NULL OR removed_at >= added_at
    )
);

-- Indexes
CREATE INDEX idx_project_sample_bridge_sample_id ON culs.project_sample_bridge(sample_id);
CREATE INDEX idx_project_sample_bridge_added_by ON culs.project_sample_bridge(added_by_user_id);
CREATE INDEX idx_project_sample_bridge_active ON culs.project_sample_bridge(project_id, sample_id)
    WHERE removed_at IS NULL;
CREATE INDEX idx_project_sample_bridge_owner ON culs.project_sample_bridge(sample_id)
    WHERE is_owner = TRUE;

-- Comments
COMMENT ON TABLE culs.project_sample_bridge IS 'Many-to-many bridge enabling samples to be shared across projects';
COMMENT ON COLUMN culs.project_sample_bridge.is_owner IS 'TRUE if this is the owning project for the sample';
COMMENT ON COLUMN culs.project_sample_bridge.access_level IS 'read|write|admin - level of access this project has to the sample';
COMMENT ON COLUMN culs.project_sample_bridge.added_by_user_id IS 'User who added this sample to the project';
COMMENT ON COLUMN culs.project_sample_bridge.removed_at IS 'Timestamp when sample was removed from project (NULL = active)';
