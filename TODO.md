
# Phase 1: Current Mockup Completion (Flask)

### In Progress

* [ ] Connect to PostgreSQL database (currently using mock data)
  * [X] Database schema created and validated (33 tables)
  * [X] Docker Compose configuration complete
  * [X] Database initialization scripts from FinalNormalization diagrams
  * [ ] SQLAlchemy ORM models for all tables
  * [ ] Replace mock data with database queries
* [ ] Implement actual sample registration workflow
* [ ] File upload functionality (field photos, notes, instrument readouts)
* [ ] Bulk sample upload with CSV/Excel validation
* [ ] Project settings modal functionality (save changes)
* [ ] Access request form submission and notifications

### Remaining Mockup Tasks

* [ ] Sample search functionality within projects
* [ ] Export functionality (CSV, Excel, JSON, EarthChem format)
* [ ] Sample history/audit log implementation
* [ ] Project activity log with real-time updates
* [ ] Team member management (add/remove collaborators)
* [ ] Workflow configuration (enable/disable analysis types)
* [ ] Sample status transitions (Active → Archived)
* [ ] Pagination controls implementation
* [ ] Advanced filtering for admin views
* [ ] Toast notifications for user actions

---

# Phase 2: Tech Stack Migration (Django)

### Infrastructure Setup

* [ ] Initialize Django project structure
* [ ] Set up Django REST Framework (DRF)
* [ ] Configure PostgreSQL database (AWS RDS)
* [ ] Set up AWS S3 for file storage
* [ ] Configure AWS ECS for hosting
* [ ] Set up GitHub Actions CI/CD pipeline
* [ ] Configure Sentry for error monitoring
* [ ] Set up CloudWatch for logging
* [ ] Configure AWS Secrets Manager

### Backend Migration (Flask → Django)

* [ ] Convert Flask blueprints to Django apps
  * [ ] `main` → Django `core` app
  * [ ] `projects` → Django `projects` app
  * [ ] `samples` → Django `samples` app
  * [ ] `auth` → Django built-in auth + custom permissions
* [ ] Migrate database schema to Django ORM models
* [ ] Convert Flask routes to Django views/viewsets
* [ ] Implement DRF serializers for API endpoints
* [ ] Set up Django authentication with 5 custom roles
* [ ] Migrate session-based auth to Django auth
* [ ] Implement permission classes for access control
* [ ] Set up Django admin interface

### Frontend Migration (Bootstrap → Tailwind + HTMX)

* [ ] Install and configure Tailwind CSS
* [ ] Set up HTMX for dynamic interactions
* [ ] Convert Bootstrap components to Tailwind
  * [ ] Navigation/header
  * [ ] Cards and containers
  * [ ] Tables and data grids
  * [ ] Forms and inputs
  * [ ] Modals and overlays
  * [ ] Badges and status indicators
  * [ ] Buttons and actions
* [ ] Replace JavaScript interactions with HTMX
  * [ ] Search functionality
  * [ ] Sorting and filtering
  * [ ] Modal interactions
  * [ ] Form submissions
  * [ ] Dynamic content loading
* [ ] Implement Tailwind-based responsive design
* [ ] Add Alpine.js for client-side interactivity (if needed)

### Database Schema Implementation

**Reference:** `diagrams/database_schema.md`

#### Core Tables (20 total)

* [ ] User (extends Django User model)
* [ ] Project
* [ ] ProjectMember
* [ ] Sample
* [ ] SampleRelationship
* [ ] Location
* [ ] PhysicalAnalysis
* [ ] Microanalysis
* [ ] GeochemicalAnalysis
* [ ] GeochemicalRun
* [ ] GeochemicalResult
* [ ] Correlation
* [ ] CorrelationMatch
* [ ] Workflow
* [ ] WorkflowStep
* [ ] File
* [ ] ActivityLog
* [ ] AccessRequest
* [ ] Notification
* [ ] Settings

#### Key Relationships

* [ ] One-to-many: Project → Sample
* [ ] Many-to-many: Project ↔ User (through ProjectMember)
* [ ] Many-to-many: Sample ↔ Sample (through SampleRelationship)
* [ ] One-to-many: Sample → Physical/Micro/Geochemical Analysis
* [ ] Proper CASCADE/PROTECT settings

### API Development

* [ ] REST API endpoints for all resources
* [ ] Authentication endpoints
* [ ] Project CRUD
* [ ] Sample CRUD
* [ ] Analysis endpoints
* [ ] File upload/download
* [ ] Search/filter endpoints
* [ ] Bulk ops
* [ ] Export formats
* [ ] Access request & notifications
* [ ] Swagger/OpenAPI documentation
* [ ] Rate limiting
* [ ] API versioning

### Authentication & Authorization

* [ ] Django authentication setup
* [ ] Custom user model with roles
* [ ] Permissions system (5 roles):
  * Administrator
  * Project_Owner
  * Collaborator
  * View_Export
  * View_Only
* [ ] Row-level access rules
* [ ] Token auth
* [ ] Password reset
* [ ] Email verification
* [ ] Session management
* [ ] CSRF protection

---

# Phase 3: Feature Enhancements

### Sample Management

* [ ] Advanced search
* [ ] Parent/child relationships
* [ ] QR code generation
* [ ] Batch operations
* [ ] Archiving workflow
* [ ] Transfer between projects
* [ ] Reservation system
* [ ] Custom metadata fields

### Analysis Workflows

**Physical Analysis**

* [ ] Sieve analysis
* [ ] Density separation
* [ ] Magnetic separation
* [ ] Loss on ignition
* [ ] Mass balance tracking

**Microanalysis**

* [ ] EPMA/SEM point analysis
* [ ] Micro-XRF mapping
* [ ] SIMS isotope analysis
* [ ] Mineral identification

**Geochemical**

* [ ] ICP-MS
* [ ] LA-ICP-MS
* [ ] XRF
* [ ] Geochronology
* [ ] Standards & QC tracking

### Correlation

* [ ] Stats correlation tools
* [ ] Similarity scoring
* [ ] Visual comparison tools

### Data Visualization

* [ ] Interactive charts
* [ ] Geochem plots
* [ ] Location maps
* [ ] Timelines
* [ ] Statistical tools
* [ ] Multi-format export

### File Management

* [ ] S3 integration
* [ ] Validation
* [ ] Thumbnails
* [ ] Versioning
* [ ] Sharing
* [ ] Bulk ops
* [ ] Previews

### Collaboration Features

* [ ] Invitations
* [ ] Access approvals
* [ ] Email + in-app notifications
* [ ] Feeds
* [ ] Comments
* [ ] @mentions

### Data Integration

* [ ] IGSN
* [ ] SESAR
* [ ] EarthChem
* [ ] GeoPass
* [ ] DOI minting
* [ ] External repo support

---

# Phase 4: Security & Compliance

### Security

* [ ] HTTPS
* [ ] SQL injection defense
* [ ] XSS protection
* [ ] CSRF protection
* [ ] Rate limiting
* [ ] Input validation
* [ ] Secure file checks
* [ ] AuthN/AuthZ hardening
* [ ] Audit logging
* [ ] Encryption at rest & transit

### Compliance

* [ ] GDPR support
* [ ] Retention policies
* [ ] Privacy policy
* [ ] Terms of service
* [ ] Cookie consent
* [ ] User data export
* [ ] Right-to-be-forgotten

---

# Phase 5: AWS Deployment

### Infrastructure as Code

* [ ] Terraform/CloudFormation
* [ ] VPC
* [ ] ECS cluster
* [ ] RDS PostgreSQL
* [ ] S3
* [ ] CloudFront
* [ ] Route53
* [ ] Load balancer
* [ ] Auto-scaling

### CI/CD

* [ ] GitHub Actions
* [ ] Tests
* [ ] Docker builds
* [ ] ECR
* [ ] Staging & prod
* [ ] Rollbacks
* [ ] Migration automation

### Monitoring & Logging

* [ ] Sentry
* [ ] CloudWatch metrics
* [ ] CloudWatch logs
* [ ] APM
* [ ] DB monitoring
* [ ] Uptime
* [ ] Alerts

### Backup & Recovery

* [ ] Automated backups
* [ ] S3 versioning
* [ ] DR plan
* [ ] Backup tests
* [ ] PIT recovery

---

# Phase 6: Testing & QA

### Testing Strategy

* [ ] Unit tests
* [ ] Integration tests
* [ ] API tests
* [ ] End-to-end tests
* [ ] Performance tests
* [ ] Security tests
* [ ] Load tests
* [ ] Accessibility tests

### Code Quality

* [ ] Linting
* [ ] Type checking
* [ ] Coverage >80%
* [ ] Code review workflow
* [ ] Docs standards
* [ ] Commit conventions

---

# Phase 7: Documentation

### Technical

* [ ] API docs
* [ ] Architecture
* [ ] DB schema
* [ ] Deployment guide
* [ ] Dev setup guide
* [ ] Contributing
* [ ] Code style

### User Docs

* [ ] User manual
* [ ] Admin guide
* [ ] Quick start
* [ ] Video tutorials
* [ ] FAQ
* [ ] Troubleshooting

---

# Deferred to Future Enhancements

### Authentication

* [ ] SSO/OIDC
* [ ] MFA
* [ ] OAuth2 providers

### Advanced Features

* [ ] Real-time collaboration
* [ ] Elasticsearch
* [ ] ML-based correlation
* [ ] Mobile app
* [ ] Webhooks
* [ ] GraphQL
* [ ] i18n
* [ ] Dashboards
* [ ] Data versioning
* [ ] Automation

### Infrastructure

* [ ] Multi-region
* [ ] DR
* [ ] Prometheus/Grafana
* [ ] Performance tuning
* [ ] CDN optimization
* [ ] Index optimization

---

# Immediate Next Steps

1. Complete pull request for `feature/matt → main`
2. Decide on migration strategy (continue Flask mockup or start Django migration)
3. Database connection setup (Flask vs Django decision)
4. Confirm Tailwind + HTMX approach with team

---

# Notes

* Current mockup uses Flask + Bootstrap for speed
* Production stack: Django + Tailwind + HTMX + AWS
* 20-table normalized schema in `diagrams/database_schema.md`
* Mock data stored under `app/projects/routes.py` and `app/samples/routes.py`
* Generic branding complete
* Admin views functional using mock data
* Private project access control already implemented
