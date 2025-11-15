#!/bin/bash
# Django Migration Setup Script for KuehnLab (Linux/Mac)
# Based on Kuehn_Lab_Normalization.md (46 Functional Dependencies)

set -e  # Exit on error

echo "=================================="
echo "KuehnLab Django Migration Setup"
echo "Based on Kuehn_Lab_Normalization"
echo "8 Domains - 46 Entities"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Django and dependencies..."
pip install --upgrade pip
pip install "django>=5.1,<6.0"
pip install psycopg2-binary
pip install python-dotenv
pip install django-extensions
pip install djangorestframework
pip install django-cors-headers
pip install pillow
pip install django-filter

echo "Creating Django project structure..."
mkdir -p django_app
cd django_app

# Create Django project
if [ ! -d "kuehnlab" ]; then
    echo "Creating Django project 'kuehnlab'..."
    django-admin startproject kuehnlab .
fi

# Create apps directory
mkdir -p apps

# Create Django apps based on 8 domains from Kuehn_Lab_Normalization.md
echo "Creating Django apps for 8 domains..."

# Domain 1: USER & ACCESS (FD1-FD5)
if [ ! -d "apps/accounts" ]; then
    echo "[1/8] Creating accounts app (USER, USER_SESSION, PROJECT_USER, PERSON, PERSON_LOG)"
    python manage.py startapp accounts apps/accounts
fi

# Domain 2: PROJECT (FD6-FD10)
if [ ! -d "apps/projects" ]; then
    echo "[2/8] Creating projects app (PROJECT, GRANT, PROJECT_REQUEST, PROJECT_LOG, PROJECT_SAMPLE_PIVOT)"
    python manage.py startapp projects apps/projects
fi

# Domain 3: SAMPLE (FD11-FD15)
if [ ! -d "apps/samples" ]; then
    echo "[3/8] Creating samples app (SAMPLE, FLAG, LOCATION_HISTORY, SAMPLE_DISBURSEMENTS, PHYSICAL_SAMPLE_MOVEMENTS)"
    python manage.py startapp samples apps/samples
fi

# Domain 4: ANALYSIS (FD16-FD18)
if [ ! -d "apps/analyses" ]; then
    echo "[4/8] Creating analyses app (ANALYSIS_SAMPLE_BRIDGE, ANALYSIS, ANALYSIS_INSTRUMENT)"
    python manage.py startapp analyses apps/analyses
fi

# Domain 5: PHYSICAL ANALYSIS WORKFLOWS (FD19-FD25)
if [ ! -d "apps/physical_analyses" ]; then
    echo "[5/8] Creating physical_analyses app (7 workflows: MACRO, COMPONENTRY, PSD, MAX_CLAST, DENSITY, CORE, CRYPTOTEPHRA)"
    python manage.py startapp physical_analyses apps/physical_analyses
fi

# Domain 6: MICROANALYSIS WORKFLOW (FD26-FD30)
if [ ! -d "apps/microanalyses" ]; then
    echo "[6/8] Creating microanalyses app (POLARIZING_MICROSCOPE, ELECTRON_IMAGING, TOMOGRAPHY, OTHER_IMAGING, IMAGING_DATA)"
    python manage.py startapp microanalyses apps/microanalyses
fi

# Domain 7: GEOCHEMICAL ANALYSIS WORKFLOW (FD31-FD37)
if [ ! -d "apps/geochemical" ]; then
    echo "[7/8] Creating geochemical app (GEOCHEM_GENERAL, XRF, ICP_MS, EPMA_SEM, LA_ICP_MS, SIMS, GEOCHRONOLOGY)"
    python manage.py startapp geochemical apps/geochemical
fi

# Domain 8: DATA MANAGEMENT (FD38-FD46)
if [ ! -d "apps/data_management" ]; then
    echo "[8/8] Creating data_management app (AUDIT_TRAIL, EXPORT, IMPORT, FILE, BATCH, INSTRUMENTS, CALIBRATION)"
    python manage.py startapp data_management apps/data_management
fi

# Create directories for templates and static files
mkdir -p templates
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
mkdir -p media/uploads

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# Django Settings
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=kuehnlab_db
DB_USER=kuehnlab_user
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOL
fi

# Save installed packages to requirements.txt
pip freeze > requirements.txt

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Django project structure created based on Kuehn_Lab_Normalization.md:"
echo ""
echo "  8 Domains:"
echo "  1. accounts        - USER & ACCESS (5 entities: USER, USER_SESSION, PROJECT_USER, PERSON, PERSON_LOG)"
echo "  2. projects        - PROJECT (5 entities: PROJECT, GRANT, PROJECT_REQUEST, PROJECT_LOG, PROJECT_SAMPLE_PIVOT)"
echo "  3. samples         - SAMPLE (5 entities: SAMPLE, FLAG, LOCATION_HISTORY, DISBURSEMENTS, MOVEMENTS)"
echo "  4. analyses        - ANALYSIS (3 entities: ANALYSIS_SAMPLE_BRIDGE, ANALYSIS, ANALYSIS_INSTRUMENT)"
echo "  5. physical_analyses - PHYSICAL WORKFLOWS (7 entities: MACRO, COMPONENTRY, PSD, MAX_CLAST, DENSITY, CORE, CRYPTO)"
echo "  6. microanalyses   - MICROANALYSIS (5 entities: POLARIZING, ELECTRON, TOMOGRAPHY, OTHER, IMAGING_DATA)"
echo "  7. geochemical     - GEOCHEMICAL (7 entities: GENERAL, XRF, ICP_MS, EPMA_SEM, LA_ICP_MS, SIMS, GEOCHRONOLOGY)"
echo "  8. data_management - DATA MGMT (9 entities: AUDIT, EXPORT, IMPORT, FILE, BATCH, INSTRUMENTS, CALIBRATION)"
echo ""
echo "  Total: 46 entities (FD1-FD46)"
echo ""
echo "Next steps:"
echo "1. Update kuehnlab/settings.py with configuration from DJANGO_MIGRATION_GUIDE.md"
echo "2. Create database models in apps/*/models.py (see KUEHNLAB_DJANGO_MODELS.md)"
echo "3. Run: python manage.py makemigrations"
echo "4. Run: python manage.py migrate"
echo "5. Create superuser: python manage.py createsuperuser"
echo "6. Run development server: python manage.py runserver"
echo ""
echo "See DJANGO_MIGRATION_GUIDE.md for detailed instructions"
