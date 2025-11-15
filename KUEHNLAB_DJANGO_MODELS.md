# KuehnLab Django Models - Complete Implementation Guide

**Based on**: `Kuehn_Lab_Normalization.md`
**Total Entities**: 46 Functional Dependencies (FD1-FD46)
**Total Domains**: 8
**Date**: 2025-11-14

---

## Table of Contents

1. [Domain 1: USER & ACCESS](#domain-1-user--access-fd1-fd5)
2. [Domain 2: PROJECT](#domain-2-project-fd6-fd10)
3. [Domain 3: SAMPLE](#domain-3-sample-fd11-fd15)
4. [Domain 4: ANALYSIS](#domain-4-analysis-fd16-fd18)
5. [Domain 5: PHYSICAL WORKFLOWS](#domain-5-physical-workflows-fd19-fd25)
6. [Domain 6: MICROANALYSIS](#domain-6-microanalysis-fd26-fd30)
7. [Domain 7: GEOCHEMICAL](#domain-7-geochemical-fd31-fd37)
8. [Domain 8: DATA MANAGEMENT](#domain-8-data-management-fd38-fd46)

---

## Domain 1: USER & ACCESS (FD1-FD5)

**File**: `apps/accounts/models.py`

### Common Imports
```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import EmailValidator
from django.utils import timezone
```

---

### FD1 - User Model

```python
class User(AbstractUser):
    """
    FD1: user_id → person_id, username, email, password_hash, is_admin

    Custom user model extending Django's AbstractUser.
    Functional Dependencies:
    - username → user_id (AK)
    - email → user_id (AK)
    """
    person = models.ForeignKey(
        'Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_accounts',
        help_text="Link to Person record for attribution"
    )
    is_admin = models.BooleanField(
        default=False,
        help_text="Administrative privileges flag"
    )

    class Meta:
        db_table = 'users'
        ordering = ['username']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['person']),
        ]

    def __str__(self):
        return f"{self.username} ({self.email})"
```

---

### FD2 - User Session Model

```python
class UserSession(models.Model):
    """
    FD2: session_id → user_id, ip_address, device, session_log_id, is_active

    Track user sessions for security and audit purposes.
    """
    session_id = models.CharField(
        max_length=40,
        primary_key=True,
        help_text="Django session ID"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    ip_address = models.GenericIPAddressField(
        help_text="Client IP address"
    )
    device = models.CharField(
        max_length=255,
        blank=True,
        help_text="User agent string"
    )
    session_log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference to session log entry"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Session active status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} ({'active' if self.is_active else 'inactive'})"
```

---

### FD3 - Project User Model

```python
class ProjectUser(models.Model):
    """
    FD3: project_user_id → project_id, user_id, role_code, log_id

    Bridge table for project collaborators with role assignments.
    """
    ROLE_CHOICES = [
        ('OWNER', 'Project Owner'),
        ('COLLABORATOR', 'Collaborator'),
        ('VIEW_EXPORT', 'View & Export'),
        ('VIEW_ONLY', 'View Only'),
    ]

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='project_users'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    role_code = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='VIEW_ONLY'
    )
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Audit log reference"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_users'
        unique_together = [['project', 'user']]
        ordering = ['project', 'user']
        indexes = [
            models.Index(fields=['project', 'role_code']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.get_role_code_display()})"
```

---

### FD4 - Person Model

```python
class Person(models.Model):
    """
    FD4: person_id → all person attributes

    Track individuals for attribution and collaboration.
    Functional Dependency: orcid → person_id (AK)
    """
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    title = models.CharField(
        max_length=50,
        blank=True,
        help_text="Dr., Prof., etc."
    )
    orcid = models.CharField(
        max_length=19,
        unique=True,
        blank=True,
        null=True,
        help_text="ORCID identifier (AK)"
    )
    organization_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Institution/organization identifier"
    )
    phone_num = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(
        default=False,
        help_text="Person record verified"
    )
    org_name = models.CharField(max_length=255, blank=True)
    org_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="University, Research Institute, etc."
    )
    affiliation = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference to PersonLog"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'persons'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['orcid']),
            models.Index(fields=['organization_id']),
        ]

    def __str__(self):
        name_parts = [self.title, self.first_name, self.middle_name, self.last_name]
        return ' '.join(filter(None, name_parts))

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
```

---

### FD5 - Person Log Model

```python
class PersonLog(models.Model):
    """
    FD5: log_id → person_id, person_log

    Audit trail for person record changes.
    """
    log_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Unique log identifier"
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        related_name='logs'
    )
    person_log = models.TextField(
        help_text="JSON or text log of changes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'person_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['person', 'created_at']),
        ]

    def __str__(self):
        return f"Log {self.log_id} - {self.person.full_name} - {self.created_at}"
```

---

## Domain 2: PROJECT (FD6-FD10)

**File**: `apps/projects/models.py`

### Common Imports
```python
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
```

---

### FD6 - Project Model

```python
class Project(models.Model):
    """
    FD6: project_id → title, description, status, visibility, project_slug,
                      project_user_id, log_id, grant_id

    Main project entity.
    Functional Dependency: project_slug → project_id (AK)
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
        ('CANCELLED', 'Cancelled'),
    ]

    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('MISSING', 'Missing'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='PRIVATE'
    )
    project_slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly identifier (AK)"
    )
    grant = models.ForeignKey(
        'Grant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference to ProjectLog"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project_slug']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.project_slug:
            self.project_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
```

---

### FD7 - Grant Model

```python
class Grant(models.Model):
    """
    FD7: grant_id → grant_title, grant_organization, funding_start_date,
                    funding_end_date, grant_note

    Funding source for projects.
    """
    grant_title = models.CharField(max_length=255)
    grant_organization = models.CharField(
        max_length=255,
        help_text="Funding agency/organization"
    )
    funding_start_date = models.DateField()
    funding_end_date = models.DateField()
    grant_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grants'
        ordering = ['-funding_start_date']
        indexes = [
            models.Index(fields=['grant_organization']),
            models.Index(fields=['funding_start_date', 'funding_end_date']),
        ]

    def __str__(self):
        return f"{self.grant_title} ({self.grant_organization})"

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.funding_start_date <= today <= self.funding_end_date
```

---

### FD8 - Project Request Model

```python
class ProjectRequest(models.Model):
    """
    FD8: request_id → project_id, request_type, status, requested_by_user_id,
                      decided_by_user_id, log_id

    Track project-related requests (creation, export, transfer, import).
    """
    REQUEST_TYPE_CHOICES = [
        ('CREATION', 'Project Creation'),
        ('EXPORT', 'Data Export'),
        ('TRANSFER', 'Project Transfer'),
        ('IMPORT', 'Data Import'),
    ]

    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='requests'
    )
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES
    )
    status = models.CharField(
        max_length=20,
        help_text="PENDING, APPROVED, DENIED, etc."
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requests_made'
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests_decided'
    )
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Audit log reference"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'project_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['request_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.project.title} ({self.status})"
```

---

### FD9 - Project Log Model

```python
class ProjectLog(models.Model):
    """
    FD9: log_id → project_id, project_log

    Audit trail for project changes.
    """
    log_id = models.CharField(
        max_length=100,
        primary_key=True
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='logs'
    )
    project_log = models.TextField(
        help_text="JSON or text log of changes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'project_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'created_at']),
        ]

    def __str__(self):
        return f"Log {self.log_id} - {self.project.title}"
```

---

### FD10 - Project Sample Pivot Model

```python
class ProjectSamplePivot(models.Model):
    """
    FD10: project_sample_id → project_id, sample_id, log_id, project_sample_log

    Many-to-many relationship between projects and samples with audit trail.
    """
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='sample_links'
    )
    sample = models.ForeignKey(
        'samples.Sample',
        on_delete=models.CASCADE,
        related_name='project_links'
    )
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Audit log reference"
    )
    project_sample_log = models.TextField(
        blank=True,
        help_text="Changes to this relationship"
    )
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'project_sample_pivot'
        unique_together = [['project', 'sample']]
        ordering = ['project', 'added_at']
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['sample']),
            models.Index(fields=['added_at']),
        ]

    def __str__(self):
        return f"{self.project.title} ↔ {self.sample.sample_name}"
```

---

## Domain 3: SAMPLE (FD11-FD15)

**File**: `apps/samples/models.py`

### Common Imports
```python
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
```

---

### FD11 - Sample Model

```python
class Sample(models.Model):
    """
    FD11: sample_id → sample_name, sample_type, analysis_progress,
                      storage_location_id, log_id, analysis_id, IGSN,
                      flag_value, disbursement_id, movement_id

    Core sample entity.
    """
    sample_name = models.CharField(max_length=255)
    sample_type = models.CharField(
        max_length=100,
        help_text="Tephra, sediment, volcanic rock, etc."
    )
    analysis_progress = models.CharField(
        max_length=50,
        blank=True,
        help_text="Status of analysis workflow"
    )
    storage_location_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Physical storage location"
    )
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Audit log reference"
    )
    analysis = models.ForeignKey(
        'analyses.Analysis',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='samples'
    )
    igsn = models.CharField(
        max_length=9,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^[A-Z0-9]{9}$')],
        help_text="International GeoSample Number"
    )
    flag_value = models.CharField(
        max_length=50,
        blank=True,
        help_text="Sample status flag"
    )
    disbursement = models.ForeignKey(
        'SampleDisbursement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='samples'
    )
    movement = models.ForeignKey(
        'PhysicalSampleMovement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='samples'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'samples'
        ordering = ['sample_name']
        indexes = [
            models.Index(fields=['sample_name']),
            models.Index(fields=['sample_type']),
            models.Index(fields=['igsn']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.sample_name
```

---

### FD12 - Flag Model

```python
class Flag(models.Model):
    """
    FD12: flag_value → sample_id, name, description, log_id

    Sample status flags (archived, missing, etc.).
    """
    flag_value = models.CharField(
        max_length=50,
        primary_key=True,
        help_text="Unique flag identifier"
    )
    sample = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
        related_name='flags'
    )
    name = models.CharField(
        max_length=100,
        help_text="Flag display name"
    )
    description = models.TextField(blank=True)
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Audit log reference"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sample_flags'
        ordering = ['sample', 'created_at']
        indexes = [
            models.Index(fields=['sample']),
        ]

    def __str__(self):
        return f"{self.name} - {self.sample.sample_name}"
```

---

### FD13 - Location History Model

```python
class LocationHistory(models.Model):
    """
    FD13: location_history_id → sample_id, storage_location_id,
                                 acquisition_timestamp, person_id, qty_value,
                                 qty_unit_code, notes, movement_id, longitude,
                                 latitude, location_name

    Track sample location over time.
    """
    sample = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
        related_name='location_history'
    )
    storage_location_id = models.CharField(
        max_length=100,
        help_text="Storage facility identifier"
    )
    acquisition_timestamp = models.DateTimeField()
    person = models.ForeignKey(
        'accounts.Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Person who acquired/moved the sample"
    )
    qty_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Quantity of sample"
    )
    qty_unit_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="grams, kg, liters, etc."
    )
    notes = models.TextField(blank=True)
    movement = models.ForeignKey(
        'PhysicalSampleMovement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    location_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Human-readable location"
    )

    class Meta:
        db_table = 'location_history'
        ordering = ['-acquisition_timestamp']
        indexes = [
            models.Index(fields=['sample', 'acquisition_timestamp']),
            models.Index(fields=['storage_location_id']),
        ]

    def __str__(self):
        return f"{self.sample.sample_name} - {self.location_name} ({self.acquisition_timestamp})"
```

---

### FD14 - Sample Disbursement Model

```python
class SampleDisbursement(models.Model):
    """
    FD14: disbursement_id → parent_sample_id, child_sample_id,
                            recipient_project_id, sender_project_id,
                            quantity_disbursed, disbursement_date, authorized_by

    Track sample subdivision and distribution.
    """
    parent_sample = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
        related_name='disbursements_as_parent'
    )
    child_sample = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
        related_name='disbursements_as_child'
    )
    recipient_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_disbursements'
    )
    sender_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_disbursements'
    )
    quantity_disbursed = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    disbursement_date = models.DateField()
    authorized_by = models.CharField(
        max_length=255,
        help_text="Person who authorized disbursement"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sample_disbursements'
        ordering = ['-disbursement_date']
        indexes = [
            models.Index(fields=['parent_sample', 'disbursement_date']),
            models.Index(fields=['child_sample']),
        ]

    def __str__(self):
        return f"{self.parent_sample.sample_name} → {self.child_sample.sample_name} ({self.quantity_disbursed})"
```

---

### FD15 - Physical Sample Movement Model

```python
class PhysicalSampleMovement(models.Model):
    """
    FD15: movement_id → sample_id, moved_from_location, moved_to_location,
                        sender_name, sender_institution, recipient_name,
                        recipient_institution, quantity_disbursed, disbursement_date

    Track physical transfer of samples between institutions.
    """
    sample = models.ForeignKey(
        'Sample',
        on_delete=models.CASCADE,
        related_name='movements'
    )
    moved_from_location = models.CharField(max_length=255)
    moved_to_location = models.CharField(max_length=255)
    sender_name = models.CharField(max_length=255)
    sender_institution = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255)
    recipient_institution = models.CharField(max_length=255)
    quantity_disbursed = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    disbursement_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'physical_sample_movements'
        ordering = ['-disbursement_date']
        indexes = [
            models.Index(fields=['sample', 'disbursement_date']),
            models.Index(fields=['sender_institution']),
            models.Index(fields=['recipient_institution']),
        ]

    def __str__(self):
        return f"{self.sample.sample_name}: {self.sender_institution} → {self.recipient_institution}"
```

---

## Domain 4: ANALYSIS (FD16-FD18)

**File**: `apps/analyses/models.py`

### Common Imports
```python
from django.db import models
from django.conf import settings
```

---

### FD16 - Analysis Sample Bridge Model

```python
class AnalysisSampleBridge(models.Model):
    """
    FD16: analysis_sample_id → analysis_id, sample_id, analysis_sample_log

    Many-to-many bridge between analyses and samples.
    """
    analysis = models.ForeignKey(
        'Analysis',
        on_delete=models.CASCADE,
        related_name='sample_links'
    )
    sample = models.ForeignKey(
        'samples.Sample',
        on_delete=models.CASCADE,
        related_name='analysis_links'
    )
    analysis_sample_log = models.TextField(
        blank=True,
        help_text="Log of changes to this relationship"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_sample_bridge'
        unique_together = [['analysis', 'sample']]
        ordering = ['analysis', 'sample']
        indexes = [
            models.Index(fields=['analysis']),
            models.Index(fields=['sample']),
        ]

    def __str__(self):
        return f"Analysis {self.analysis.pk} ↔ {self.sample.sample_name}"
```

---

### FD17 - Analysis Model

```python
class Analysis(models.Model):
    """
    FD17: analysis_id → sample_id, person_id, user_id, project_id,
                        instrument_id, batch_id, notes, date_analysis_performed,
                        file_id, branch_id, log_id

    Core analysis entity linking samples to analytical workflows.
    """
    sample = models.ForeignKey(
        'samples.Sample',
        on_delete=models.CASCADE,
        related_name='analyses'
    )
    person = models.ForeignKey(
        'accounts.Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Person who performed analysis"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User account who created record"
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    instrument_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference to instrument used"
    )
    batch = models.ForeignKey(
        'data_management.Batch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    date_analysis_performed = models.DateField()
    file_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference to data files"
    )
    branch_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Link to specific analysis workflow (physical/micro/geochem)"
    )
    log_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Audit log reference"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analyses'
        ordering = ['-date_analysis_performed']
        indexes = [
            models.Index(fields=['sample', 'date_analysis_performed']),
            models.Index(fields=['project']),
            models.Index(fields=['branch_id']),
        ]

    def __str__(self):
        return f"Analysis {self.pk} - {self.sample.sample_name} ({self.date_analysis_performed})"
```

---

### FD18 - Analysis Instrument Model

```python
class AnalysisInstrument(models.Model):
    """
    FD18: analysis_instrument_id → analysis_id, instrument_id, settings_note

    Link analyses to instruments with settings documentation.
    """
    analysis = models.ForeignKey(
        'Analysis',
        on_delete=models.CASCADE,
        related_name='instrument_links'
    )
    instrument = models.ForeignKey(
        'data_management.Instrument',
        on_delete=models.CASCADE,
        related_name='analysis_links'
    )
    settings_note = models.TextField(
        blank=True,
        help_text="Instrument settings and parameters used"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_instruments'
        unique_together = [['analysis', 'instrument']]
        ordering = ['analysis']
        indexes = [
            models.Index(fields=['analysis']),
            models.Index(fields=['instrument']),
        ]

    def __str__(self):
        return f"Analysis {self.analysis.pk} on {self.instrument.instrument_name}"
```

---

## Domain 5: PHYSICAL WORKFLOWS (FD19-FD25)

**File**: `apps/physical_analyses/models.py`

### Common Imports
```python
from django.db import models
```

---

### FD19 - Macro Characteristics Model

```python
class MacroCharacteristics(models.Model):
    """
    FD19: branch_id → particle_size, petrography, alteration_hydration,
                      color_of_juvenile_components, glass_color, grain_morphology,
                      clast_morphology, internal_clast_fabric, groundmass_crystallinity,
                      componentry, vesicularity_of_juvenile_clasts,
                      method_of_estimating_vesicularity

    Physical analysis: macroscopic sample characteristics.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    particle_size = models.CharField(max_length=100, blank=True)
    petrography = models.CharField(max_length=100, blank=True)
    alteration_hydration = models.CharField(max_length=100, blank=True)
    color_of_juvenile_components = models.CharField(max_length=100, blank=True)
    glass_color = models.CharField(max_length=100, blank=True)
    grain_morphology = models.CharField(max_length=100, blank=True)
    clast_morphology = models.CharField(max_length=100, blank=True)
    internal_clast_fabric = models.CharField(max_length=100, blank=True)
    groundmass_crystallinity = models.CharField(max_length=100, blank=True)
    componentry = models.CharField(max_length=100, blank=True)
    vesicularity_of_juvenile_clasts = models.CharField(max_length=100, blank=True)
    method_of_estimating_vesicularity = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'macro_characteristics'
        verbose_name_plural = 'Macro characteristics'

    def __str__(self):
        return f"Macro Characteristics - Branch {self.branch_id}"
```

---

### FD20 - Componentry Model

```python
class Componentry(models.Model):
    """
    FD20: branch_id → size_fraction_analyzed, total_amount_of_sample_analyzed,
                      juvenile_vesicular_type, mass_percent_juvenile_vesicular_type,
                      description_of_juvenile_vesicular_type, juvenile_dense_type,
                      mass_percent_juvenile_dense_type, description_juvenile_dense_type,
                      lithic_type, mass_percent_lithic_type, description_lithic_type,
                      free_crystals, mass_percent_free_crystals, description_free_crystals

    Physical analysis: componentry breakdown.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    size_fraction_analyzed = models.CharField(max_length=100, blank=True)
    total_amount_of_sample_analyzed = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
    )
    juvenile_vesicular_type = models.CharField(max_length=100, blank=True)
    mass_percent_juvenile_vesicular_type = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    description_of_juvenile_vesicular_type = models.TextField(blank=True)
    juvenile_dense_type = models.CharField(max_length=100, blank=True)
    mass_percent_juvenile_dense_type = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    description_juvenile_dense_type = models.TextField(blank=True)
    lithic_type = models.CharField(max_length=100, blank=True)
    mass_percent_lithic_type = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    description_lithic_type = models.TextField(blank=True)
    free_crystals = models.CharField(max_length=100, blank=True)
    mass_percent_free_crystals = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    description_free_crystals = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'componentry'
        verbose_name_plural = 'Componentry analyses'

    def __str__(self):
        return f"Componentry - Branch {self.branch_id}"
```

---

### FD21 - Particle Size Distribution Model

```python
class ParticleSizeDistribution(models.Model):
    """
    FD21: branch_id → how_sampled, particle_size_method, lot_grn_fractions,
                      median_particle_size, sorting, skewness, grain_size_data_reporting

    Physical analysis: particle size distribution.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    how_sampled = models.CharField(max_length=255, blank=True)
    particle_size_method = models.CharField(max_length=255, blank=True)
    lot_grn_fractions = models.CharField(
        max_length=255,
        blank=True,
        help_text="Grain size fractions analyzed"
    )
    median_particle_size = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Median grain size (mm or phi)"
    )
    sorting = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True
    )
    skewness = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True
    )
    grain_size_data_reporting = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'particle_size_distribution'
        verbose_name_plural = 'Particle size distributions'

    def __str__(self):
        return f"PSD - Branch {self.branch_id}"
```

---

### FD22 - Maximum Clast Measurements Model

```python
class MaximumClastMeasurements(models.Model):
    """
    FD22: branch_id → how_sampled, sample_standardization_metric,
                      maximum_clast_measurement_method, performed_in_field_or_laboratory

    Physical analysis: maximum clast size measurements.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    how_sampled = models.CharField(max_length=255, blank=True)
    sample_standardization_metric = models.CharField(max_length=255, blank=True)
    maximum_clast_measurement_method = models.CharField(max_length=255, blank=True)
    performed_in_field_or_laboratory = models.CharField(
        max_length=50,
        blank=True,
        choices=[('FIELD', 'Field'), ('LABORATORY', 'Laboratory')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'maximum_clast_measurements'
        verbose_name_plural = 'Maximum clast measurements'

    def __str__(self):
        return f"Max Clast - Branch {self.branch_id}"
```

---

### FD23 - Density Model

```python
class Density(models.Model):
    """
    FD23: branch_id → density_method, juvenile_clast_density,
                      nonjuvenile_clast_density, deposit_density

    Physical analysis: density measurements.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    density_method = models.CharField(max_length=255, blank=True)
    juvenile_clast_density = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="g/cm³"
    )
    nonjuvenile_clast_density = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="g/cm³"
    )
    deposit_density = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="g/cm³"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'density'
        verbose_name_plural = 'Density measurements'

    def __str__(self):
        return f"Density - Branch {self.branch_id}"
```

---

### FD24 - Core Measurements Model

```python
class CoreMeasurements(models.Model):
    """
    FD24: branch_id → core_id, core_logging, core_imaging

    Physical analysis: sediment core measurements.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    core_id = models.CharField(max_length=100)
    core_logging = models.TextField(
        blank=True,
        help_text="Core description and logging data"
    )
    core_imaging = models.TextField(
        blank=True,
        help_text="Core imaging details"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_measurements'
        verbose_name_plural = 'Core measurements'

    def __str__(self):
        return f"Core {self.core_id} - Branch {self.branch_id}"
```

---

### FD25 - Cryptotephra Model

```python
class Cryptotephra(models.Model):
    """
    FD25: branch_id → type_of_material, identification_method,
                      type_of_cryptotephra_analysis, processing_method,
                      cryptotephra_prospecting_method

    Physical analysis: cryptotephra (hidden tephra) identification.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    type_of_material = models.CharField(max_length=100, blank=True)
    identification_method = models.CharField(max_length=255, blank=True)
    type_of_cryptotephra_analysis = models.CharField(max_length=255, blank=True)
    processing_method = models.CharField(max_length=255, blank=True)
    cryptotephra_prospecting_method = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cryptotephra'
        verbose_name_plural = 'Cryptotephra analyses'

    def __str__(self):
        return f"Cryptotephra - Branch {self.branch_id}"
```

---

## Domain 6: MICROANALYSIS (FD26-FD30)

**File**: `apps/microanalyses/models.py`

### Common Imports
```python
from django.db import models
```

---

### FD26 - Polarizing Microscope Model

```python
class PolarizingMicroscope(models.Model):
    """
    FD26: branch_id → image_instrument_id, sample_mount_id, type_of_material_analyzed,
                      magnifications, area_imaged_field_view, analysis_methods,
                      ground_mass_description, phases_identified, phase_proportions,
                      phase_proportion_method, phase_spatial_distribution,
                      crystal_size_analyzed, crystal_shape_analysis,
                      mineral_zoning_phase_analysis, glass_shard_morphology,
                      grain_morphology_method, shard_alteration, vesicle_shape_analysis,
                      vesicle_proportion_bubble_number_density

    Microanalysis: polarizing microscope observations.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    image_instrument_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference to imaging instrument"
    )
    sample_mount_id = models.CharField(max_length=100, blank=True)
    type_of_material_analyzed = models.CharField(max_length=255, blank=True)
    magnifications = models.CharField(max_length=100, blank=True)
    area_imaged_field_view = models.CharField(max_length=100, blank=True)
    analysis_methods = models.TextField(blank=True)
    ground_mass_description = models.TextField(blank=True)
    phases_identified = models.TextField(blank=True)
    phase_proportions = models.TextField(blank=True)
    phase_proportion_method = models.CharField(max_length=255, blank=True)
    phase_spatial_distribution = models.TextField(blank=True)
    crystal_size_analyzed = models.TextField(blank=True)
    crystal_shape_analysis = models.TextField(blank=True)
    mineral_zoning_phase_analysis = models.TextField(blank=True)
    glass_shard_morphology = models.TextField(blank=True)
    grain_morphology_method = models.CharField(max_length=255, blank=True)
    shard_alteration = models.TextField(blank=True)
    vesicle_shape_analysis = models.TextField(blank=True)
    vesicle_proportion_bubble_number_density = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'polarizing_microscope'
        verbose_name_plural = 'Polarizing microscope analyses'

    def __str__(self):
        return f"Polarizing Microscope - Branch {self.branch_id}"
```

---

### FD27 - Electron Imaging Element Map Model

```python
class ElectronImagingElementMap(models.Model):
    """
    FD27: branch_id → image_instrument_id, sample_mount_id, type_of_material_analyzed,
                      description_of_materials_analyzed, glass_or_groundmass_description,
                      componentry, surface_morphology, quantitative_surface_measurements,
                      general_observations, phases_identified, phase_proportions,
                      phase_proportion_method, phase_spatial_distribution,
                      crystal_shape_analysis, crystal_size_analysis

    Microanalysis: electron microscopy and element mapping.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    type_of_material_analyzed = models.CharField(max_length=255, blank=True)
    description_of_materials_analyzed = models.TextField(blank=True)
    glass_or_groundmass_description = models.TextField(blank=True)
    componentry = models.TextField(blank=True)
    surface_morphology = models.TextField(blank=True)
    quantitative_surface_measurements = models.TextField(blank=True)
    general_observations = models.TextField(blank=True)
    phases_identified = models.TextField(blank=True)
    phase_proportions = models.TextField(blank=True)
    phase_proportion_method = models.CharField(max_length=255, blank=True)
    phase_spatial_distribution = models.TextField(blank=True)
    crystal_shape_analysis = models.TextField(blank=True)
    crystal_size_analysis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'electron_imaging_element_map'
        verbose_name_plural = 'Electron imaging element maps'

    def __str__(self):
        return f"Electron Imaging - Branch {self.branch_id}"
```

---

### FD28 - Tomography Model

```python
class Tomography(models.Model):
    """
    FD28: branch_id → image_instrument_id, sample_mount_id, material_type,
                      phases_identified, phase_proportions, phase_proportion_method,
                      size_distributions, shape_distributions, connectivity,
                      crystal_number_density, bubble_number_density, particle_number,
                      particle_size_distribution, particle_shapes

    Microanalysis: X-ray or electron tomography.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    material_type = models.CharField(max_length=255, blank=True)
    phases_identified = models.TextField(blank=True)
    phase_proportions = models.TextField(blank=True)
    phase_proportion_method = models.CharField(max_length=255, blank=True)
    size_distributions = models.TextField(blank=True)
    shape_distributions = models.TextField(blank=True)
    connectivity = models.TextField(blank=True)
    crystal_number_density = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        null=True,
        blank=True
    )
    bubble_number_density = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        null=True,
        blank=True
    )
    particle_number = models.IntegerField(null=True, blank=True)
    particle_size_distribution = models.TextField(blank=True)
    particle_shapes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tomography'
        verbose_name_plural = 'Tomography analyses'

    def __str__(self):
        return f"Tomography - Branch {self.branch_id}"
```

---

### FD29 - Other Imaging Data Model

```python
class OtherImagingData(models.Model):
    """
    FD29: branch_id → image_instrument_id, sample_mount_id, type_of_material_analyzed

    Microanalysis: other imaging techniques not covered above.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    type_of_material_analyzed = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'other_imaging_data'
        verbose_name_plural = 'Other imaging data'

    def __str__(self):
        return f"Other Imaging - Branch {self.branch_id}"
```

---

### FD30 - Microanalysis Imaging Data Model

```python
class MicroanalysisImagingData(models.Model):
    """
    FD30: image_instrument_id → analysis_id, file_id, date_of_image_analysis,
                                 instrument_and_image_acquisition_software,
                                 image_acquisition_software, image_processing_software,
                                 types_of_images_collected, sample_volume_imaged,
                                 accelerating_voltage, beam_current, voxel_size,
                                 working_distance, xray_acquisition_mode,
                                 xray_pulse_processing, EDS_dead_time,
                                 area_imaged_field_of_view, pixel_resolution

    Microanalysis: imaging instrument settings and parameters.
    """
    image_instrument_id = models.CharField(
        max_length=100,
        primary_key=True
    )
    analysis = models.ForeignKey(
        'analyses.Analysis',
        on_delete=models.CASCADE,
        related_name='imaging_data'
    )
    file_id = models.CharField(max_length=100, blank=True)
    date_of_image_analysis = models.DateField()
    instrument_and_image_acquisition_software = models.CharField(max_length=255, blank=True)
    image_acquisition_software = models.CharField(max_length=255, blank=True)
    image_processing_software = models.CharField(max_length=255, blank=True)
    types_of_images_collected = models.TextField(blank=True)
    sample_volume_imaged = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        null=True,
        blank=True
    )
    accelerating_voltage = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="kV"
    )
    beam_current = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="nA"
    )
    voxel_size = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="μm"
    )
    working_distance = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="mm"
    )
    xray_acquisition_mode = models.CharField(max_length=100, blank=True)
    xray_pulse_processing = models.CharField(max_length=100, blank=True)
    eds_dead_time = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percent"
    )
    area_imaged_field_of_view = models.CharField(max_length=100, blank=True)
    pixel_resolution = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'microanalysis_imaging_data'
        verbose_name_plural = 'Microanalysis imaging data'

    def __str__(self):
        return f"Imaging Data {self.image_instrument_id}"
```

---

## Domain 7: GEOCHEMICAL (FD31-FD37)

**File**: `apps/geochemical/models.py`

### Common Imports
```python
from django.db import models
```

---

### FD31 - Geochem General Attributes Model

```python
class GeochemGeneralAttributes(models.Model):
    """
    FD31: branch_id → technique, method_name, method_ref, method_date,
                      lab_name, lab_id, lab_location, notes, repeating_analysis

    Geochemical analysis: general metadata applicable to all techniques.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    technique = models.CharField(
        max_length=100,
        help_text="XRF, ICP-MS, EPMA, LA-ICP-MS, SIMS, Geochronology"
    )
    method_name = models.CharField(max_length=255, blank=True)
    method_ref = models.CharField(
        max_length=255,
        blank=True,
        help_text="Reference/citation for method"
    )
    method_date = models.DateField(null=True, blank=True)
    lab_name = models.CharField(max_length=255, blank=True)
    lab_id = models.CharField(max_length=100, blank=True)
    lab_location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    repeating_analysis = models.BooleanField(
        default=False,
        help_text="Is this a repeat analysis?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'geochem_general_attributes'
        verbose_name_plural = 'Geochem general attributes'

    def __str__(self):
        return f"{self.technique} - Branch {self.branch_id}"
```

---

### FD32 - XRF Model

```python
class XRF(models.Model):
    """
    FD32: branch_id → xrf_instrument_id, xrf_lab_location, xrf_sample_id,
                      xrf_type, xray_voltage, xray_current, metal_target,
                      mask_dimensions, interference_correction, calibration_ref,
                      secondary_ref, detection_limit, xrf_methodology,
                      clast_num, xrf_date

    Geochemical analysis: X-ray fluorescence.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    xrf_instrument_id = models.CharField(max_length=100, blank=True)
    xrf_lab_location = models.CharField(max_length=255, blank=True)
    xrf_sample_id = models.CharField(max_length=100, blank=True)
    xrf_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Portable, benchtop, synchrotron"
    )
    xray_voltage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="kV"
    )
    xray_current = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="μA"
    )
    metal_target = models.CharField(
        max_length=50,
        blank=True,
        help_text="Rh, Mo, W, etc."
    )
    mask_dimensions = models.CharField(max_length=100, blank=True)
    interference_correction = models.TextField(blank=True)
    calibration_ref = models.CharField(max_length=255, blank=True)
    secondary_ref = models.CharField(max_length=255, blank=True)
    detection_limit = models.TextField(blank=True)
    xrf_methodology = models.TextField(blank=True)
    clast_num = models.IntegerField(
        null=True,
        blank=True,
        help_text="Clast number analyzed"
    )
    xrf_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'xrf'
        verbose_name = 'XRF'
        verbose_name_plural = 'XRF analyses'

    def __str__(self):
        return f"XRF - Branch {self.branch_id}"
```

---

### FD33 - ICP MS Model

```python
class ICPMS(models.Model):
    """
    FD33: branch_id → icpms_lab_id, icpms_instrument, icpms_type,
                      icpms_lab_location, icpms_lab_sample_id, internal_spike,
                      rf_power, calibration_ref, qc_standard, drift_monitor,
                      analysis_time, reduction_sw, method_ref, sample_id_lab,
                      geochem_phases, sample_type, icpms_date

    Geochemical analysis: Inductively Coupled Plasma Mass Spectrometry.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    icpms_lab_id = models.CharField(max_length=100, blank=True)
    icpms_instrument = models.CharField(max_length=255, blank=True)
    icpms_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Quadrupole, TOF, etc."
    )
    icpms_lab_location = models.CharField(max_length=255, blank=True)
    icpms_lab_sample_id = models.CharField(max_length=100, blank=True)
    internal_spike = models.CharField(
        max_length=100,
        blank=True,
        help_text="Internal standard used"
    )
    rf_power = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Watts"
    )
    calibration_ref = models.CharField(max_length=255, blank=True)
    qc_standard = models.CharField(max_length=255, blank=True)
    drift_monitor = models.CharField(max_length=255, blank=True)
    analysis_time = models.DurationField(null=True, blank=True)
    reduction_sw = models.CharField(
        max_length=255,
        blank=True,
        help_text="Data reduction software"
    )
    method_ref = models.CharField(max_length=255, blank=True)
    sample_id_lab = models.CharField(max_length=100, blank=True)
    geochem_phases = models.TextField(blank=True)
    sample_type = models.CharField(max_length=100, blank=True)
    icpms_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'icpms'
        verbose_name = 'ICP-MS'
        verbose_name_plural = 'ICP-MS analyses'

    def __str__(self):
        return f"ICP-MS - Branch {self.branch_id}"
```

---

### FD34 - EPMA SEM Model

```python
class EPMASEM(models.Model):
    """
    FD34: branch_id → (extensive list of EPMA/SEM parameters)

    Geochemical analysis: Electron Probe Microanalysis / Scanning Electron Microscopy.
    Note: Full attribute list from Kuehn_Lab_Normalization.md should be included.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    # Add all EPMA/SEM specific fields from normalization document
    # (Simplified here - expand based on actual requirements)
    instrument_type = models.CharField(
        max_length=50,
        choices=[('EPMA', 'EPMA'), ('SEM', 'SEM')]
    )
    lab_location = models.CharField(max_length=255, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    accelerating_voltage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="kV"
    )
    beam_current = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="nA"
    )
    spot_size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="μm"
    )
    standards_used = models.TextField(blank=True)
    elements_analyzed = models.TextField(blank=True)
    detection_limits = models.TextField(blank=True)
    analysis_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'epma_sem'
        verbose_name = 'EPMA/SEM'
        verbose_name_plural = 'EPMA/SEM analyses'

    def __str__(self):
        return f"EPMA/SEM - Branch {self.branch_id}"
```

---

### FD35 - LA ICP MS Model

```python
class LAICPMS(models.Model):
    """
    FD35: branch_id → (LA-ICP-MS specific parameters)

    Geochemical analysis: Laser Ablation Inductively Coupled Plasma Mass Spectrometry.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    lab_location = models.CharField(max_length=255, blank=True)
    laser_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Excimer, Nd:YAG, etc."
    )
    wavelength = models.IntegerField(
        null=True,
        blank=True,
        help_text="nm"
    )
    spot_size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="μm"
    )
    laser_energy = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="mJ"
    )
    repetition_rate = models.IntegerField(
        null=True,
        blank=True,
        help_text="Hz"
    )
    calibration_standards = models.TextField(blank=True)
    internal_standard = models.CharField(max_length=100, blank=True)
    elements_analyzed = models.TextField(blank=True)
    analysis_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'la_icpms'
        verbose_name = 'LA-ICP-MS'
        verbose_name_plural = 'LA-ICP-MS analyses'

    def __str__(self):
        return f"LA-ICP-MS - Branch {self.branch_id}"
```

---

### FD36 - SIMS Model

```python
class SIMS(models.Model):
    """
    FD36: branch_id → (SIMS specific parameters)

    Geochemical analysis: Secondary Ion Mass Spectrometry.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    sims_lab_id = models.CharField(max_length=100, blank=True)
    sims_instrument = models.CharField(max_length=255, blank=True)
    beam_current = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="nA"
    )
    spot_size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="μm"
    )
    calibration_refs = models.TextField(blank=True)
    elements_analyzed = models.TextField(blank=True)
    analysis_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sims'
        verbose_name = 'SIMS'
        verbose_name_plural = 'SIMS analyses'

    def __str__(self):
        return f"SIMS - Branch {self.branch_id}"
```

---

### FD37 - Geochronology Model

```python
class Geochronology(models.Model):
    """
    FD37: branch_id → gc_lab_name, gc_lab_location, dating_method,
                      fusing_method, method_ref, gc_sample, material_amount,
                      dated, gc_date, gc_age, error_age, strat_relation,
                      rc_age, rc_age_error, rc_age_datum, rc_age_calibrated,
                      model_details, gc_details

    Geochemical analysis: age dating.
    """
    branch_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Links to Analysis.branch_id"
    )
    gc_lab_name = models.CharField(max_length=255, blank=True)
    gc_lab_location = models.CharField(max_length=255, blank=True)
    dating_method = models.CharField(
        max_length=100,
        blank=True,
        help_text="40Ar/39Ar, U-Pb, 14C, etc."
    )
    fusing_method = models.CharField(max_length=255, blank=True)
    method_ref = models.CharField(max_length=255, blank=True)
    gc_sample = models.CharField(max_length=100, blank=True)
    material_amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
    )
    dated = models.BooleanField(
        default=True,
        help_text="Was dating successful?"
    )
    gc_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date analysis performed"
    )
    gc_age = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Calculated age"
    )
    error_age = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Age error/uncertainty"
    )
    strat_relation = models.TextField(
        blank=True,
        help_text="Stratigraphic relationship"
    )
    rc_age = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Radiocarbon age (14C years BP)"
    )
    rc_age_error = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
    )
    rc_age_datum = models.CharField(
        max_length=100,
        blank=True,
        help_text="BP, AD, BC"
    )
    rc_age_calibrated = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Calibrated radiocarbon age"
    )
    model_details = models.TextField(blank=True)
    gc_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'geochronology'
        verbose_name_plural = 'Geochronology analyses'

    def __str__(self):
        return f"Geochronology - Branch {self.branch_id}"
```

---

## Domain 8: DATA MANAGEMENT (FD38-FD46)

**File**: `apps/data_management/models.py`

### Common Imports
```python
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
import hashlib
```

---

### FD38 - Audit Trail Model

```python
class AuditTrail(models.Model):
    """
    FD38: log_id → action, user_id, performed_at_timestamp, description

    System-wide audit logging.
    """
    log_id = models.CharField(
        max_length=100,
        primary_key=True
    )
    action = models.CharField(
        max_length=100,
        help_text="CREATE, UPDATE, DELETE, EXPORT, etc."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    performed_at_timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(
        help_text="Detailed description of action"
    )

    class Meta:
        db_table = 'audit_trail'
        ordering = ['-performed_at_timestamp']
        indexes = [
            models.Index(fields=['user', 'performed_at_timestamp']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.action} by {self.user} at {self.performed_at_timestamp}"
```

---

### FD39 - Export History Model

```python
class ExportHistory(models.Model):
    """
    FD39: export_id → project_id, exported_by, export_date, format,
                      export_scope, record_count

    Track data exports.
    """
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='exports'
    )
    exported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='exports'
    )
    export_date = models.DateTimeField(auto_now_add=True)
    format = models.CharField(
        max_length=50,
        help_text="CSV, JSON, Excel, etc."
    )
    export_scope = models.CharField(
        max_length=100,
        help_text="What was exported (samples, analyses, etc.)"
    )
    record_count = models.IntegerField(
        help_text="Number of records exported"
    )

    class Meta:
        db_table = 'export_history'
        ordering = ['-export_date']
        verbose_name_plural = 'Export histories'
        indexes = [
            models.Index(fields=['project', 'export_date']),
            models.Index(fields=['exported_by']),
        ]

    def __str__(self):
        return f"Export {self.pk} - {self.project.title} ({self.format}) - {self.export_date}"
```

---

### FD40 - Export Request Model

```python
class ExportRequest(models.Model):
    """
    FD40: request_id → requestor_id, project_id, request_timestamp,
                       status, reviewed_by

    Track export approval workflow.
    """
    requestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='export_requests_made'
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='export_requests'
    )
    request_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('DENIED', 'Denied'),
        ],
        default='PENDING'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='export_requests_reviewed'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'export_requests'
        ordering = ['-request_timestamp']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['requestor']),
        ]

    def __str__(self):
        return f"Export Request {self.pk} - {self.project.title} ({self.status})"
```

---

### FD41 - Import Job Model

```python
class ImportJob(models.Model):
    """
    FD41: import_id → project_id, imported_by, import_date, file_name,
                      file_type, validation_status, records_created

    Track data imports.
    """
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='imports'
    )
    imported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='imports'
    )
    import_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(
        max_length=50,
        help_text="CSV, JSON, Excel, etc."
    )
    validation_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('VALID', 'Valid'),
            ('INVALID', 'Invalid'),
            ('ERROR', 'Error'),
        ],
        default='PENDING'
    )
    records_created = models.IntegerField(
        default=0,
        help_text="Number of records successfully imported"
    )
    error_log = models.TextField(
        blank=True,
        help_text="Validation errors or import issues"
    )

    class Meta:
        db_table = 'import_jobs'
        ordering = ['-import_date']
        indexes = [
            models.Index(fields=['project', 'import_date']),
            models.Index(fields=['validation_status']),
        ]

    def __str__(self):
        return f"Import {self.pk} - {self.file_name} ({self.validation_status})"
```

---

### FD42 - File Model

```python
class File(models.Model):
    """
    FD42: file_id → filename, media_type, type_size, checksum_sha256,
                    storage_uri, uploaded_by, uploaded_at, description

    Track uploaded files and data.
    """
    filename = models.CharField(max_length=255)
    media_type = models.CharField(
        max_length=100,
        help_text="MIME type"
    )
    type_size = models.BigIntegerField(
        help_text="File size in bytes"
    )
    checksum_sha256 = models.CharField(
        max_length=64,
        help_text="SHA-256 hash for integrity verification"
    )
    storage_uri = models.CharField(
        max_length=500,
        help_text="File location (S3, filesystem path, etc.)"
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_files'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'files'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['checksum_sha256']),
            models.Index(fields=['uploaded_by', 'uploaded_at']),
        ]

    def __str__(self):
        return f"{self.filename} ({self.media_type})"

    @staticmethod
    def calculate_sha256(file_obj):
        """Calculate SHA-256 hash of a file."""
        sha256 = hashlib.sha256()
        for chunk in file_obj.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()
```

---

### FD43 - Batch Model

```python
class Batch(models.Model):
    """
    FD43: batch_id → instrument_id, created_by, created_at, started_at,
                     fully_uploaded_at, status, notes

    Analytical batches for instrument runs.
    """
    instrument = models.ForeignKey(
        'Instrument',
        on_delete=models.CASCADE,
        related_name='batches'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    fully_uploaded_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='PENDING'
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'batches'
        ordering = ['-created_at']
        verbose_name_plural = 'Batches'
        indexes = [
            models.Index(fields=['instrument', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Batch {self.pk} - {self.instrument.instrument_name} ({self.status})"
```

---

### FD44 - Instrument Model

```python
class Instrument(models.Model):
    """
    FD44: instrument_id → instrument_name, manufacturer, model, serial_no,
                          lab_location, date_acquired, operator_id, status

    Laboratory instruments.
    """
    instrument_name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    serial_no = models.CharField(
        max_length=100,
        blank=True,
        help_text="Serial number"
    )
    lab_location = models.CharField(max_length=255)
    date_acquired = models.DateField(null=True, blank=True)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='operated_instruments',
        help_text="Primary operator"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('MAINTENANCE', 'Maintenance'),
            ('RETIRED', 'Retired'),
        ],
        default='ACTIVE'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'instruments'
        ordering = ['instrument_name']
        indexes = [
            models.Index(fields=['lab_location']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.instrument_name} ({self.manufacturer} {self.model})"
```

---

### FD45 - Calibration Data Model

```python
class CalibrationData(models.Model):
    """
    FD45: calibration_id → instrument_id, calibration_date, calibration_method,
                           operator_id, software_version, qc_passed, notes

    Instrument calibration records.
    """
    instrument = models.ForeignKey(
        'Instrument',
        on_delete=models.CASCADE,
        related_name='calibrations'
    )
    calibration_date = models.DateField()
    calibration_method = models.CharField(
        max_length=255,
        help_text="Calibration procedure used"
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Person who performed calibration"
    )
    software_version = models.CharField(
        max_length=100,
        blank=True,
        help_text="Instrument software version"
    )
    qc_passed = models.BooleanField(
        default=True,
        help_text="Quality control check passed"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calibration_data'
        ordering = ['-calibration_date']
        verbose_name_plural = 'Calibration data'
        indexes = [
            models.Index(fields=['instrument', 'calibration_date']),
            models.Index(fields=['qc_passed']),
        ]

    def __str__(self):
        return f"Calibration {self.pk} - {self.instrument.instrument_name} ({self.calibration_date})"
```

---

### FD46 - Calibration Measurement Model

```python
class CalibrationMeasurement(models.Model):
    """
    FD46: measurement_id → calibration_id, analyte, measured_value, units,
                           uncertainty, detection_limit

    Individual measurements from calibration procedures.
    """
    calibration = models.ForeignKey(
        'CalibrationData',
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    analyte = models.CharField(
        max_length=100,
        help_text="Element or compound measured"
    )
    measured_value = models.DecimalField(
        max_digits=15,
        decimal_places=6
    )
    units = models.CharField(
        max_length=50,
        help_text="ppm, wt%, etc."
    )
    uncertainty = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Measurement uncertainty"
    )
    detection_limit = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Minimum detection limit"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calibration_measurements'
        ordering = ['calibration', 'analyte']
        indexes = [
            models.Index(fields=['calibration', 'analyte']),
        ]

    def __str__(self):
        return f"{self.analyte}: {self.measured_value} {self.units} (Cal {self.calibration.pk})"
```

---

## Next Steps

### 1. Install Models in Apps

Copy each domain's model code into the respective `apps/*/models.py` file:

```bash
# Domain 1
cp models_domain_1.py django_app/apps/accounts/models.py

# Domain 2
cp models_domain_2.py django_app/apps/projects/models.py

# ... and so on for all 8 domains
```

### 2. Update App Configurations

In each app's `apps.py`, ensure proper configuration:

```python
# apps/accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'User & Access Management'
```

### 3. Register Models in Admin

Create `admin.py` for each app:

```python
# apps/accounts/admin.py
from django.contrib import admin
from .models import User, UserSession, ProjectUser, Person, PersonLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_admin', 'is_active']

# ... register other models similarly
```

### 4. Create and Run Migrations

```bash
cd django_app
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Test Django Admin

```bash
python manage.py runserver
# Visit: http://localhost:8000/admin
```

---

## Important Notes

1. **Foreign Key Relationships**: All cross-app foreign keys use string references (e.g., `'projects.Project'`)
2. **Primary Keys**: Default AutoField unless specified otherwise (e.g., branch_id as CharField PK)
3. **Indexes**: Added for frequently queried fields and foreign keys
4. **Validation**: Basic validators included; add custom validation as needed
5. **Migrations**: Always review auto-generated migrations before applying
6. **Testing**: Write unit tests for all models before production use

---

## References

- **Source Document**: `Kuehn_Lab_Normalization.md`
- **Setup Scripts**: `django_setup.bat`, `django_setup.sh`
- **Migration Guide**: `DJANGO_MIGRATION_GUIDE.md`
- **Django Documentation**: https://docs.djangoproject.com/en/5.0/

---

**Last Updated**: 2025-11-14
**Version**: 1.0
**Total Models**: 46 across 8 domains
