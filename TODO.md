# KuehnLab - Development Roadmap

**Current Status**: Flask mockup hosted on Amazon Lightsail
**Target Stack**: Django + PostgreSQL + pgAdmin + Tailwind CSS + HTMX
**Hosting**: Amazon Lightsail (currently deployed)

---

## 🎯 Current State

- ✅ Flask mockup application deployed on Amazon Lightsail
- ✅ Database schema designed (20 entities, 263 fields)
- ✅ Basic UI with Bootstrap 5
- ✅ Role-based access control mockup (5 roles)
- ✅ Project and sample management views
- ✅ Generic branding (KuehnLab)
- ⚠️ Using mock data (not connected to PostgreSQL)
- ⚠️ No pgAdmin integration yet

---

# Phase 1: Django Migration Preparation

### Pre-Migration Tasks

* [ ] **Audit remaining placeholder references**
  * [X] Identify files with old branding
  * [X] Update `app/auth/routes.py` - change @concord.edu emails to @kuehnlab.edu
  * [X] Update `app/auth/README_MOCK_LOGIN.md` - change @concord.edu emails to @kuehnlab.edu
  * [X] Update `app/samples/routes.py` - change @culs.example.edu to @kuehnlab.edu
  * [X] Update `app/templates/components/_header.html` - changed to "KuehnLab"
  * [X] Search for any remaining "Geology Lab Software" references
  * [X] Update CHANGELOG.md with final branding changes

* [ ] **Database preparation**
  * [ ] Set up PostgreSQL on Lightsail or separate database instance
  * [ ] Install and configure pgAdmin for database management
  * [ ] Create production database schema
  * [ ] Create development/staging database schema
  * [ ] Document database connection strings
  * [ ] Set up database backups on Lightsail

* [X] **Documentation**
  * [X] Document current Flask architecture
  * [X] Create migration plan timeline (see DJANGO_MIGRATION_GUIDE.md)
  * [X] Document API endpoints to preserve
  * [X] List all current routes and views
  * [X] Identify breaking changes for users
  * [X] Create automated setup scripts (django_setup.sh, django_setup.bat)
  * [X] Create Django quick-start guide (DJANGO_README.md)

---

# Phase 2: Django Project Setup

**See DJANGO_MIGRATION_GUIDE.md and DJANGO_README.md for complete instructions and code examples**

### Infrastructure on Amazon Lightsail

* [ ] **Lightsail instance configuration**
  * [ ] Verify current Lightsail instance specifications
  * [ ] Plan resource requirements for Django
  * [ ] Set up separate Lightsail database instance (or RDS)
  * [ ] Configure Lightsail static IP
  * [ ] Set up Lightsail load balancer (if needed)
  * [ ] Configure Lightsail firewall rules
  * [ ] Set up SSL/TLS certificate (Let's Encrypt or Lightsail cert)

* [ ] **PostgreSQL + pgAdmin setup**
  * [ ] Install PostgreSQL on Lightsail or use managed database
  * [ ] Configure PostgreSQL for remote connections
  * [ ] Install pgAdmin 4 (web interface)
  * [ ] Configure pgAdmin authentication
  * [ ] Set up database users and roles in pgAdmin
  * [ ] Create backup schedules through pgAdmin
  * [ ] Document pgAdmin access URL and credentials

* [ ] **Django project initialization**
  * [ ] Create Django project structure (`kuehn_labs`)
  * [ ] Set up virtual environment
  * [ ] Install Django 5.0+ and dependencies
  * [ ] Configure settings.py for Lightsail deployment
  * [ ] Set up environment variables (.env)
  * [ ] Configure static files handling
  * [ ] Set up media files storage
  * [ ] Configure logging

### Django Apps Structure

* [ ] **Core apps**
  * [ ] `core` - Homepage, dashboard, base templates
  * [ ] `accounts` - Custom user model with 5 roles
  * [ ] `projects` - Project management
  * [ ] `samples` - Sample tracking and management
  * [ ] `analyses` - Physical, micro, and geochemical analysis
  * [ ] `files` - File upload and management
  * [ ] `reports` - Export and reporting functionality

* [ ] **Database configuration**
  * [ ] Configure Django to use PostgreSQL
  * [ ] Set up database connection pooling
  * [ ] Configure pgAdmin access for team
  * [ ] Create initial migrations
  * [ ] Document migration commands

---

# Phase 3: Backend Migration (Flask → Django)

### Django Models (ORM)

**Reference:** `ENTITY-REFERENCE.md` (20 entities, 263 fields)

#### Core Management Models
* [ ] `User` (extend Django AbstractUser)
  * [ ] 16 fields including succession planning
  * [ ] 5 role choices (Administrator, Project_Owner, Collaborator, View_Export, View_Only)
  * [ ] Self-referencing designated_successor
  * [ ] ORCID field validation
* [ ] `Project`
  * [ ] 12 fields with visibility enum
  * [ ] Owner foreign key to User
  * [ ] Status field (Active, Archived, Pending_Transfer, etc.)
* [ ] `ProjectCollaborator` (through model)
  * [ ] 8 fields with permissions JSONB
  * [ ] Unique constraint on (project, user)
* [ ] `ProjectTransfer`
  * [ ] 15 fields for ownership transfer tracking

#### Sample Management Models
* [ ] `Sample`
  * [ ] 22 fields including IGSN
  * [ ] Geographic coordinates (Django GIS)
  * [ ] Metadata and public_metadata JSONFields
  * [ ] Parent-child relationship (self FK)
  * [ ] Version control and soft deletes
* [ ] `SampleDisbursement`
  * [ ] 12 fields for sample splitting

#### Analytical Workflow Models
* [ ] `PhysicalAnalysis` (7 workflow branches)
  * [ ] 15 fields with 7 JSONB workflow fields
  * [ ] QC status enum
* [ ] `PhysicalMicroanalysis` (4 workflow branches)
  * [ ] 14 fields with image file handling
* [ ] `GeochemicalAnalysis` (7 workflow branches)
  * [ ] 16 fields with calibration tracking
* [ ] `Instrument`
  * [ ] 11 fields with calibration frequency
* [ ] `AnalyticalBatch`
  * [ ] 9 fields for batch QC
* [ ] `CalibrationData`
  * [ ] 10 fields for standards tracking
* [ ] `ToolProfile`
  * [ ] 12 fields for reusable instrument profiles

#### People & Attribution Models
* [ ] `Person`
  * [ ] 12 fields with ORCID
  * [ ] Optional link to User account
* [ ] `ProjectPerson` (through model)
  * [ ] 7 fields with role attribution
* [ ] `SamplePerson` (through model)
  * [ ] 7 fields for chain-of-custody

#### Data Management Models
* [ ] `ImportJob`
  * [ ] 12 fields for import tracking
* [ ] `ExportHistory`
  * [ ] 10 fields with audit trail
* [ ] `ExportRequest`
  * [ ] 9 fields for permission workflows
* [ ] `AuditTrail`
  * [ ] 12 fields, immutable log
  * [ ] 7-year retention policy

### Django Views & URLs

* [ ] **Convert Flask blueprints to Django apps**
  * [ ] `main` blueprint → `core` app
  * [ ] `auth` blueprint → `accounts` app (use Django auth)
  * [ ] `projects` blueprint → `projects` app
  * [ ] `samples` blueprint → `samples` app

* [ ] **URL configuration**
  * [ ] Main URL patterns
  * [ ] App-specific URL patterns
  * [ ] API URL patterns (Django REST Framework)
  * [ ] Admin URL patterns

* [ ] **Views migration**
  * [ ] Convert Flask routes to Django views
  * [ ] Implement class-based views where appropriate
  * [ ] Add proper permission decorators
  * [ ] Implement pagination
  * [ ] Add search and filtering

### Django REST Framework (API)

* [ ] **DRF setup**
  * [ ] Install Django REST Framework
  * [ ] Configure DRF settings
  * [ ] Set up authentication (Token/JWT)
  * [ ] Configure permissions
  * [ ] Set up CORS

* [ ] **Serializers**
  * [ ] User serializer
  * [ ] Project serializer (nested)
  * [ ] Sample serializer (nested)
  * [ ] Analysis serializers
  * [ ] File upload serializer

* [ ] **API ViewSets**
  * [ ] ProjectViewSet with filtering
  * [ ] SampleViewSet with search
  * [ ] AnalysisViewSet
  * [ ] FileViewSet
  * [ ] ExportViewSet

* [ ] **API documentation**
  * [ ] Install drf-spectacular (OpenAPI)
  * [ ] Document all endpoints
  * [ ] Add example requests/responses
  * [ ] Generate Swagger UI

### Authentication & Authorization

* [ ] **Django authentication**
  * [ ] Custom user model with 5 roles
  * [ ] Login/logout views
  * [ ] Password reset flow
  * [ ] Email verification (optional)
  * [ ] Session management

* [ ] **Permission system**
  * [ ] Create custom permission classes
  * [ ] Implement row-level permissions
  * [ ] Project visibility enforcement
  * [ ] Sample access control
  * [ ] Export permission checks

* [ ] **Admin interface**
  * [ ] Customize Django admin for all models
  * [ ] Add filters and search
  * [ ] Inline editing for related objects
  * [ ] Readonly fields for audit data
  * [ ] Admin actions (bulk operations)

---

# Phase 4: Frontend Migration

### Tailwind CSS Setup

* [ ] **Installation & configuration**
  * [ ] Install Tailwind CSS
  * [ ] Configure tailwind.config.js
  * [ ] Set up PostCSS
  * [ ] Configure purge/content settings
  * [ ] Add custom color scheme (KuehnLab branding)
  * [ ] Configure custom fonts if needed

* [ ] **Convert Bootstrap to Tailwind**
  * [ ] Navigation/header components
  * [ ] Footer components
  * [ ] Card layouts
  * [ ] Tables and data grids
  * [ ] Forms and inputs
  * [ ] Buttons and badges
  * [ ] Modals and overlays
  * [ ] Alert/notification components
  * [ ] Responsive utilities

### HTMX Integration

* [ ] **HTMX setup**
  * [ ] Install HTMX
  * [ ] Configure HTMX in base template
  * [ ] Set up HTMX headers in Django views
  * [ ] Configure HTMX error handling

* [ ] **Dynamic interactions with HTMX**
  * [ ] Search functionality (live search)
  * [ ] Sorting and filtering (no page reload)
  * [ ] Form submissions (inline validation)
  * [ ] Modal interactions (load content dynamically)
  * [ ] Infinite scroll / lazy loading
  * [ ] Notifications and toasts
  * [ ] Delete confirmations

* [ ] **Alpine.js (optional)**
  * [ ] Install Alpine.js for client-side state
  * [ ] Dropdown menus
  * [ ] Tabs and accordions
  * [ ] Form field toggling
  * [ ] Client-side validation

### Template Migration

* [ ] **Base templates**
  * [ ] `base.html` with Tailwind
  * [ ] Navigation partial
  * [ ] Footer partial
  * [ ] Flash messages component

* [ ] **Core app templates**
  * [ ] Homepage/dashboard
  * [ ] User profile
  * [ ] Settings page

* [ ] **Projects app templates**
  * [ ] Project list view
  * [ ] Project detail view
  * [ ] Project create/edit forms
  * [ ] Project settings modal

* [ ] **Samples app templates**
  * [ ] Sample list view
  * [ ] Sample detail view
  * [ ] Sample registration form
  * [ ] Bulk upload interface
  * [ ] Sample history/audit log

* [ ] **Analysis templates**
  * [ ] Physical analysis forms (7 branches)
  * [ ] Microanalysis forms (4 branches)
  * [ ] Geochemical analysis forms (7 branches)
  * [ ] QC status indicators

* [ ] **Reports templates**
  * [ ] Export format selection
  * [ ] Export preview
  * [ ] Download page

---

# Phase 5: Database Integration

### PostgreSQL Configuration

* [ ] **Database setup in pgAdmin**
  * [ ] Create production database
  * [ ] Create development database
  * [ ] Create test database
  * [ ] Set up database users and roles
  * [ ] Configure connection limits
  * [ ] Enable required extensions (PostGIS for geographic data)

* [ ] **Schema migration**
  * [ ] Run Django migrations to create all tables
  * [ ] Verify foreign key constraints
  * [ ] Verify indexes created correctly
  * [ ] Set up database partitioning (audit_trail, export_history)
  * [ ] Document schema in pgAdmin

* [ ] **Data migration from Flask**
  * [ ] Export mock data structure
  * [ ] Create Django fixtures
  * [ ] Load initial test data
  * [ ] Verify data integrity

### pgAdmin Configuration

* [ ] **pgAdmin setup**
  * [ ] Install pgAdmin 4 web interface
  * [ ] Configure server connections
  * [ ] Set up team member access
  * [ ] Configure query tool settings
  * [ ] Set up dashboard widgets

* [ ] **Database management workflows**
  * [ ] Document backup procedures in pgAdmin
  * [ ] Set up scheduled backups
  * [ ] Configure maintenance jobs
  * [ ] Set up query monitoring
  * [ ] Document common queries for team

---

# Phase 6: File Management

### File Upload System

* [ ] **Local file storage (initial)**
  * [ ] Configure Django media files
  * [ ] Set up file upload views
  * [ ] Implement file validation
  * [ ] Generate thumbnails for images
  * [ ] Organize files by project/sample hierarchy

* [ ] **Future: AWS S3 (Phase 7)**
  * [ ] Deferred to later phase
  * [ ] Document S3 migration plan

### Supported File Types

* [ ] **Sample files**
  * [ ] Field photos (JPEG, PNG, HEIC)
  * [ ] Field notes (PDF, DOCX, TXT)
  * [ ] GPS data (GPX, KML)

* [ ] **Analysis files**
  * [ ] Instrument data (CSV, XLSX, TXT)
  * [ ] Microscopy images (TIFF, JPEG, PNG, BCF)
  * [ ] 3D tomography (DICOM, custom formats)
  * [ ] Geochemical data (CSV, XLSX)

* [ ] **Export files**
  * [ ] CSV export
  * [ ] Excel export
  * [ ] JSON export
  * [ ] EarthChem XML format

---

# Phase 7: Testing & Quality Assurance

### Testing Strategy

* [ ] **Unit tests**
  * [ ] Model tests (all 20 models)
  * [ ] View tests
  * [ ] Form tests
  * [ ] Serializer tests
  * [ ] Permission tests
  * [ ] Utility function tests

* [ ] **Integration tests**
  * [ ] Authentication flows
  * [ ] Project workflows
  * [ ] Sample registration workflows
  * [ ] Analysis data entry
  * [ ] Export functionality
  * [ ] File upload/download

* [ ] **API tests**
  * [ ] Test all REST endpoints
  * [ ] Test authentication
  * [ ] Test permissions
  * [ ] Test filtering and search
  * [ ] Test pagination
  * [ ] Test error handling

* [ ] **End-to-end tests**
  * [ ] User registration/login
  * [ ] Project creation and management
  * [ ] Sample registration
  * [ ] Analysis workflows
  * [ ] Export workflows
  * [ ] Team collaboration

* [ ] **Performance tests**
  * [ ] Load testing with multiple users
  * [ ] Database query optimization
  * [ ] Large file upload testing
  * [ ] Bulk operations testing

* [ ] **Security tests**
  * [ ] OWASP Top 10 vulnerability scan
  * [ ] SQL injection tests
  * [ ] XSS tests
  * [ ] CSRF tests
  * [ ] Authentication bypass tests
  * [ ] Permission escalation tests

### Code Quality

* [ ] **Linting & formatting**
  * [ ] Set up Black (Python formatter)
  * [ ] Set up Flake8 (linter)
  * [ ] Set up isort (import sorting)
  * [ ] Set up Prettier (JS/CSS)
  * [ ] Pre-commit hooks

* [ ] **Type checking**
  * [ ] Set up mypy for Python type hints
  * [ ] Add type hints to critical functions
  * [ ] Configure mypy.ini

* [ ] **Test coverage**
  * [ ] Set up coverage.py
  * [ ] Target >80% coverage
  * [ ] Generate coverage reports
  * [ ] Add coverage badge to README

* [ ] **Code review**
  * [ ] Define code review process
  * [ ] Create pull request template
  * [ ] Document code standards
  * [ ] Set up branch protection rules

---

# Phase 8: Deployment on Amazon Lightsail

### Lightsail Deployment Configuration

* [ ] **Django application deployment**
  * [ ] Configure Gunicorn for production
  * [ ] Set up Nginx as reverse proxy
  * [ ] Configure static files serving
  * [ ] Configure media files serving
  * [ ] Set up environment variables
  * [ ] Configure ALLOWED_HOSTS
  * [ ] Set DEBUG=False

* [ ] **SSL/TLS certificate**
  * [ ] Obtain SSL certificate (Let's Encrypt or Lightsail)
  * [ ] Configure Nginx for HTTPS
  * [ ] Set up automatic certificate renewal
  * [ ] Force HTTPS redirects
  * [ ] Configure HSTS headers

* [ ] **Database on Lightsail**
  * [ ] Set up managed PostgreSQL database (or separate instance)
  * [ ] Configure database backups
  * [ ] Set up read replicas (if needed)
  * [ ] Configure connection pooling
  * [ ] Restrict database access to application only

* [ ] **pgAdmin deployment**
  * [ ] Deploy pgAdmin on separate Lightsail instance (or container)
  * [ ] Configure reverse proxy for pgAdmin
  * [ ] Set up authentication
  * [ ] Restrict access by IP (VPN or team IPs)
  * [ ] Document access procedures

### CI/CD Pipeline

* [ ] **GitHub Actions setup**
  * [ ] Create workflow files
  * [ ] Set up automated testing
  * [ ] Configure Docker builds (if using containers)
  * [ ] Set up deployment scripts
  * [ ] Configure secrets management

* [ ] **Deployment workflow**
  * [ ] Develop → staging → production flow
  * [ ] Automated migrations
  * [ ] Zero-downtime deployments
  * [ ] Rollback procedures
  * [ ] Health checks

### Monitoring & Logging

* [ ] **Application monitoring**
  * [ ] Set up error tracking (Sentry or similar)
  * [ ] Configure Django logging
  * [ ] Set up application metrics
  * [ ] Monitor response times
  * [ ] Monitor error rates

* [ ] **Infrastructure monitoring**
  * [ ] Lightsail instance metrics (CPU, memory, disk)
  * [ ] Database performance monitoring
  * [ ] Disk space alerts
  * [ ] Uptime monitoring
  * [ ] SSL certificate expiration alerts

* [ ] **Logging**
  * [ ] Centralized logging (file-based or external service)
  * [ ] Log rotation configuration
  * [ ] Access logs
  * [ ] Error logs
  * [ ] Audit logs (7-year retention)

### Backup & Recovery

* [ ] **Database backups**
  * [ ] Automated daily backups
  * [ ] Weekly full backups
  * [ ] Test restore procedures
  * [ ] Document recovery steps
  * [ ] Off-site backup storage

* [ ] **Application backups**
  * [ ] Code repository backups (GitHub)
  * [ ] Media files backups
  * [ ] Configuration files backups
  * [ ] Lightsail snapshots

* [ ] **Disaster recovery plan**
  * [ ] Document recovery procedures
  * [ ] Define RTO (Recovery Time Objective)
  * [ ] Define RPO (Recovery Point Objective)
  * [ ] Test disaster recovery annually

---

# Phase 9: Security & Compliance

### Security Hardening

* [ ] **Application security**
  * [ ] HTTPS enforcement
  * [ ] SQL injection protection (Django ORM)
  * [ ] XSS protection (Django templates)
  * [ ] CSRF protection (Django middleware)
  * [ ] Clickjacking protection
  * [ ] Content Security Policy headers
  * [ ] Rate limiting on API endpoints
  * [ ] Input validation and sanitization
  * [ ] Secure file upload validation
  * [ ] Password strength requirements

* [ ] **Infrastructure security**
  * [ ] Firewall rules (Lightsail)
  * [ ] SSH key-based authentication only
  * [ ] Disable password authentication
  * [ ] Keep software updated
  * [ ] Security patch management
  * [ ] Principle of least privilege for users

* [ ] **Data security**
  * [ ] Encryption at rest (database)
  * [ ] Encryption in transit (HTTPS)
  * [ ] Secure environment variables
  * [ ] Secret management (not in code)
  * [ ] Audit trail immutability
  * [ ] 7-year audit log retention

### Compliance

* [ ] **FERPA compliance** (if applicable)
  * [ ] Document data handling procedures
  * [ ] Implement access controls
  * [ ] Audit trail for data access
  * [ ] Data retention policies

* [ ] **GDPR considerations** (if EU users)
  * [ ] Privacy policy
  * [ ] Terms of service
  * [ ] Cookie consent
  * [ ] User data export functionality
  * [ ] Right-to-be-forgotten implementation

* [ ] **Repository compliance**
  * [ ] IGSN metadata mapping
  * [ ] EarthChem export format
  * [ ] ORCID integration for attribution
  * [ ] Data citation guidelines

---

# Phase 10: Documentation

### Technical Documentation

* [ ] **Architecture documentation**
  * [ ] System architecture diagram
  * [ ] Database schema documentation
  * [ ] API documentation (OpenAPI/Swagger)
  * [ ] Deployment architecture
  * [ ] Security architecture

* [ ] **Developer documentation**
  * [ ] Development setup guide
  * [ ] Code structure overview
  * [ ] Coding standards
  * [ ] Git workflow
  * [ ] Testing guidelines
  * [ ] Contributing guidelines

* [ ] **Operations documentation**
  * [ ] Deployment procedures
  * [ ] Backup and recovery procedures
  * [ ] Monitoring and alerting setup
  * [ ] Troubleshooting guide
  * [ ] Incident response plan
  * [ ] pgAdmin usage guide

### User Documentation

* [ ] **User manual**
  * [ ] Getting started guide
  * [ ] Project management guide
  * [ ] Sample registration guide
  * [ ] Analysis workflows guide (18 branches)
  * [ ] Export and reporting guide
  * [ ] Collaboration features guide

* [ ] **Administrator guide**
  * [ ] User management
  * [ ] Role configuration
  * [ ] System settings
  * [ ] Database management with pgAdmin
  * [ ] Backup procedures
  * [ ] Audit log review

* [ ] **Training materials**
  * [ ] Quick start tutorials
  * [ ] Video walkthroughs
  * [ ] FAQ
  * [ ] Common workflows
  * [ ] Best practices

---

# Phase 11: Advanced Features (Future Enhancements)

### Sample Management Enhancements

* [ ] Advanced search with multiple criteria
* [ ] QR code generation for sample labels
* [ ] Batch operations (bulk status changes)
* [ ] Sample reservation system
* [ ] Custom metadata field definitions
* [ ] Sample chain-of-custody visualization

### Analysis Workflow Enhancements

* [ ] Real-time collaboration on analyses
* [ ] Version comparison for analytical results
* [ ] Automatic calculation of derived values
* [ ] Integration with instrument APIs
* [ ] Template-based data entry
* [ ] Quality control dashboard

### Data Visualization

* [ ] Interactive geochemical plots (Harker diagrams, REE plots)
* [ ] Sample location maps (GIS integration)
* [ ] Timeline visualization
* [ ] Statistical analysis tools
* [ ] Correlation matrix visualization
* [ ] Export plots in publication-quality formats

### Collaboration Features

* [ ] Real-time notifications (WebSockets)
* [ ] In-app messaging
* [ ] Comments and annotations
* [ ] @mentions
* [ ] Activity feeds
* [ ] Email digests

### Data Integration

* [ ] IGSN registration API
* [ ] SESAR integration
* [ ] EarthChem repository submission
* [ ] DOI minting for datasets
* [ ] ORCiD authentication
* [ ] External repository sync

### Advanced Infrastructure (Future)

* [ ] Multi-region deployment
* [ ] CDN for static files
* [ ] Elasticsearch for advanced search
* [ ] Redis for caching
* [ ] Celery for background tasks
* [ ] WebSockets for real-time features

---

# Immediate Next Steps (Priority)

## Week 1-2: Branding & Database Setup
1. [X] Update remaining placeholder references to KuehnLab
2. [ ] Set up PostgreSQL database on Lightsail
3. [ ] Install and configure pgAdmin
4. [ ] Document database connection details

## Week 3-4: Django Project Initialization
5. [ ] Initialize Django project structure
6. [ ] Create Django apps (core, accounts, projects, samples, analyses)
7. [ ] Configure Django settings for Lightsail
8. [ ] Set up development environment

## Week 5-8: Core Models Migration
9. [ ] Implement all 20 Django models based on ENTITY-REFERENCE.md
10. [ ] Run migrations in development database
11. [ ] Verify schema in pgAdmin
12. [ ] Create admin interface for all models

## Week 9-12: Views & Templates
13. [ ] Migrate Flask views to Django views
14. [ ] Convert Bootstrap templates to Tailwind
15. [ ] Implement HTMX for dynamic interactions
16. [ ] Test all user workflows

## Week 13-16: Testing & Deployment
17. [ ] Write comprehensive tests (unit, integration, E2E)
18. [ ] Set up CI/CD pipeline
19. [ ] Deploy to production Lightsail instance
20. [ ] Monitor and optimize

---

# Notes

* **Current hosting**: Amazon Lightsail (already deployed)
* **Current stack**: Flask + Bootstrap + Mock Data
* **Target stack**: Django + Tailwind + HTMX + PostgreSQL + pgAdmin
* **Database**: 20 entities, 263 fields, 18 analytical workflow branches
* **Branding**: KuehnLab (replacing all previous references)
* **Repository**: GitHub with CI/CD
* **Documentation**: `PROJECT-OVERVIEW.md`, `ENTITY-REFERENCE.md`, `requirements.md`

---

# Questions to Resolve

1. **Database hosting**: Same Lightsail instance or separate database instance?
2. **pgAdmin deployment**: Separate Lightsail instance or container on main instance?
3. **Migration strategy**: Gradual (feature by feature) or big bang?
4. **Downtime**: Can we afford downtime during migration, or need zero-downtime approach?
5. **Domain**: Do we need to update domain/subdomain for KuehnLab?
6. **Team access**: Who needs pgAdmin access for database management?

---

**Last Updated**: 2025-11-13
**Maintained by**: Development Team
