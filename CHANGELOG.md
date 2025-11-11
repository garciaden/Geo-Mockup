# Changelog

## 11/11/25 - Database Schema Implementation

### Database Integration & Schema Updates

**Overview**: Updated Database folder SQL scripts to match FinalNormalization diagrams, focusing on User, Person, Project, and Supporting domains (highest priority for Phase 1 authentication and basic functionality).

#### User Domain Enhancements (`01_people_and_access.sql`)

- **Added `user_status` lookup table**
  - Status codes: pending, active, locked, disabled, suspended
  - Tracks whether accounts can log in (`is_active` flag)
  - Replaced ENUM with normalized lookup table

- **Added `session_status` lookup table**
  - Status codes: active, expired, terminated, invalidated
  - For user session state management

- **Added `user_session` table**
  - Tracks login sessions with UUID primary keys
  - Records IP address, user agent, session tokens
  - Implements session expiration and activity tracking
  - Foreign keys to `user` and `session_status`

- **Enhanced `user` table**
  - Added FK to `user_status` (replaces ENUM field)
  - Added MFA support: `mfa_enabled`, `mfa_secret` fields
  - Added `failed_login_count` for account lockout
  - Added `password_changed_at` timestamp
  - Added `updated_at` timestamp for auditing

#### Person Domain Expansion (`01_people_and_access.sql`)

- **Added `country` lookup table**
  - ISO 3166-1 alpha-2 codes (US, GB, CA, etc.)
  - ISO 3166-1 alpha-3 codes (USA, GBR, CAN, etc.)
  - Pre-populated with 10 common countries

- **Added `organization_type` lookup table**
  - Types: university, research_institute, government, private_company, nonprofit, other
  - Pre-populated with descriptions

- **Added `organization` table**
  - Links to `organization_type` and `country`
  - Fields: name, abbreviation, website, full address
  - Full-text search index on organization name

- **Added `contact_type` lookup table**
  - Types: primary_email, secondary_email, work_phone, mobile_phone, office_address, home_address, other
  - Pre-populated with all contact types

- **Added `contact` table**
  - Multiple contacts per person (emails, phones, addresses)
  - Links to `person` and `contact_type`
  - `is_primary` and `is_public` flags
  - Flexible `contact_value` TEXT field

- **Added `identifier_type` lookup table**
  - Types: orcid, passport, national_id, drivers_license, employee_id, student_id, other
  - Pre-populated with common identifier types

- **Added `person_identifier` table**
  - Multiple identifiers per person (passports, IDs, employee numbers, etc.)
  - Links to `person`, `identifier_type`, and optional `country`
  - Tracks `issued_date` and `expiry_date`
  - Unique constraint on (person_id, identifier_type_id, identifier_value)

- **Enhanced `person` table**
  - Added FK to `organization` for primary affiliation
  - Added `title` field (Dr., Prof., Mr., Ms., etc.)
  - Added `position` field (job title or academic position)
  - Added `department` field
  - Added `updated_at` timestamp
  - Removed direct `email`, `phone`, `affiliation` fields (now in `contact` table)

#### Project Domain Improvements (`02_projects_and_membership.sql`)

- **Added `project_sample_bridge` junction table**
  - Enables samples to be shared across multiple projects
  - Tracks `is_owner` flag for sample ownership
  - Implements `access_level` (read, write, admin)
  - Records `added_by_user_id` and `added_at` timestamp
  - Soft delete with `removed_at` timestamp
  - Foreign key to `sample` added via late-stage constraint file

#### Supporting Domain Enhancements (`06_batches_and_instruments.sql`)

- **Added `material_type` lookup table**
  - Types: standard, blank, control, spike, duplicate, matrix, other
  - For reference material classification

- **Added `material_source` lookup table**
  - Common sources: NIST, USGS, NRC, IAEA, INTERNAL, OTHER
  - Includes abbreviations and website URLs

- **Added `analyte` lookup table**
  - Chemical elements and compounds (SiO2, Al2O3, Fe2O3, etc.)
  - Includes chemical formulas and CAS Registry Numbers
  - Pre-populated with 10 common analytes
  - CAS number format validation

- **Added `unit` lookup table**
  - Measurement units: ppm, ppb, wt%, mg/L, ug/L, g, mg, mL, L, mm, cm, degC, ratio
  - Categorized by `unit_type` (concentration, mass, volume, length, temperature, etc.)

- **Added `reference_material` table**
  - Certified reference materials and standards
  - Links to `material_type` and `material_source`
  - Tracks lot numbers, certificate numbers, expiry dates
  - Storage conditions and notes

- **Enhanced `instrument_calibration` table**
  - Added `performed_by_user_id` FK to track who performed calibration
  - Added `is_valid` boolean flag
  - Added `valid_until` timestamp for calibration expiration
  - Renamed `method` to `calibration_method` for clarity

- **Added `calibration_measurement` table**
  - Individual analyte measurements during calibration runs
  - Links to `calibration`, `reference_material`, `analyte`, `unit`
  - Tracks `expected_value`, `measured_value`, `uncertainty`
  - Calculates `recovery_percent` ((measured/expected)*100)
  - `passes_qc` flag for quality control
  - `measurement_order` for sequential measurements

#### Infrastructure Updates

- **Created `10_add_foreign_keys.sql`**
  - Late-stage foreign key constraints for cross-file dependencies
  - Adds `sample_id` FK to `project_sample_bridge` after `sample` table creation
  - Documented for future late-stage constraints

- **Updated `00_init.sql`**
  - Removed `user_status` ENUM type (converted to lookup table)
  - Added documentation comment explaining the change

#### Database Testing & Validation

- Successfully created database with **33 tables** in `culs` schema
- All foreign key constraints properly established
- All lookup tables populated with default data
- Verified table structures match FinalNormalization diagrams
- Tested with Docker Compose PostgreSQL 15 + PostGIS 3.3

### UI Bug Fixes

- **Fixed broken breadcrumb in Sample view** (`sample_view.html`)
  - Removed broken "Projects" link that pointed to non-existent route
  - Simplified breadcrumb navigation to: Home  Project Title â Sample Name
  - Maintains context while eliminating dead link

### Documentation Updates

- Updated `SCHEMA_COMPARISON.md` with detailed analysis of changes
- Updated `TODO.md` with database integration progress
- Updated `CHANGELOG.md` with comprehensive session documentation

---

## 11/10/25 - Changes made by Matthew Kenner

### Homepage Updates

- Added sortable "Last Updated" column with relative time formatting ("2 days ago")
- Added sort button for "Last Updated" (Oldest/Newest)
- Relative time formatter converts dates to human-readable format

### Project View Updates

- Added breadcrumb navigation (Home > Project Name)
- Gear icon for settings button (was already present!)
- Renamed "Sample Name"  "Short Description"
- Added "Laboratory Catalog Number" column (with placeholder data: LAB-2025-001, etc.)

### Sample View Updates

- Changed "Upload Image"  "Upload Files"
- Geochemical Analysis: Converted to collapsible accordion sections
  - Alphabetically sorted (EPMA/SEM, Geochronology, ICP-MS, LA-ICP-MS, Micro XRF, SIMS, Whole XRF)
  - Multiple sections can be open simultaneously (removed data-bs-parent)
  - Shows badge with number of runs per section
- Added Inventory & Sub-samples section with:
  - Table: Fraction ID, Storage Location, Quantity, Unit, Status
  - Placeholder data showing sieve fractions (2-1mm, 1mm-63Âµm, <63Âµm)
  - Total quantity summary
- Added Sample Disbursements section with:
  - Table: Date, Recipient, Institution, Quantity, Purpose
  - "Record Disbursement" button
  - Helpful info message

### Mock Login System

Created a complete development login system with 5 roles:

Quick Login URLs (fastest for dev):

- Administrator: http://localhost:5000/auth/quick-login/Administrator
- Project Owner: http://localhost:5000/auth/quick-login/Project_Owner
- Collaborator: http://localhost:5000/auth/quick-login/Collaborator
- View & Export: http://localhost:5000/auth/quick-login/View_Export
- View Only: http://localhost:5000/auth/quick-login/View_Only

Login Page: http://localhost:5000/auth/login

Features:

- Session-based authentication
- Role-based permissions
- User dropdown in navigation (shows role badge + permissions)
- "Add Project" button hidden for non-authorized users
- Sample edit buttons respect user permissions
- Logout functionality
- Comprehensive documentation (app/auth/README_MOCK_LOGIN.md)

### Bug Fixes

- Removed "Projects" link from breadcrumb (was causing broken link)
- Changed settings button to display "Settings" text with gear icon for clarity
- Restored maroon header (#7b2b43) with search functionality

### Generic Branding Changes

Removed all institution-specific references to make software open-source friendly:

- Changed branding from "CULS" to "Geology Lab Software"
- Changed all email addresses from @concord.edu to @university.edu
- Changed sample ID prefix from CULS-2025- to LAB-2025-
- Changed laboratory catalog number prefix from CU- to LAB-
- Changed "CULS Field Team" to "Lab Field Team"
- Updated placeholder text throughout

### Admin Views

Created system-wide admin views for Administrators only:

- **All Samples View**: Shows all samples across all projects with analysis status indicators
- **All Geochemical Analysis View**: System-wide geochemical data with filtering and QC status
- **All Microanalysis View**: Comprehensive microanalysis data with point counts
- **All Physical Analysis View**: All physical analysis data with mass tracking
- **Admin Navigation Menu**: Dropdown in header for quick access (Administrators only)

Features:

- Summary statistics cards for each view
- Filter controls by analysis type, status, analyst
- Export functionality buttons
- Breadcrumb navigation between views
- Links to individual sample detail pages
- QC status badges and color-coded indicators

### Permission Restrictions

- Project settings button now only visible to Administrators and Project Owners
- Admin Views dropdown only visible to Administrators

### Private Project Access Control

Implemented comprehensive access control for private projects:

**Access Logic**:

- Public projects (`is_private: false`) are accessible to everyone
- Private projects (`is_private: true`) require permission:
  - Administrators have access to all projects
  - Project owners have access to their own projects
  - Collaborators listed on the project have access
  - All other users see access request screen

**User Experience**:

- Users with access see project normally
- Users without access see:
  - Blurred background showing project preview
  - Centered access request modal with lock icon
  - Project name and owner information
  - Optional message field to explain access need
  - "Request Access" button to submit request
  - "Back to Projects" button to return home
  - Login prompt for non-authenticated users

**Features**:

- Automatic permission checking on project load
- Visual feedback with blur effect (8px filter)
- Non-interactive blurred content (pointer-events disabled)
- Clean modal design with Bootstrap styling
- Contextual information (project title, owner)

### Bug Fixes (Continued)

- Fixed "Back to Projects" button on Create New Project page (was calling non-existent route)
