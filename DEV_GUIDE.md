# Development Guide

## Daily Workflow

### Quick Start (2 Minutes)

**From HOST terminal (WSL/Windows)**:

```bash
cd "[Folder where Mockup Clone lives on your machine]""

# Start database
docker compose up postgres -d

# Open VS Code and reopen in container
code .
# Click "Reopen in Container" when prompted

# In VS Code terminal (inside devcontainer)
python3 myapp.py
```

**Access**: http://localhost:5000

---

## VS Code Shortcuts

### Run Flask App

- **Ctrl+Shift+B** - Runs Flask automatically
- **F5** - Run with debugger
- **Terminal**: `python3 myapp.py`

### VS Code Tasks (Ctrl+Shift+P  "Run Task")

- **Start Flask Development Server** - Launch Flask
- **Check Database Connection** - Test DB connectivity
- **Install Python Dependencies** - Update packages
- **View Database Tables** - List all tables

---

## Database Management

### Check Database Status

```bash
# From HOST terminal
docker ps | grep postgres
# Should show: culs_postgres

# View database tables
docker exec -it culs_postgres psql -U culs_user -d culs_db -c "\dt culs.*"
# Should show 33 tables
```

### Database Commands

```bash
# Access database shell
docker exec -it culs_postgres psql -U culs_user -d culs_db

# View logs
docker logs culs_postgres

# Restart database
docker compose restart postgres

# Stop database
docker compose stop postgres

# Remove database (deletes all data!)
docker compose down postgres -v
```

### Backup and Restore

```bash
# Create backup
docker exec culs_postgres pg_dump -U culs_user culs_db > backup_$(date +%Y%m%d).sql

# Restore backup
cat backup_20251111.sql | docker exec -i culs_postgres psql -U culs_user -d culs_db
```

---

## Stopping Services

### Stop Flask

Press **Ctrl+C** in VS Code terminal

### Stop Database (Optional)

```bash
# From HOST terminal
cd "/mnt/c/Users/Matthew/OneDrive - The University of Colorado Denver/School/Courses/CULS-Data/CULS-Mockup"
docker compose stop postgres
# OR
./stop-dev.sh
```

**Tip**: Leave database running between sessions for faster startup

---

## Troubleshooting

### "Connection refused" - Database not running

```bash
docker compose up postgres -d
sleep 10
python3 myapp.py
```

### "Port 5432 in use" - Another PostgreSQL running

```bash
sudo lsof -i :5432  # Find what's using the port
# Stop conflicting service or change port in docker-compose.yml
```

### Flask won't start - Missing dependencies

```bash
pip install -r requirements.txt
```

### Can't see database - Not initialized

```bash
docker compose down postgres -v
docker compose up postgres -d
sleep 30  # Wait for initialization
```

### Tables not created

```bash
# Check logs for errors
docker logs culs_postgres | grep ERROR

# Manually run initialization
docker exec -it culs_postgres psql -U culs_user -d culs_db -f /docker-entrypoint-initdb.d/99_run_all.sql
```

### VS Code Dev Container won't start

```bash
# In VS Code: Ctrl+Shift+P  "Dev Containers: Rebuild Container"

# Or rebuild from command line
docker compose down
docker compose build labmanager
docker compose up
```

---

## Access Points

| Service        | URL/Command                                                    | Where         |
| -------------- | -------------------------------------------------------------- | ------------- |
| Flask App      | http://localhost:5000                                          | Browser       |
| Database Shell | `docker exec -it culs_postgres psql -U culs_user -d culs_db` | Host terminal |
| Database Logs  | `docker logs culs_postgres`                                  | Host terminal |
| Flask Logs     | VS Code terminal                                               | Dev container |

---

## Database Structure

### Schemas

- **culs** - Main application schema (33 tables)
- **audit** - Audit logging
- **files** - File asset management

### Key Table Groups

**User & Authentication (7 tables)**:

- `user`, `user_status`, `user_session`, `session_status`
- `person`, `system_role`
- Session tracking with IP address and user agent

**Organization & Contacts (7 tables)**:

- `organization`, `organization_type`, `country`
- `contact`, `contact_type`
- `person_identifier`, `identifier_type`

**Projects & Funding (4 tables)**:

- `project`, `project_user`, `project_sample_bridge`
- `fund`, `project_fund`

**Samples & Storage (2 tables)**:

- `sample` (with PostGIS geography)
- `storage_location`

**Analysis & Calibration (8 tables)**:

- `batch`, `instrument`, `instrument_calibration`
- `reference_material`, `calibration_measurement`
- `material_type`, `material_source`, `analyte`, `unit`
- `analysis`, `physical_analysis`, `geochem_analysis`, `imaging_analysis`

**Files (4 tables)**:

- `file_asset`, `project_file`, `sample_file`, `analysis_file`

---

## Configuration

### Environment Setup (One-Time)

**Already configured**:

- `.env` file created from `example.env`
- `DATABASE_URL` set to localhost
- PostgreSQL service in `docker-compose.yml`
- Database libraries in `requirements.txt`

### Environment Variables

```bash
# Application
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1

# Database (Local - Flask in devcontainer)
DATABASE_URL=postgresql://culs_user:development_password@localhost:5432/culs_db
DB_PASSWORD=development_password
```

---

## Helper Scripts

### Start Development Environment

```bash
./start-dev.sh
```

Starts PostgreSQL and provides instructions for VS Code.

### Stop Development Environment

```bash
./stop-dev.sh
```

Stops PostgreSQL gracefully.

---

## Success Checklist

Before starting development each day:

- [ ] PostgreSQL container running (`docker ps`)
- [ ] VS Code opened in devcontainer
- [ ] Flask starts without errors (`python3 myapp.py`)
- [ ] Can access http://localhost:5000
- [ ] Database has 33 tables (check with `\dt culs.*`)

---

## Typical Development Session

```bash
# 1. Start database (HOST terminal - ONE TIME)
./start-dev.sh

# 2. Open VS Code
code .
# Click "Reopen in Container"

# 3. Start Flask (VS Code terminal)
python3 myapp.py

# 4. Develop! Restart Flask as needed (Ctrl+C, then python3 myapp.py)

# 5. End of day - Stop Flask (Ctrl+C)
# Optional: Stop database
./stop-dev.sh
```

---

## Next Steps

### Immediate

1. Create SQLAlchemy ORM models for all 33 tables
2. Replace mock data with database queries
3. Implement user authentication with database
4. Add file upload functionality

### Phase 2 (Django Migration)

See `TASK_ASSIGNMENTS.md` for detailed migration plan:

- Convert Flask blueprints to Django apps
- Migrate to Django ORM
- Implement Django REST Framework API
- Switch from Bootstrap to Tailwind CSS
- Add HTMX for dynamic interactions

---

## Documentation References

- **Database Schema**: `Database/README.md`
- **Schema Comparison**: `SCHEMA_COMPARISON.md`
- **Task Assignments**: `TASK_ASSIGNMENTS.md`
- **TODO List**: `TODO.md`
- **Changelog**: `CHANGELOG.md`
- **Mock Login**: `app/auth/README_MOCK_LOGIN.md`

---

**Your development environment is ready!**

Database running  Flask ready â http://localhost:5000 is live
