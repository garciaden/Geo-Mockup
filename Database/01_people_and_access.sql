-- =====================================================
-- People and Access Control Tables
-- Concord University Laboratory Software (CULS)
-- =====================================================
-- Purpose: User authentication, people records, roles
-- Dependencies: 00_init.sql
-- =====================================================

SET search_path TO culs, public;

-- =====================================================
-- COUNTRY: Lookup table for countries
-- =====================================================
CREATE TABLE culs.country (
    country_id          SERIAL PRIMARY KEY,
    country_code        VARCHAR(2) NOT NULL UNIQUE,  -- ISO 3166-1 alpha-2
    country_name        VARCHAR(100) NOT NULL,
    country_code_3      VARCHAR(3),  -- ISO 3166-1 alpha-3

    -- Constraints
    CONSTRAINT country_code_format CHECK (
        country_code ~ '^[A-Z]{2}$'
    )
);

-- Comments
COMMENT ON TABLE culs.country IS 'ISO 3166-1 country codes and names';
COMMENT ON COLUMN culs.country.country_code IS 'ISO 3166-1 alpha-2 code (e.g., US, GB, FR)';
COMMENT ON COLUMN culs.country.country_code_3 IS 'ISO 3166-1 alpha-3 code (e.g., USA, GBR, FRA)';

-- Insert common countries (expand as needed)
INSERT INTO culs.country (country_code, country_name, country_code_3) VALUES
    ('US', 'United States', 'USA'),
    ('GB', 'United Kingdom', 'GBR'),
    ('CA', 'Canada', 'CAN'),
    ('AU', 'Australia', 'AUS'),
    ('DE', 'Germany', 'DEU'),
    ('FR', 'France', 'FRA'),
    ('JP', 'Japan', 'JPN'),
    ('CN', 'China', 'CHN'),
    ('IN', 'India', 'IND'),
    ('BR', 'Brazil', 'BRA');


-- =====================================================
-- ORGANIZATION_TYPE: Lookup table for organization types
-- =====================================================
CREATE TABLE culs.organization_type (
    organization_type_id SERIAL PRIMARY KEY,
    type_code            VARCHAR(20) NOT NULL UNIQUE,
    type_name            VARCHAR(100) NOT NULL,
    description          TEXT,

    -- Constraints
    CONSTRAINT organization_type_code_valid CHECK (
        type_code IN ('university', 'research_institute', 'government', 'private_company', 'nonprofit', 'other')
    )
);

-- Comments
COMMENT ON TABLE culs.organization_type IS 'Lookup table for organization type categories';
COMMENT ON COLUMN culs.organization_type.type_code IS 'Unique type identifier';

-- Insert default organization types
INSERT INTO culs.organization_type (type_code, type_name, description) VALUES
    ('university', 'University', 'Academic institution granting degrees'),
    ('research_institute', 'Research Institute', 'Research-focused organization'),
    ('government', 'Government Agency', 'Government or public sector organization'),
    ('private_company', 'Private Company', 'For-profit private sector company'),
    ('nonprofit', 'Non-Profit Organization', 'Non-profit or NGO'),
    ('other', 'Other', 'Other type of organization');


-- =====================================================
-- ORGANIZATION: Organizations and institutions
-- =====================================================
CREATE TABLE culs.organization (
    organization_id     SERIAL PRIMARY KEY,
    organization_type_id INTEGER REFERENCES culs.organization_type(organization_type_id) ON DELETE RESTRICT,
    country_id          INTEGER REFERENCES culs.country(country_id) ON DELETE RESTRICT,
    name                VARCHAR(255) NOT NULL,
    abbreviation        VARCHAR(50),
    website             VARCHAR(255),
    address             TEXT,
    city                VARCHAR(100),
    state_province      VARCHAR(100),
    postal_code         VARCHAR(20),
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT organization_website_format CHECK (
        website IS NULL OR website ~ '^https?://.*'
    )
);

-- Indexes
CREATE INDEX idx_organization_type_id ON culs.organization(organization_type_id);
CREATE INDEX idx_organization_country_id ON culs.organization(country_id);
CREATE INDEX idx_organization_name ON culs.organization(name);
CREATE INDEX idx_organization_abbreviation ON culs.organization(abbreviation);

-- Full-text search
CREATE INDEX idx_organization_name_fts ON culs.organization USING gin(to_tsvector('english', name));

-- Comments
COMMENT ON TABLE culs.organization IS 'Organizations and institutions for person affiliations';
COMMENT ON COLUMN culs.organization.abbreviation IS 'Common abbreviation or acronym';
COMMENT ON COLUMN culs.organization.website IS 'Organization website URL';


-- =====================================================
-- CONTACT_TYPE: Lookup table for contact types
-- =====================================================
CREATE TABLE culs.contact_type (
    contact_type_id     SERIAL PRIMARY KEY,
    type_code           VARCHAR(20) NOT NULL UNIQUE,
    type_name           VARCHAR(100) NOT NULL,
    description         TEXT,

    -- Constraints
    CONSTRAINT contact_type_code_valid CHECK (
        type_code IN ('primary_email', 'secondary_email', 'work_phone', 'mobile_phone', 'office_address', 'home_address', 'other')
    )
);

-- Comments
COMMENT ON TABLE culs.contact_type IS 'Lookup table for contact information types';

-- Insert default contact types
INSERT INTO culs.contact_type (type_code, type_name, description) VALUES
    ('primary_email', 'Primary Email', 'Main email address'),
    ('secondary_email', 'Secondary Email', 'Alternate email address'),
    ('work_phone', 'Work Phone', 'Work/office phone number'),
    ('mobile_phone', 'Mobile Phone', 'Mobile/cell phone number'),
    ('office_address', 'Office Address', 'Work/office mailing address'),
    ('home_address', 'Home Address', 'Home/residential address'),
    ('other', 'Other', 'Other contact method');


-- =====================================================
-- IDENTIFIER_TYPE: Lookup table for person identifier types
-- =====================================================
CREATE TABLE culs.identifier_type (
    identifier_type_id  SERIAL PRIMARY KEY,
    type_code           VARCHAR(20) NOT NULL UNIQUE,
    type_name           VARCHAR(100) NOT NULL,
    description         TEXT,

    -- Constraints
    CONSTRAINT identifier_type_code_valid CHECK (
        type_code IN ('passport', 'national_id', 'drivers_license', 'employee_id', 'student_id', 'orcid', 'other')
    )
);

-- Comments
COMMENT ON TABLE culs.identifier_type IS 'Lookup table for person identifier types';

-- Insert default identifier types
INSERT INTO culs.identifier_type (type_code, type_name, description) VALUES
    ('orcid', 'ORCID', 'Open Researcher and Contributor ID'),
    ('passport', 'Passport', 'Passport number'),
    ('national_id', 'National ID', 'National identification number'),
    ('drivers_license', 'Drivers License', 'Drivers license number'),
    ('employee_id', 'Employee ID', 'Organization employee ID'),
    ('student_id', 'Student ID', 'University student ID'),
    ('other', 'Other', 'Other identifier type');


-- =====================================================
-- PERSON: Individual people (may or may not have user accounts)
-- =====================================================
CREATE TABLE culs.person (
    person_id           SERIAL PRIMARY KEY,
    organization_id     INTEGER REFERENCES culs.organization(organization_id) ON DELETE SET NULL,
    given_name          VARCHAR(100),
    family_name         VARCHAR(100),
    middle_name         VARCHAR(100),
    display_name        VARCHAR(255),
    title               VARCHAR(100),  -- Dr., Prof., Mr., Ms., etc.
    position            VARCHAR(255),  -- Job title or academic position
    department          VARCHAR(255),  -- Department within organization
    orcid               VARCHAR(19) UNIQUE,  -- Format: XXXX-XXXX-XXXX-XXXX
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT person_orcid_format CHECK (
        orcid IS NULL OR orcid ~ '^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$'
    )
);

-- Indexes
CREATE INDEX idx_person_organization_id ON culs.person(organization_id);
CREATE INDEX idx_person_orcid ON culs.person(orcid) WHERE orcid IS NOT NULL;
CREATE INDEX idx_person_name ON culs.person(family_name, given_name);
CREATE INDEX idx_person_department ON culs.person(department);

-- Comments
COMMENT ON TABLE culs.person IS 'Individual people records for attribution and collaboration';
COMMENT ON COLUMN culs.person.organization_id IS 'Primary organizational affiliation';
COMMENT ON COLUMN culs.person.orcid IS 'Open Researcher and Contributor ID (XXXX-XXXX-XXXX-XXXX)';
COMMENT ON COLUMN culs.person.display_name IS 'Preferred display name (auto-generated if NULL)';
COMMENT ON COLUMN culs.person.title IS 'Professional or academic title (Dr., Prof., etc.)';
COMMENT ON COLUMN culs.person.position IS 'Job title or academic position';


-- =====================================================
-- CONTACT: Contact information for persons
-- =====================================================
CREATE TABLE culs.contact (
    contact_id          SERIAL PRIMARY KEY,
    person_id           INTEGER NOT NULL REFERENCES culs.person(person_id) ON DELETE CASCADE,
    contact_type_id     INTEGER NOT NULL REFERENCES culs.contact_type(contact_type_id) ON DELETE RESTRICT,
    contact_value       TEXT NOT NULL,
    is_primary          BOOLEAN NOT NULL DEFAULT FALSE,
    is_public           BOOLEAN NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT contact_value_not_empty CHECK (
        length(trim(contact_value)) > 0
    )
);

-- Indexes
CREATE INDEX idx_contact_person_id ON culs.contact(person_id);
CREATE INDEX idx_contact_type_id ON culs.contact(contact_type_id);
CREATE INDEX idx_contact_is_primary ON culs.contact(person_id, is_primary) WHERE is_primary = TRUE;
CREATE INDEX idx_contact_is_public ON culs.contact(is_public) WHERE is_public = TRUE;

-- Comments
COMMENT ON TABLE culs.contact IS 'Contact information for persons (emails, phones, addresses)';
COMMENT ON COLUMN culs.contact.contact_value IS 'The actual contact information (email, phone, address, etc.)';
COMMENT ON COLUMN culs.contact.is_primary IS 'Primary contact method for this type';
COMMENT ON COLUMN culs.contact.is_public IS 'Whether contact info is publicly visible';


-- =====================================================
-- PERSON_IDENTIFIER: Additional identifiers for persons
-- =====================================================
CREATE TABLE culs.person_identifier (
    person_identifier_id SERIAL PRIMARY KEY,
    person_id            INTEGER NOT NULL REFERENCES culs.person(person_id) ON DELETE CASCADE,
    identifier_type_id   INTEGER NOT NULL REFERENCES culs.identifier_type(identifier_type_id) ON DELETE RESTRICT,
    country_id           INTEGER REFERENCES culs.country(country_id) ON DELETE SET NULL,
    identifier_value     VARCHAR(255) NOT NULL,
    issued_date          DATE,
    expiry_date          DATE,
    notes                TEXT,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT person_identifier_unique_per_type UNIQUE (person_id, identifier_type_id, identifier_value),
    CONSTRAINT person_identifier_expiry_after_issued CHECK (
        expiry_date IS NULL OR issued_date IS NULL OR expiry_date >= issued_date
    )
);

-- Indexes
CREATE INDEX idx_person_identifier_person_id ON culs.person_identifier(person_id);
CREATE INDEX idx_person_identifier_type_id ON culs.person_identifier(identifier_type_id);
CREATE INDEX idx_person_identifier_country_id ON culs.person_identifier(country_id);
CREATE INDEX idx_person_identifier_value ON culs.person_identifier(identifier_value);

-- Comments
COMMENT ON TABLE culs.person_identifier IS 'Additional identifiers for persons (passports, IDs, etc.)';
COMMENT ON COLUMN culs.person_identifier.identifier_value IS 'The identifier number/value';
COMMENT ON COLUMN culs.person_identifier.country_id IS 'Issuing country for national identifiers';


-- =====================================================
-- SYSTEM_ROLE: System-level roles
-- =====================================================
CREATE TABLE culs.system_role (
    system_role_id      SERIAL PRIMARY KEY,
    role_name           VARCHAR(50) NOT NULL UNIQUE,
    description         TEXT,

    -- Constraints
    CONSTRAINT system_role_name_valid CHECK (
        role_name IN ('admin', 'owner', 'collaborator', 'viewer')
    )
);

-- Comments
COMMENT ON TABLE culs.system_role IS 'System-level roles defining base permissions';
COMMENT ON COLUMN culs.system_role.role_name IS 'admin|owner|collaborator|viewer';

-- Insert default roles
INSERT INTO culs.system_role (role_name, description) VALUES
    ('admin', 'System administrator with full access'),
    ('owner', 'Project owner with management permissions'),
    ('collaborator', 'Project collaborator with data entry permissions'),
    ('viewer', 'View-only access to assigned projects');


-- =====================================================
-- USER_STATUS: Lookup table for user account statuses
-- =====================================================
CREATE TABLE culs.user_status (
    user_status_id      SERIAL PRIMARY KEY,
    status_code         VARCHAR(20) NOT NULL UNIQUE,
    status_name         VARCHAR(100) NOT NULL,
    description         TEXT,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,

    -- Constraints
    CONSTRAINT user_status_code_valid CHECK (
        status_code IN ('active', 'locked', 'disabled', 'pending', 'suspended')
    )
);

-- Comments
COMMENT ON TABLE culs.user_status IS 'Lookup table for user account status values';
COMMENT ON COLUMN culs.user_status.status_code IS 'Unique status identifier (active|locked|disabled|pending|suspended)';
COMMENT ON COLUMN culs.user_status.is_active IS 'Whether accounts with this status can log in';

-- Insert default user statuses
INSERT INTO culs.user_status (status_code, status_name, description, is_active) VALUES
    ('pending', 'Pending Activation', 'User account created but not yet activated', FALSE),
    ('active', 'Active', 'User account is active and can log in', TRUE),
    ('locked', 'Locked', 'Account temporarily locked due to failed login attempts', FALSE),
    ('disabled', 'Disabled', 'Account disabled by administrator', FALSE),
    ('suspended', 'Suspended', 'Account temporarily suspended', FALSE);


-- =====================================================
-- SESSION_STATUS: Lookup table for session statuses
-- =====================================================
CREATE TABLE culs.session_status (
    session_status_id   SERIAL PRIMARY KEY,
    status_code         VARCHAR(20) NOT NULL UNIQUE,
    status_name         VARCHAR(100) NOT NULL,
    description         TEXT,

    -- Constraints
    CONSTRAINT session_status_code_valid CHECK (
        status_code IN ('active', 'expired', 'terminated', 'invalidated')
    )
);

-- Comments
COMMENT ON TABLE culs.session_status IS 'Lookup table for user session status values';
COMMENT ON COLUMN culs.session_status.status_code IS 'Unique status identifier (active|expired|terminated|invalidated)';

-- Insert default session statuses
INSERT INTO culs.session_status (status_code, status_name, description) VALUES
    ('active', 'Active', 'Session is currently active'),
    ('expired', 'Expired', 'Session expired due to timeout'),
    ('terminated', 'Terminated', 'Session terminated by user (logout)'),
    ('invalidated', 'Invalidated', 'Session invalidated by administrator or security event');


-- =====================================================
-- USER: System user accounts
-- =====================================================
CREATE TABLE culs.user (
    user_id             SERIAL PRIMARY KEY,
    person_id           INTEGER REFERENCES culs.person(person_id) ON DELETE RESTRICT,
    system_role_id      INTEGER NOT NULL REFERENCES culs.system_role(system_role_id) ON DELETE RESTRICT,
    user_status_id      INTEGER NOT NULL REFERENCES culs.user_status(user_status_id) ON DELETE RESTRICT DEFAULT 4,  -- Default to 'pending'
    username            VARCHAR(100) NOT NULL UNIQUE,
    email               VARCHAR(255) NOT NULL UNIQUE,
    password_hash       VARCHAR(255) NOT NULL,  -- bcrypt/argon2 hash
    mfa_enabled         BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret          VARCHAR(255),  -- TOTP secret for MFA
    last_login_at       TIMESTAMP,
    password_changed_at TIMESTAMP,
    failed_login_count  INTEGER NOT NULL DEFAULT 0,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT user_email_format CHECK (
        email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    ),
    CONSTRAINT user_username_format CHECK (
        username ~ '^[a-zA-Z0-9_-]{3,50}$'
    ),
    CONSTRAINT user_failed_login_positive CHECK (
        failed_login_count >= 0
    )
);

-- Indexes
CREATE INDEX idx_user_person_id ON culs.user(person_id);
CREATE INDEX idx_user_system_role_id ON culs.user(system_role_id);
CREATE INDEX idx_user_status_id ON culs.user(user_status_id);
CREATE INDEX idx_user_email ON culs.user(email);
CREATE INDEX idx_user_last_login ON culs.user(last_login_at DESC);
CREATE INDEX idx_user_username ON culs.user(username);

-- Comments
COMMENT ON TABLE culs.user IS 'System user accounts with authentication credentials';
COMMENT ON COLUMN culs.user.person_id IS 'Link to person record (optional for system accounts)';
COMMENT ON COLUMN culs.user.password_hash IS 'Hashed password using bcrypt or argon2';
COMMENT ON COLUMN culs.user.user_status_id IS 'Foreign key to user_status lookup table';
COMMENT ON COLUMN culs.user.mfa_enabled IS 'Multi-factor authentication enabled flag';
COMMENT ON COLUMN culs.user.mfa_secret IS 'TOTP secret for MFA (encrypted)';
COMMENT ON COLUMN culs.user.failed_login_count IS 'Count of consecutive failed login attempts';


-- =====================================================
-- USER_SESSION: Track user login sessions
-- =====================================================
CREATE TABLE culs.user_session (
    session_id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             INTEGER NOT NULL REFERENCES culs.user(user_id) ON DELETE CASCADE,
    session_status_id   INTEGER NOT NULL REFERENCES culs.session_status(session_status_id) ON DELETE RESTRICT DEFAULT 1,  -- Default to 'active'
    session_token       VARCHAR(255) NOT NULL UNIQUE,
    ip_address          INET,
    user_agent          TEXT,
    started_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_activity_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at          TIMESTAMP NOT NULL,
    ended_at            TIMESTAMP,

    -- Constraints
    CONSTRAINT user_session_expires_after_start CHECK (
        expires_at > started_at
    ),
    CONSTRAINT user_session_ended_after_start CHECK (
        ended_at IS NULL OR ended_at >= started_at
    )
);

-- Indexes
CREATE INDEX idx_user_session_user_id ON culs.user_session(user_id);
CREATE INDEX idx_user_session_status_id ON culs.user_session(session_status_id);
CREATE INDEX idx_user_session_token ON culs.user_session(session_token);
CREATE INDEX idx_user_session_started_at ON culs.user_session(started_at DESC);
CREATE INDEX idx_user_session_active ON culs.user_session(user_id, session_status_id)
    WHERE session_status_id = 1 AND ended_at IS NULL;

-- Comments
COMMENT ON TABLE culs.user_session IS 'Track user login sessions for security and auditing';
COMMENT ON COLUMN culs.user_session.session_token IS 'Unique session token (hashed)';
COMMENT ON COLUMN culs.user_session.ip_address IS 'IP address of client';
COMMENT ON COLUMN culs.user_session.user_agent IS 'Browser/client user agent string';
COMMENT ON COLUMN culs.user_session.last_activity_at IS 'Timestamp of last user activity in session';
COMMENT ON COLUMN culs.user_session.expires_at IS 'Session expiration timestamp';
COMMENT ON COLUMN culs.user_session.ended_at IS 'Timestamp when session ended (NULL if still active)';
