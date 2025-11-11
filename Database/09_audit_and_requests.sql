-- =====================================================
-- Audit and Request Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: Audit logging, export requests, project transfers
-- Dependencies: 01_people_and_access.sql, 02_projects_and_membership.sql, 08_files.sql
-- =====================================================

SET search_path TO audit, culs, public;

-- =====================================================
-- AUDIT_LOG: Immutable audit trail
-- =====================================================
CREATE TABLE audit.audit_log (
    audit_id            BIGSERIAL PRIMARY KEY,
    actor_user_id       INTEGER REFERENCES culs.user(user_id) ON DELETE SET NULL,
    target_table        VARCHAR(100) NOT NULL,
    target_id           INTEGER,
    action              culs.audit_action NOT NULL,
    changed_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    change_summary      TEXT,
    diff_json           JSONB,

    -- Constraints
    CONSTRAINT audit_target_table_valid CHECK (
        target_table IN (
            'PERSON', 'SYSTEM_ROLE', 'USER', 'PROJECT', 'PROJECT_USER',
            'FUND', 'PROJECT_FUND', 'STORAGE_LOCATION', 'SAMPLE', 'BATCH',
            'INSTRUMENT', 'INSTRUMENT_CALIBRATION', 'ANALYSIS',
            'PHYSICAL_ANALYSIS', 'GEOCHEM_ANALYSIS', 'IMAGING_ANALYSIS',
            'FILE_ASSET', 'PROJECT_FILE', 'SAMPLE_FILE', 'ANALYSIS_FILE',
            'EXPORT_REQUEST', 'PROJECT_TRANSFER'
        )
    )
);

-- Indexes
CREATE INDEX idx_audit_actor ON audit.audit_log(actor_user_id);
CREATE INDEX idx_audit_target ON audit.audit_log(target_table, target_id);
CREATE INDEX idx_audit_action ON audit.audit_log(action);
CREATE INDEX idx_audit_changed_at ON audit.audit_log(changed_at DESC);
CREATE INDEX idx_audit_diff_json ON audit.audit_log USING gin(diff_json);

-- Partition by month for performance (optional, for high-volume systems)
-- This is commented out but can be enabled for production
-- CREATE TABLE audit.audit_log_y2025m01 PARTITION OF audit.audit_log
--     FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- Comments
COMMENT ON TABLE audit.audit_log IS 'Immutable audit trail for all system operations';
COMMENT ON COLUMN audit.audit_log.action IS 'insert|update|delete|export|transfer';
COMMENT ON COLUMN audit.audit_log.diff_json IS 'JSON diff showing old and new values';

-- Prevent updates and deletes on audit log
CREATE OR REPLACE FUNCTION audit.protect_audit_log()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Audit log records are immutable and cannot be modified or deleted';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_log_no_update
    BEFORE UPDATE ON audit.audit_log
    FOR EACH ROW
    EXECUTE FUNCTION audit.protect_audit_log();

CREATE TRIGGER trg_audit_log_no_delete
    BEFORE DELETE ON audit.audit_log
    FOR EACH ROW
    EXECUTE FUNCTION audit.protect_audit_log();


-- =====================================================
-- EXPORT_REQUEST: Data export requests and tracking
-- =====================================================
CREATE TABLE culs.export_request (
    export_id               SERIAL PRIMARY KEY,
    project_id              INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE CASCADE,
    requested_by_user_id    INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE RESTRICT,
    requested_at            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    format                  culs.export_format NOT NULL,
    status                  culs.export_status NOT NULL DEFAULT 'pending',
    delivered_file_id       INTEGER REFERENCES files.file_asset(file_id) ON DELETE SET NULL,

    -- Constraints
    CONSTRAINT export_delivered_when_done CHECK (
        status != 'done' OR delivered_file_id IS NOT NULL
    )
);

-- Indexes
CREATE INDEX idx_export_project ON culs.export_request(project_id);
CREATE INDEX idx_export_requested_by ON culs.export_request(requested_by_user_id);
CREATE INDEX idx_export_status ON culs.export_request(status);
CREATE INDEX idx_export_requested_at ON culs.export_request(requested_at DESC);
CREATE INDEX idx_export_delivered_file ON culs.export_request(delivered_file_id);

-- Comments
COMMENT ON TABLE culs.export_request IS 'Data export requests and delivery tracking';
COMMENT ON COLUMN culs.export_request.format IS 'csv|xlsx|json|netcdf|zip';
COMMENT ON COLUMN culs.export_request.status IS 'pending|processing|done|failed';
COMMENT ON COLUMN culs.export_request.delivered_file_id IS 'Reference to generated export file';


-- =====================================================
-- PROJECT_TRANSFER: Project ownership transfers
-- =====================================================
CREATE TABLE culs.project_transfer (
    transfer_id         SERIAL PRIMARY KEY,
    project_id          INTEGER NOT NULL REFERENCES culs.project(project_id) ON DELETE CASCADE,
    from_user_id        INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE RESTRICT,
    to_user_id          INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE RESTRICT,
    initiated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_at         TIMESTAMP,
    status              culs.transfer_status NOT NULL DEFAULT 'pending',

    -- Constraints
    CONSTRAINT transfer_different_users CHECK (
        from_user_id != to_user_id
    ),
    CONSTRAINT transfer_approved_at_valid CHECK (
        approved_at IS NULL OR approved_at >= initiated_at
    ),
    CONSTRAINT transfer_approved_when_approved CHECK (
        status != 'approved' OR approved_at IS NOT NULL
    )
);

-- Indexes
CREATE INDEX idx_transfer_project ON culs.project_transfer(project_id);
CREATE INDEX idx_transfer_from_user ON culs.project_transfer(from_user_id);
CREATE INDEX idx_transfer_to_user ON culs.project_transfer(to_user_id);
CREATE INDEX idx_transfer_status ON culs.project_transfer(status);
CREATE INDEX idx_transfer_initiated_at ON culs.project_transfer(initiated_at DESC);

-- Comments
COMMENT ON TABLE culs.project_transfer IS 'Project ownership transfer requests and approvals';
COMMENT ON COLUMN culs.project_transfer.status IS 'pending|approved|rejected';


-- =====================================================
-- Trigger to log all changes to audit_log
-- =====================================================
CREATE OR REPLACE FUNCTION audit.log_change()
RETURNS TRIGGER AS $$
DECLARE
    v_action culs.audit_action;
    v_actor_id INTEGER;
    v_diff JSONB;
BEGIN
    -- Determine action
    IF TG_OP = 'INSERT' THEN
        v_action := 'insert';
    ELSIF TG_OP = 'UPDATE' THEN
        v_action := 'update';
    ELSIF TG_OP = 'DELETE' THEN
        v_action := 'delete';
    END IF;

    -- Try to get actor from current_setting (should be set by application)
    BEGIN
        v_actor_id := current_setting('app.current_user_id')::INTEGER;
    EXCEPTION WHEN OTHERS THEN
        v_actor_id := NULL;
    END;

    -- Build diff JSON
    IF TG_OP = 'UPDATE' THEN
        v_diff := jsonb_build_object(
            'old', to_jsonb(OLD),
            'new', to_jsonb(NEW)
        );
    ELSIF TG_OP = 'INSERT' THEN
        v_diff := jsonb_build_object('new', to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        v_diff := jsonb_build_object('old', to_jsonb(OLD));
    END IF;

    -- Insert audit record
    INSERT INTO audit.audit_log (
        actor_user_id,
        target_table,
        target_id,
        action,
        change_summary,
        diff_json
    ) VALUES (
        v_actor_id,
        TG_TABLE_NAME,
        COALESCE(NEW.project_id, NEW.sample_id, NEW.analysis_id, NEW.user_id, OLD.project_id, OLD.sample_id, OLD.analysis_id, OLD.user_id),
        v_action,
        TG_OP || ' on ' || TG_TABLE_NAME,
        v_diff
    );

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Example: Enable audit logging on critical tables
-- CREATE TRIGGER trg_project_audit AFTER INSERT OR UPDATE OR DELETE ON culs.project
--     FOR EACH ROW EXECUTE FUNCTION audit.log_change();
-- CREATE TRIGGER trg_sample_audit AFTER INSERT OR UPDATE OR DELETE ON culs.sample
--     FOR EACH ROW EXECUTE FUNCTION audit.log_change();
