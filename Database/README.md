
---

# CULS Database Setup Scripts

PostgreSQL database schema for  **Concord University Laboratory Software (CULS)** .

Based on: ER diagram and normalization

---

## File Organization

```
Database/
├── 00_init.sql                      # Database initialization and extensions
├── 01_people_and_access.sql         # PERSON, SYSTEM_ROLE, USER
├── 02_projects_and_membership.sql   # PROJECT, PROJECT_USER
├── 03_funding.sql                   # FUND, PROJECT_FUND
├── 04_storage.sql                   # STORAGE_LOCATION
├── 05_samples.sql                   # SAMPLE
├── 06_batches_and_instruments.sql   # BATCH, INSTRUMENT, INSTRUMENT_CALIBRATION
├── 07_analysis.sql                  # ANALYSIS, PHYSICAL_ANALYSIS, GEOCHEM_ANALYSIS, IMAGING_ANALYSIS
├── 08_files.sql                     # FILE_ASSET, PROJECT_FILE, SAMPLE_FILE, ANALYSIS_FILE
├── 09_audit_and_requests.sql        # AUDIT_LOG, EXPORT_REQUEST, PROJECT_TRANSFER
├── 99_run_all.sql                   # Master script (runs all in order)
├── 99_drop_all.sql                  # Cleanup script (drops all objects)
└── README.md                        # This file
```

---

## Quick Start

### Prerequisites

* PostgreSQL **13+**
* **PostGIS** extension
* Database superuser access (initial setup)

---

### Option 1: Run All Scripts at Once

```bash
# Create database
createdb culs_db

# Run all DDL scripts in order
psql -U postgres -d culs_db -f 99_run_all.sql
```

---

### Option 2: Run Scripts Individually

```bash
# 1. Create database
createdb culs_db

# 2. Connect to database
psql -U postgres -d culs_db

# 3. Run each script in order
\i 00_init.sql
\i 01_people_and_access.sql
\i 02_projects_and_membership.sql
\i 03_funding.sql
\i 04_storage.sql
\i 05_samples.sql
\i 06_batches_and_instruments.sql
\i 07_analysis.sql
\i 08_files.sql
\i 09_audit_and_requests.sql
```

---

### Clean Up / Reset Database

```bash
# WARNING: This deletes ALL data!
psql -U postgres -d culs_db -f 99_drop_all.sql
```

---

## Database Structure

### Schemas

* **`culs`** – Main application data (projects, samples, analyses)
* **`audit`** – Audit logging and compliance
* **`files`** – File and asset management

---

## Key Tables (20 total)

### Core Management (4 tables)

* `person` – People (names, ORCID, affiliations)
* `system_role` – System-level roles (Admin, Owner, etc.)
* `user` – User accounts + authentication info
* `project_user` – Project-level membership & roles

---

### Projects & Funding (4 tables)

* `project` – Research project metadata
* `fund` – Funding sources
* `project_fund` – Linking projects ↔ funding

---

### Samples & Storage (2 tables)

* `storage_location` – Physical storage locations
* `sample` – Sample metadata + geographic coordinates

---

### Analysis (7 tables)

* `batch`
* `instrument`
* `instrument_calibration`
* `analysis` – Parent analysis record
* `physical_analysis`
* `geochem_analysis`
* `imaging_analysis`

Supports  **polymorphic workflows** .

---

### Files (4 tables)

* `file_asset` – File metadata
* `project_file` – Files ↔ Projects
* `sample_file` – Files ↔ Samples
* `analysis_file` – Files ↔ Analyses

---

### Audit & Requests (3 tables)

* `audit_log`
* `export_request`
* `project_transfer`

---

## Key Features

### Geographic Data (PostGIS)

* Coordinates stored using **geometry(Point, 4326)**
* Fast spatial queries using **GIST indexes**
* Automatic lat/lon → geometry conversion triggers included

---

### Audit Logging

* Immutable audit log (insert-only)
* Stores:
  * user ID
  * timestamp
  * table name
  * primary key
  * old values
  * new values
* Fully JSON-based change tracking

---

### File Management

* SHA256 checksum verification
* S3/folder storage supported
* File “purpose” classification ENUMs
* Automated thumbnail/preview workflows (optional)

---

### Analysis Workflows

* Parent → specialized table pattern
* Supports **18 workflow branches**
* Branch validation enforced via triggers

---

## Custom Types (ENUMs)

* `user_status` — active, locked, disabled, pending
* `visibility_level` — public, restricted, hidden
* `project_status` — active, archived
* `sample_status` — drafted, ingested, curated, retired
* `qc_status` — pending, pass, fail, partial
* `analysis_type` — physical, geochem, imaging
* `analysis_status` — pending, processing, complete, failed
* `instrument_status` — active, maintenance, retired
* `file_purpose_*` — purpose classifications
* `audit_action` — insert, update, delete, export, transfer
* `export_format` — csv, xlsx, json, netcdf, zip
* `export_status` — pending, processing, done, failed
* `transfer_status` — pending, approved, rejected

---

## Indexes

### Performance Indexes

* B-tree indexes on all FKs, timestamps, and ENUMs
* GIN for JSONB fields
* Full-text search (GIN) on names, descriptions
* GIST for spatial queries (PostGIS)

### Unique Constraints

* ORCID
* Email + username
* Instrument serial number
* Grant/fund codes
* `(project_id, sample_code)` composite uniqueness

---

## Security Features

### Data Integrity

* Full FK graph
* Proper `ON DELETE CASCADE` vs `RESTRICT` usage
* CHECK constraints for validation
* Branch integrity enforced with triggers

### Audit Protection

* `audit_log` is **write-only**
* Updates/deletes prevented via triggers
* User attribution included in every row

---

## Sample Data

```sql
-- Example: system roles seeded in 01_people_and_access.sql
SELECT * FROM culs.system_role;
```

---

## Additional Documentation

* **`OVERALL_DESIGN.mmd`** — Mermaid ERD
* **`ENTITY-REFERENCE.md`** — Full entity dictionary
* **`requirements.md`** — SRS requirements

---

## Important Notes

1. Required extensions: `postgis`, `uuid-ossp`, `pgcrypto`
2. Audit log is permanent and cannot be modified
3. Be cautious with CASCADE operations
4. For large deployments: partition `audit_log` monthly
5. Always back up before running `99_drop_all.sql`

---

## Support

For issues or questions:

* `/Design_Documents/`
* `requirements.md` (SRS)
* `/Team_Meetings/` notes

---

**Version:** 1.0

**Last Updated:** 2025-01-09

**Based on:** `OVERALL_DESIGN.mmd` ERD

---

If you want, I can also:

✅ Convert this into a **GitHub Wiki page**

✅ Generate a  **runbook** ,  **setup automation** , or **Makefile**

✅ Build a **Dockerized database + seed environment**

Just let me know.
