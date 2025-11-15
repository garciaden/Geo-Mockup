@echo off
REM Django Migration Setup Script for KuehnLab (Windows)
REM Based on Kuehn_Lab_Normalization.md (46 Functional Dependencies)

echo ==================================
echo KuehnLab Django Migration Setup
echo Based on Kuehn_Lab_Normalization
echo 8 Domains - 46 Entities
echo ==================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Django and dependencies...
python -m pip install --upgrade pip
pip install "django>=5.1,<6.0"
pip install psycopg2-binary
pip install python-dotenv
pip install django-extensions
pip install djangorestframework
pip install django-cors-headers
pip install pillow
pip install django-filter

echo Creating Django project structure...
if not exist "django_app" mkdir django_app
cd django_app

REM Create Django project
if not exist "kuehnlab" (
    echo Creating Django project 'kuehnlab'...
    django-admin startproject kuehnlab .
)

REM Create apps directory
if not exist "apps" mkdir apps

REM Make sure we're using the venv python
set PYTHON_CMD=%CD%\..\venv\Scripts\python.exe

REM Create Django apps based on 8 domains from Kuehn_Lab_Normalization.md
echo Creating Django apps for 8 domains...

REM Domain 1: USER & ACCESS (FD1-FD5)
if not exist "apps\accounts" (
    echo [1/8] Creating accounts app (USER, USER_SESSION, PROJECT_USER, PERSON, PERSON_LOG)
    "%PYTHON_CMD%" manage.py startapp accounts apps\accounts
)

REM Domain 2: PROJECT (FD6-FD10)
if not exist "apps\projects" (
    echo [2/8] Creating projects app (PROJECT, GRANT, PROJECT_REQUEST, PROJECT_LOG, PROJECT_SAMPLE_PIVOT)
    "%PYTHON_CMD%" manage.py startapp projects apps\projects
)

REM Domain 3: SAMPLE (FD11-FD15)
if not exist "apps\samples" (
    echo [3/8] Creating samples app (SAMPLE, FLAG, LOCATION_HISTORY, SAMPLE_DISBURSEMENTS, PHYSICAL_SAMPLE_MOVEMENTS)
    "%PYTHON_CMD%" manage.py startapp samples apps\samples
)

REM Domain 4: ANALYSIS (FD16-FD18)
if not exist "apps\analyses" (
    echo [4/8] Creating analyses app (ANALYSIS_SAMPLE_BRIDGE, ANALYSIS, ANALYSIS_INSTRUMENT)
    "%PYTHON_CMD%" manage.py startapp analyses apps\analyses
)

REM Domain 5: PHYSICAL ANALYSIS WORKFLOWS (FD19-FD25)
if not exist "apps\physical_analyses" (
    echo [5/8] Creating physical_analyses app (7 workflows: MACRO, COMPONENTRY, PSD, MAX_CLAST, DENSITY, CORE, CRYPTOTEPHRA)
    "%PYTHON_CMD%" manage.py startapp physical_analyses apps\physical_analyses
)

REM Domain 6: MICROANALYSIS WORKFLOW (FD26-FD30)
if not exist "apps\microanalyses" (
    echo [6/8] Creating microanalyses app (POLARIZING_MICROSCOPE, ELECTRON_IMAGING, TOMOGRAPHY, OTHER_IMAGING, IMAGING_DATA)
    "%PYTHON_CMD%" manage.py startapp microanalyses apps\microanalyses
)

REM Domain 7: GEOCHEMICAL ANALYSIS WORKFLOW (FD31-FD37)
if not exist "apps\geochemical" (
    echo [7/8] Creating geochemical app (GEOCHEM_GENERAL, XRF, ICP_MS, EPMA_SEM, LA_ICP_MS, SIMS, GEOCHRONOLOGY)
    "%PYTHON_CMD%" manage.py startapp geochemical apps\geochemical
)

REM Domain 8: DATA MANAGEMENT (FD38-FD46)
if not exist "apps\data_management" (
    echo [8/8] Creating data_management app (AUDIT_TRAIL, EXPORT, IMPORT, FILE, BATCH, INSTRUMENTS, CALIBRATION)
    "%PYTHON_CMD%" manage.py startapp data_management apps\data_management
)

REM Create directories for templates and static files
if not exist "templates" mkdir templates
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "static\images" mkdir static\images
if not exist "media\uploads" mkdir media\uploads

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    (
        echo # Django Settings
        echo SECRET_KEY=django-insecure-dev-key-change-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # Database Configuration - PostgreSQL
        echo DB_NAME=kuehnlab_db
        echo DB_USER=kuehnlab_user
        echo DB_PASSWORD=
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo.
        echo # CORS Settings
        echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
    ) > .env
)

REM Save installed packages to requirements.txt
"%PYTHON_CMD%" -m pip freeze > requirements.txt

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Django project structure created based on Kuehn_Lab_Normalization.md:
echo.
echo   8 Domains:
echo   1. accounts        - USER ^& ACCESS (5 entities: USER, USER_SESSION, PROJECT_USER, PERSON, PERSON_LOG)
echo   2. projects        - PROJECT (5 entities: PROJECT, GRANT, PROJECT_REQUEST, PROJECT_LOG, PROJECT_SAMPLE_PIVOT)
echo   3. samples         - SAMPLE (5 entities: SAMPLE, FLAG, LOCATION_HISTORY, DISBURSEMENTS, MOVEMENTS)
echo   4. analyses        - ANALYSIS (3 entities: ANALYSIS_SAMPLE_BRIDGE, ANALYSIS, ANALYSIS_INSTRUMENT)
echo   5. physical_analyses - PHYSICAL WORKFLOWS (7 entities: MACRO, COMPONENTRY, PSD, MAX_CLAST, DENSITY, CORE, CRYPTO)
echo   6. microanalyses   - MICROANALYSIS (5 entities: POLARIZING, ELECTRON, TOMOGRAPHY, OTHER, IMAGING_DATA)
echo   7. geochemical     - GEOCHEMICAL (7 entities: GENERAL, XRF, ICP_MS, EPMA_SEM, LA_ICP_MS, SIMS, GEOCHRONOLOGY)
echo   8. data_management - DATA MGMT (9 entities: AUDIT, EXPORT, IMPORT, FILE, BATCH, INSTRUMENTS, CALIBRATION)
echo.
echo   Total: 46 entities (FD1-FD46)
echo.
echo Next steps:
echo 1. Update kuehnlab\settings.py with configuration from DJANGO_MIGRATION_GUIDE.md
echo 2. Create database models in apps\*\models.py (see KUEHNLAB_DJANGO_MODELS.md)
echo 3. Run: python manage.py makemigrations
echo 4. Run: python manage.py migrate
echo 5. Create superuser: python manage.py createsuperuser
echo 6. Run development server: python manage.py runserver
echo.
echo See DJANGO_MIGRATION_GUIDE.md for detailed instructions

pause
