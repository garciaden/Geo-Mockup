# Changelog

## 11/13/25 - Final KuehnLab Branding

### Branding Updates

- Changed all branding to "KuehnLab" (singular, no space)
- Updated email addresses to @kuehnlab.edu:
  - app/auth/routes.py (all 5 mock user roles)
  - app/auth/README_MOCK_LOGIN.md (documentation)
  - app/samples/routes.py (_default_email function)
- Updated header navigation to display "KuehnLab"
- Removed all remaining references to:
  - "Geology Lab Software"
  - @concord.edu email addresses
  - @culs.example.edu email addresses

### Documentation Updates

- Updated TODO.md for Django migration planning
- Added Amazon Lightsail deployment focus
- Added pgAdmin database management integration
- Documented all 20 Django models from ENTITY-REFERENCE.md
- Added Tailwind CSS + HTMX frontend migration plan

## 11/10/25 - Changes made by Matthew Kenner

### Homepage Updates

- Added sortable "Last Updated" column with relative time formatting ("2 days ago")
- Added sort button for "Last Updated" (Oldest/Newest)
- Relative time formatter converts dates to human-readable format

### Project View Updates

- Added breadcrumb navigation (Home > Project Name)
- Gear icon for settings button (was already present!)
- Renamed "Sample Name" → "Short Description"
- Added "Laboratory Catalog Number" column (with placeholder data: LAB-2025-001, etc.)

### Sample View Updates

- Changed "Upload Image" → "Upload Files"
- Geochemical Analysis: Converted to collapsible accordion sections
  - Alphabetically sorted (EPMA/SEM, Geochronology, ICP-MS, LA-ICP-MS, Micro XRF, SIMS, Whole XRF)
  - Multiple sections can be open simultaneously (removed data-bs-parent)
  - Shows badge with number of runs per section
- Added Inventory & Sub-samples section with:
  - Table: Fraction ID, Storage Location, Quantity, Unit, Status
  - Placeholder data showing sieve fractions (2-1mm, 1mm-63µm, <63µm)
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
