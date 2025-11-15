# Django Migration Guide - Flask to Django

**Project**: KuehnLab Laboratory Information Management System
**Current Stack**: Flask + Bootstrap + Mock Data
**Target Stack**: Django + PostgreSQL + Tailwind CSS + HTMX
**Date**: 2025-11-13

---

## Table of Contents

1. [Why Django?](#why-django)
2. [Migration Strategy](#migration-strategy)
3. [Project Structure Comparison](#project-structure-comparison)
4. [Step-by-Step Migration](#step-by-step-migration)
5. [Models Migration](#models-migration)
6. [Views Migration](#views-migration)
7. [Templates Migration](#templates-migration)
8. [URL Routing Migration](#url-routing-migration)
9. [Static Files & Assets](#static-files--assets)
10. [Testing Strategy](#testing-strategy)
11. [Deployment Considerations](#deployment-considerations)

---

## Why Django?

### Advantages Over Flask

1. **Built-in ORM** - Powerful database abstraction layer
   - Automatic migrations
   - Query optimization
   - Relationship management
   - Support for complex queries

2. **Admin Interface** - Out-of-the-box administration
   - Automatic CRUD operations
   - Customizable interface
   - User management
   - Audit logging

3. **Authentication System** - Robust user management
   - User model with permissions
   - Group-based permissions
   - Password hashing (PBKDF2)
   - Session management
   - Password reset flows

4. **Security Features** - Production-ready security
   - CSRF protection
   - XSS protection
   - SQL injection protection
   - Clickjacking protection
   - Secure cookie handling

5. **Django REST Framework** - Powerful API development
   - Serialization
   - Authentication/Permissions
   - ViewSets and Routers
   - Browsable API
   - OpenAPI documentation

6. **Scalability** - Better for growing applications
   - Connection pooling
   - Query optimization
   - Caching framework
   - Middleware system

7. **Ecosystem** - Large community and packages
   - Django Debug Toolbar
   - Django Extensions
   - Celery integration
   - Third-party packages

---

## Migration Strategy

### Phased Approach (Recommended)

**Phase 1: Foundation** (Week 1-2)
- Set up Django project structure
- Configure PostgreSQL database
- Create Django models (all 46 entities across 8 domains)
- Set up Django admin interface

**Phase 2: Core Features** (Week 3-4)
- Migrate authentication system
- Convert project management views
- Convert sample management views
- Implement basic CRUD operations

**Phase 3: Frontend** (Week 5-6)
- Migrate templates to Django template language
- Convert Bootstrap to Tailwind CSS
- Implement HTMX for dynamic interactions
- Update static files structure

**Phase 4: Advanced Features** (Week 7-8)
- Analysis workflow views (18 branches)
- File upload system
- Export functionality
- Permission system refinement

**Phase 5: Testing & Polish** (Week 9-10)
- Unit tests for models
- Integration tests for views
- API endpoint tests
- Security testing
- Performance optimization

**Phase 6: Deployment** (Week 11-12)
- Set up Gunicorn + Nginx
- Configure for Lightsail
- Database migration scripts
- CI/CD pipeline
- Monitoring and logging

---

## Project Structure Comparison

### Current Flask Structure

```
CULS-Mockup/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── auth/                 # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/
│   ├── main/                 # Main blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── projects/             # Projects blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── samples/              # Samples blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── static/               # Static files
│   └── templates/            # Base templates
├── config.py                 # Configuration
├── myapp.py                  # Entry point
└── requirements.txt          # Dependencies
```

### Target Django Structure

```
kuehnlab/                     # Project root
├── manage.py                 # Django management script
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
│
├── kuehnlab/                 # Project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application (future)
│
├── apps/                     # Django applications (8 domains per Kuehn_Lab_Normalization.md)
│   │
│   ├── accounts/             # Domain 1: USER & ACCESS (FD1-FD5)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py         # USER, USER_SESSION, PROJECT_USER, PERSON, PERSON_LOG
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   └── templates/
│   │       └── accounts/
│   │
│   ├── projects/             # Domain 2: PROJECT (FD6-FD10)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py         # PROJECT, GRANT, PROJECT_REQUEST, PROJECT_LOG, PROJECT_SAMPLE_PIVOT
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── serializers.py    # DRF serializers
│   │   ├── admin.py
│   │   └── templates/
│   │       └── projects/
│   │
│   ├── samples/              # Domain 3: SAMPLE (FD11-FD15)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py         # SAMPLE, FLAG, LOCATION_HISTORY, SAMPLE_DISBURSEMENTS, PHYSICAL_SAMPLE_MOVEMENTS
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   ├── admin.py
│   │   └── templates/
│   │       └── samples/
│   │
│   ├── analyses/             # Domain 4: ANALYSIS (FD16-FD18)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py         # ANALYSIS_SAMPLE_BRIDGE, ANALYSIS, ANALYSIS_INSTRUMENT
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   ├── admin.py
│   │   └── templates/
│   │       └── analyses/
│   │
│   ├── physical_analyses/    # Domain 5: PHYSICAL WORKFLOWS (FD19-FD25)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py         # MACRO, COMPONENTRY, PSD, MAX_CLAST, DENSITY, CORE, CRYPTOTEPHRA
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/
│   │
│   ├── microanalyses/        # Domain 6: MICROANALYSIS (FD26-FD30)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py         # POLARIZING_MICROSCOPE, ELECTRON_IMAGING, TOMOGRAPHY, OTHER_IMAGING, IMAGING_DATA
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/
│   │
│   ├── geochemical/          # Domain 7: GEOCHEMICAL (FD31-FD37)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py         # GEOCHEM_GENERAL, XRF, ICP_MS, EPMA_SEM, LA_ICP_MS, SIMS, GEOCHRONOLOGY
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/
│   │
│   └── data_management/      # Domain 8: DATA MGMT (FD38-FD46)
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py         # AUDIT_TRAIL, EXPORT_HISTORY, EXPORT_REQUESTS, IMPORT_JOBS, FILE, BATCH, INSTRUMENTS, CALIBRATION_DATA, CALIBRATION_MEASUREMENT
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       └── templates/
│
├── static/                   # Static files (Tailwind CSS, JS)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                    # User uploads
│   └── uploads/
│
└── templates/                # Base templates
    ├── base.html
    ├── _navbar.html
    └── _footer.html
```

---

## Step-by-Step Migration

### Step 1: Initialize Django Project

```bash
# Create project directory
cd CULS-Mockup
mkdir django_app
cd django_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install Django and dependencies (latest stable 5.x)
pip install "django>=5.1,<6.0"
pip install psycopg2-binary  # PostgreSQL adapter
pip install python-dotenv
pip install django-extensions
pip install djangorestframework
pip install django-cors-headers
pip install pillow  # For image handling
pip install django-filter

# Create Django project
django-admin startproject kuehnlab .

# Create apps
python manage.py startapp core apps/core
python manage.py startapp accounts apps/accounts
python manage.py startapp projects apps/projects
python manage.py startapp samples apps/samples
python manage.py startapp analyses apps/analyses
python manage.py startapp people apps/people
python manage.py startapp data_management apps/data_management
```

### Step 2: Configure Django Settings

**File**: `kuehnlab/settings.py`

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # For PostGIS (geographic data)

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_extensions',

    # Local apps
    'apps.core',
    'apps.accounts',
    'apps.projects',
    'apps.samples',
    'apps.analyses',
    'apps.people',
    'apps.data_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kuehnlab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'kuehnlab_db'),
        'USER': os.getenv('DB_USER', 'kuehnlab_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

# CORS settings (for API)
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# Session settings
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG  # True in production
```

### Step 3: Create Custom User Model

**File**: `apps/accounts/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """Custom User model with KuehnLab-specific fields"""

    ROLE_CHOICES = [
        ('Administrator', 'Administrator'),
        ('Project_Owner', 'Project Owner'),
        ('Collaborator', 'Collaborator'),
        ('View_Export', 'View & Export'),
        ('View_Only', 'View Only'),
    ]

    ACCOUNT_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Deceased', 'Deceased'),
    ]

    # Primary Key
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Override username to make it UUID-based
    username = models.CharField(max_length=150, unique=True)

    # KuehnLab-specific fields
    orcid = models.CharField(
        max_length=19,
        unique=True,
        null=True,
        blank=True,
        help_text="ORCID identifier (XXXX-XXXX-XXXX-XXXX)"
    )
    affiliation = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='View_Only')
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='Active')

    # Succession planning
    designated_successor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='successors',
        help_text="User to inherit projects"
    )
    auto_transfer_enabled = models.BooleanField(default=False)
    auto_transfer_delay_days = models.IntegerField(default=30, help_text="Days before auto-transfer (0-365)")

    # Emergency contact (JSON field)
    emergency_contact = models.JSONField(null=True, blank=True)

    # Activity tracking
    last_activity_date = models.DateTimeField(null=True, blank=True)
    session_timeout = models.IntegerField(default=30, help_text="Session timeout in minutes")

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.username} ({self.role})"

    def save(self, *args, **kwargs):
        # Validate designated_successor is not self
        if self.designated_successor and self.designated_successor.user_id == self.user_id:
            raise ValueError("Designated successor cannot be self")
        super().save(*args, **kwargs)

    # Permission helper methods
    def can_create_projects(self):
        return self.role in ['Administrator', 'Project_Owner']

    def can_edit_samples(self):
        return self.role in ['Administrator', 'Project_Owner', 'Collaborator']

    def can_manage_analysis(self):
        return self.role in ['Administrator', 'Project_Owner', 'Collaborator']

    def can_export_data(self):
        return self.role in ['Administrator', 'Project_Owner', 'View_Export']

    def can_flag_samples(self):
        return self.role in ['Administrator', 'Project_Owner', 'Collaborator']

    def can_create_subsample(self):
        return self.role in ['Administrator', 'Project_Owner', 'Collaborator']
```

### Step 4: Create Project Models

**File**: `apps/projects/models.py`

```python
from django.db import models
from django.conf import settings
import uuid

class Project(models.Model):
    """Project management model"""

    VISIBILITY_CHOICES = [
        ('Public', 'Public (metadata only)'),
        ('Private', 'Private (restricted)'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Archived', 'Archived'),
        ('Pending_Transfer', 'Pending Transfer'),
        ('Transferred', 'Transferred'),
        ('Deleted', 'Deleted'),
    ]

    # Primary Key
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    project_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    # Visibility & Status
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='Private')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')

    # Ownership
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_projects'
    )

    # Funding Information
    funding_source = models.CharField(max_length=255, null=True, blank=True)
    grant_id = models.CharField(max_length=100, null=True, blank=True)

    # Related URLs (JSON field)
    related_urls = models.JSONField(null=True, blank=True)

    # Flags
    is_temporary = models.BooleanField(default=False)

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-last_modified']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['visibility']),
        ]

    def __str__(self):
        return f"{self.project_name} ({self.owner.username})"

    def save(self, *args, **kwargs):
        # Validate temporary projects cannot be public
        if self.is_temporary and self.visibility == 'Public':
            raise ValueError("Temporary projects cannot have Public visibility")
        super().save(*args, **kwargs)


class ProjectCollaborator(models.Model):
    """Project collaborator junction table"""

    ROLE_CHOICES = [
        ('Owner', 'Owner'),
        ('Co_Owner', 'Co-Owner'),
        ('Collaborator', 'Collaborator'),
        ('View_Export', 'View & Export'),
        ('View_Only', 'View Only'),
    ]

    # Primary Key
    collaboration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collaborations')

    # Role & Permissions
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    permissions = models.JSONField(null=True, blank=True, help_text="Granular permissions configuration")

    # Succession Planning
    is_successor_designate = models.BooleanField(default=False)

    # Metadata
    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='collaborators_added'
    )

    class Meta:
        db_table = 'project_collaborators'
        unique_together = [['project', 'user']]
        indexes = [
            models.Index(fields=['user', 'role']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name} ({self.role})"


class ProjectTransfer(models.Model):
    """Project ownership transfer tracking"""

    TRANSFER_TYPE_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
        ('Emergency', 'Emergency'),
        ('Succession', 'Succession'),
    ]

    TRANSFER_REASON_CHOICES = [
        ('Retirement', 'Retirement'),
        ('Medical_Leave', 'Medical Leave'),
        ('Death', 'Death'),
        ('Lab_Closure', 'Lab Closure'),
        ('Voluntary', 'Voluntary'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    # Primary Key
    transfer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='transfers')
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='transfers_from'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='transfers_to'
    )

    # Transfer Details
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE_CHOICES)
    transfer_reason = models.CharField(max_length=50, choices=TRANSFER_REASON_CHOICES)
    transfer_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Approval
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transfers_approved'
    )

    # Notes & Metadata
    notes = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    transfer_metadata = models.JSONField(null=True, blank=True)

    # Notification
    notification_sent = models.BooleanField(default=False)

    # Timestamps
    initiated_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'project_transfers'
        ordering = ['-initiated_date']
        indexes = [
            models.Index(fields=['project', 'transfer_status']),
            models.Index(fields=['from_user']),
            models.Index(fields=['to_user']),
        ]

    def __str__(self):
        to_user = self.to_user.username if self.to_user else 'TBD'
        return f"Transfer: {self.project.project_name} ({self.from_user.username} → {to_user})"
```

### Step 5: Create Sample Models

**File**: `apps/samples/models.py`

```python
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings
import uuid

class Sample(gis_models.Model):
    """Sample management model with geographic support"""

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Archived', 'Archived'),
        ('Lost', 'Lost'),
        ('Missing', 'Missing'),
        ('Under_Review', 'Under Review'),
        ('Deleted', 'Deleted'),
    ]

    STATE_CHOICES = [
        ('Raw', 'Raw'),
        ('Processed', 'Processed'),
    ]

    # Primary Key
    sample_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    sample_name = models.CharField(max_length=255)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.PROTECT,
        related_name='samples'
    )

    # IGSN (International Geo Sample Number)
    igsn = models.CharField(max_length=50, unique=True, null=True, blank=True)

    # Collection Information
    collection_date = models.DateField(null=True, blank=True)
    collection_location = gis_models.PointField(null=True, blank=True)  # PostGIS

    # Sample Details
    sample_type = models.CharField(max_length=100, null=True, blank=True)
    storage_location = models.CharField(max_length=255, null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    sample_state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Raw')

    # Parent-Child Relationship (for splits/processing)
    parent_sample = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_samples'
    )

    # Quantity
    remaining_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    quantity_unit = models.CharField(max_length=20, null=True, blank=True)

    # Metadata (JSON fields)
    metadata = models.JSONField(null=True, blank=True, help_text="Full sample metadata")
    public_metadata = models.JSONField(null=True, blank=True, help_text="Public-facing metadata subset")

    # Flagging
    flagged = models.BooleanField(default=False)
    flag_reason = models.TextField(null=True, blank=True)

    # Audit Fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='samples_created'
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='samples_deleted'
    )

    # Version Control
    version = models.IntegerField(default=1)

    # Soft Delete
    is_deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'samples'
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['igsn']),
            models.Index(fields=['flagged']),
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return f"{self.sample_name} ({self.project.project_name})"

    def save(self, *args, **kwargs):
        # Validate processed samples must have parent
        if self.sample_state == 'Processed' and not self.parent_sample:
            raise ValueError("Processed samples must have a parent sample")
        # Validate remaining quantity >= 0
        if self.remaining_quantity is not None and self.remaining_quantity < 0:
            raise ValueError("Remaining quantity cannot be negative")
        super().save(*args, **kwargs)


class SampleDisbursement(models.Model):
    """Sample splitting and distribution tracking"""

    # Primary Key
    disbursement_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships
    parent_sample = models.ForeignKey(
        Sample,
        on_delete=models.CASCADE,
        related_name='disbursements_from'
    )
    child_sample = models.ForeignKey(
        Sample,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disbursements_to'
    )

    # Recipient Information
    recipient_name = models.CharField(max_length=255)
    recipient_institution = models.CharField(max_length=255, null=True, blank=True)
    recipient_email = models.EmailField(null=True, blank=True)

    # Disbursement Details
    quantity_disbursed = models.DecimalField(max_digits=10, decimal_places=4)
    quantity_unit = models.CharField(max_length=20)
    disbursement_date = models.DateField()

    # Purpose & Notes
    purpose = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # Authorization
    authorized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='disbursements_authorized'
    )

    class Meta:
        db_table = 'sample_disbursements'
        ordering = ['-disbursement_date']
        indexes = [
            models.Index(fields=['parent_sample', 'disbursement_date']),
        ]

    def __str__(self):
        return f"{self.parent_sample.sample_name} → {self.recipient_name} ({self.quantity_disbursed} {self.quantity_unit})"
```

---

## Models Migration

### Complete Models List (46 entities)

Based on `Kuehn_Lab_Normalization.md`, here are all models to implement across 8 domains:

#### Domain 1: USER & ACCESS (5 models - FD1-FD5)
1. **User** - `apps/accounts/models.py` (FD1)
2. **UserSession** - `apps/accounts/models.py` (FD2)
3. **ProjectUser** - `apps/accounts/models.py` (FD3)
4. **Person** - `apps/accounts/models.py` (FD4)
5. **PersonLog** - `apps/accounts/models.py` (FD5)

#### Domain 2: PROJECT (5 models - FD6-FD10)
6. **Project** - `apps/projects/models.py` (FD6)
7. **Grant** - `apps/projects/models.py` (FD7)
8. **ProjectRequest** - `apps/projects/models.py` (FD8)
9. **ProjectLog** - `apps/projects/models.py` (FD9)
10. **ProjectSamplePivot** - `apps/projects/models.py` (FD10)

#### Domain 3: SAMPLE (5 models - FD11-FD15)
11. **Sample** - `apps/samples/models.py` (FD11)
12. **Flag** - `apps/samples/models.py` (FD12)
13. **LocationHistory** - `apps/samples/models.py` (FD13)
14. **SampleDisbursement** - `apps/samples/models.py` (FD14)
15. **PhysicalSampleMovement** - `apps/samples/models.py` (FD15)

#### Domain 4: ANALYSIS (3 models - FD16-FD18)
16. **AnalysisSampleBridge** - `apps/analyses/models.py` (FD16)
17. **Analysis** - `apps/analyses/models.py` (FD17)
18. **AnalysisInstrument** - `apps/analyses/models.py` (FD18)

#### Domain 5: PHYSICAL WORKFLOWS (7 models - FD19-FD25)
19. **MacroCharacteristics** - `apps/physical_analyses/models.py` (FD19)
20. **Componentry** - `apps/physical_analyses/models.py` (FD20)
21. **ParticleSizeDistribution** - `apps/physical_analyses/models.py` (FD21)
22. **MaximumClastMeasurements** - `apps/physical_analyses/models.py` (FD22)
23. **Density** - `apps/physical_analyses/models.py` (FD23)
24. **CoreMeasurements** - `apps/physical_analyses/models.py` (FD24)
25. **Cryptotephra** - `apps/physical_analyses/models.py` (FD25)

#### Domain 6: MICROANALYSIS (5 models - FD26-FD30)
26. **PolarizingMicroscope** - `apps/microanalyses/models.py` (FD26)
27. **ElectronImagingElementMap** - `apps/microanalyses/models.py` (FD27)
28. **Tomography** - `apps/microanalyses/models.py` (FD28)
29. **OtherImagingData** - `apps/microanalyses/models.py` (FD29)
30. **MicroanalysisImagingData** - `apps/microanalyses/models.py` (FD30)

#### Domain 7: GEOCHEMICAL (7 models - FD31-FD37)
31. **GeochemGeneralAttributes** - `apps/geochemical/models.py` (FD31)
32. **XRF** - `apps/geochemical/models.py` (FD32)
33. **ICPMS** - `apps/geochemical/models.py` (FD33)
34. **EPMASEM** - `apps/geochemical/models.py` (FD34)
35. **LAICPMS** - `apps/geochemical/models.py` (FD35)
36. **SIMS** - `apps/geochemical/models.py` (FD36)
37. **Geochronology** - `apps/geochemical/models.py` (FD37)

#### Domain 8: DATA MANAGEMENT (9 models - FD38-FD46)
38. **AuditTrail** - `apps/data_management/models.py` (FD38)
39. **ExportHistory** - `apps/data_management/models.py` (FD39)
40. **ExportRequest** - `apps/data_management/models.py` (FD40)
41. **ImportJob** - `apps/data_management/models.py` (FD41)
42. **File** - `apps/data_management/models.py` (FD42)
43. **Batch** - `apps/data_management/models.py` (FD43)
44. **Instrument** - `apps/data_management/models.py` (FD44)
45. **CalibrationData** - `apps/data_management/models.py` (FD45)
46. **CalibrationMeasurement** - `apps/data_management/models.py` (FD46)

**Note**: See `KUEHNLAB_DJANGO_MODELS.md` for complete model code with all fields, relationships, and methods.

---

## Views Migration

### Flask to Django View Conversion

#### Flask Route Pattern
```python
# Flask: app/projects/routes.py
from flask import render_template, request
from app.projects import bp

@bp.route('/projects')
def project_list():
    projects = get_projects()  # Mock data
    return render_template('projects/list.html', projects=projects)
```

#### Django View Pattern (Function-Based)
```python
# Django: apps/projects/views.py
from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/list.html', {'projects': projects})
```

#### Django View Pattern (Class-Based)
```python
# Django: apps/projects/views.py
from django.views.generic import ListView
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 25
```

### View Conversion Map

| Flask Route | Django View | Type |
|-------------|-------------|------|
| `main.index` | `core.views.HomeView` | ListView |
| `auth.login` | `accounts.views.LoginView` | Built-in Django |
| `auth.logout` | `accounts.views.LogoutView` | Built-in Django |
| `projects.project_list` | `projects.views.ProjectListView` | ListView |
| `projects.project_detail` | `projects.views.ProjectDetailView` | DetailView |
| `projects.project_create` | `projects.views.ProjectCreateView` | CreateView |
| `samples.sample_list` | `samples.views.SampleListView` | ListView |
| `samples.sample_detail` | `samples.views.SampleDetailView` | DetailView |
| `samples.sample_register` | `samples.views.SampleCreateView` | CreateView |

---

## Templates Migration

### Template Syntax Comparison

#### Flask (Jinja2)
```jinja2
{% extends "base.html" %}

{% block title %}{{ project.project_name }}{% endblock %}

{% block content %}
  <h1>{{ project.project_name }}</h1>
  <p>Owner: {{ project.owner }}</p>

  {% if session.get('is_authenticated') %}
    {% if session.get('user', {}).get('can_edit_sample') %}
      <a href="{{ url_for('samples.sample_register', project_id=project.id) }}">
        Add Sample
      </a>
    {% endif %}
  {% endif %}
{% endblock %}
```

#### Django Template
```django
{% extends "base.html" %}

{% block title %}{{ project.project_name }}{% endblock %}

{% block content %}
  <h1>{{ project.project_name }}</h1>
  <p>Owner: {{ project.owner }}</p>

  {% if user.is_authenticated %}
    {% if user.can_edit_samples %}
      <a href="{% url 'samples:sample_register' project_id=project.project_id %}">
        Add Sample
      </a>
    {% endif %}
  {% endif %}
{% endblock %}
```

### Key Differences

| Flask (Jinja2) | Django Template |
|----------------|-----------------|
| `url_for('route.name')` | `{% url 'app:view_name' %}` |
| `session.get('user')` | `{{ user }}` (built-in) |
| `session.get('is_authenticated')` | `{{ user.is_authenticated }}` |
| `{{ project.id }}` | `{{ project.project_id }}` (UUID) |

---

## URL Routing Migration

### Flask URL Pattern
```python
# Flask: app/projects/__init__.py
from flask import Blueprint

bp = Blueprint('projects', __name__, url_prefix='/project')

# Flask: app/projects/routes.py
@bp.route('/')
def project_list():
    pass

@bp.route('/<int:id>')
def project_detail(id):
    pass
```

### Django URL Pattern
```python
# Django: apps/projects/urls.py
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<uuid:project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
]

# Django: kuehnlab/urls.py (root)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('projects/', include('apps.projects.urls')),
    path('samples/', include('apps.samples.urls')),
]
```

---

## Static Files & Assets

### Flask Static Files
```
app/static/
├── css/
├── js/
└── images/
    ├── logo.png
    └── favicon.png
```

### Django Static Files
```
static/
├── css/
│   └── tailwind.css
├── js/
│   ├── htmx.min.js
│   └── alpine.min.js
└── images/
    ├── logo.png
    └── favicon.png

# Settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Template usage
{% load static %}
<link rel="stylesheet" href="{% static 'css/tailwind.css' %}">
<img src="{% static 'images/logo.png' %}" alt="KuehnLab">
```

---

## Testing Strategy

### Unit Tests (Models)
```python
# apps/projects/tests/test_models.py
from django.test import TestCase
from apps.accounts.models import User
from apps.projects.models import Project

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@kuehnlab.edu',
            password='testpass123'
        )

    def test_project_creation(self):
        project = Project.objects.create(
            project_name='Test Project',
            owner=self.user,
            visibility='Private'
        )
        self.assertEqual(project.project_name, 'Test Project')
        self.assertEqual(project.status, 'Active')

    def test_temporary_project_cannot_be_public(self):
        with self.assertRaises(ValueError):
            Project.objects.create(
                project_name='Temp Project',
                owner=self.user,
                visibility='Public',
                is_temporary=True
            )
```

### Integration Tests (Views)
```python
# apps/projects/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import User
from apps.projects.models import Project

class ProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@kuehnlab.edu',
            password='testpass123',
            role='Project_Owner'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_project_list_view(self):
        response = self.client.get(reverse('projects:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_create_view_permission(self):
        response = self.client.post(reverse('projects:project_create'), {
            'project_name': 'New Project',
            'description': 'Test description',
            'visibility': 'Private'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Project.objects.filter(project_name='New Project').exists())
```

---

## Deployment Considerations

### Production Settings

**File**: `kuehnlab/settings_production.py`

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['your-lightsail-domain.com', 'your-ip-address']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = '/var/www/kuehnlab/staticfiles/'

# Media files
MEDIA_ROOT = '/var/www/kuehnlab/media/'
```

### Gunicorn Configuration

**File**: `gunicorn.conf.py`

```python
bind = '0.0.0.0:8000'
workers = 4
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '/var/log/kuehnlab/access.log'
errorlog = '/var/log/kuehnlab/error.log'
loglevel = 'info'
```

### Nginx Configuration

**File**: `/etc/nginx/sites-available/kuehnlab`

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/kuehnlab/staticfiles/;
    }

    location /media/ {
        alias /var/www/kuehnlab/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Next Steps

1. **Review this guide** and ask questions
2. **Set up Django project** following Step 1-2
3. **Create models** one app at a time (start with accounts, projects, samples)
4. **Run migrations** and test in Django admin
5. **Convert views** from Flask to Django
6. **Migrate templates** to Django template syntax
7. **Test thoroughly** with unit and integration tests
8. **Deploy to Lightsail** with Gunicorn + Nginx

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django PostgreSQL Setup](https://docs.djangoproject.com/en/5.0/ref/databases/#postgresql-notes)
- [Django GIS (PostGIS)](https://docs.djangoproject.com/en/5.0/ref/contrib/gis/)
- [Django Testing](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Deploying Django](https://docs.djangoproject.com/en/5.0/howto/deployment/)

---

**Last Updated**: 2025-11-13
**Status**: Ready for implementation
**Maintained by**: Development Team
