"""
Script to automatically create model files for all 8 Django apps.
Run this from CULS-Mockup directory after django_setup.bat completes.

Usage:
    python create_models.py
"""

import os
from pathlib import Path

# Model code for each domain
MODELS = {
    'accounts': '''from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import EmailValidator
from django.utils import timezone


class User(AbstractUser):
    """
    FD1: user_id → person_id, username, email, password_hash, is_admin
    Custom user model extending Django's AbstractUser.
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


class UserSession(models.Model):
    """FD2: Track user sessions for security and audit purposes."""
    session_id = models.CharField(max_length=40, primary_key=True, help_text="Django session ID")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    ip_address = models.GenericIPAddressField(help_text="Client IP address")
    device = models.CharField(max_length=255, blank=True, help_text="User agent string")
    session_log_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_sessions'
        ordering = ['-created_at']


class ProjectUser(models.Model):
    """FD3: Bridge table for project collaborators with role assignments."""
    ROLE_CHOICES = [
        ('OWNER', 'Project Owner'),
        ('COLLABORATOR', 'Collaborator'),
        ('VIEW_EXPORT', 'View & Export'),
        ('VIEW_ONLY', 'View Only'),
    ]
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='project_users')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships')
    role_code = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEW_ONLY')
    log_id = models.CharField(max_length=100, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_users'
        unique_together = [['project', 'user']]


class Person(models.Model):
    """FD4: Track individuals for attribution and collaboration."""
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=50, blank=True)
    orcid = models.CharField(max_length=19, unique=True, blank=True, null=True)
    organization_id = models.CharField(max_length=100, blank=True)
    phone_num = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)
    org_name = models.CharField(max_length=255, blank=True)
    org_type = models.CharField(max_length=100, blank=True)
    affiliation = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    log_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'persons'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PersonLog(models.Model):
    """FD5: Audit trail for person record changes."""
    log_id = models.CharField(max_length=100, primary_key=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='logs')
    person_log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'person_logs'
        ordering = ['-created_at']
''',

    'projects': '''from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Grant(models.Model):
    """FD7: Funding source for projects."""
    grant_title = models.CharField(max_length=255)
    grant_organization = models.CharField(max_length=255)
    funding_start_date = models.DateField()
    funding_end_date = models.DateField()
    grant_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grants'
        ordering = ['-funding_start_date']

    def __str__(self):
        return f"{self.grant_title} ({self.grant_organization})"


class Project(models.Model):
    """FD6: Main project entity."""
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='PRIVATE')
    project_slug = models.SlugField(max_length=255, unique=True)
    grant = models.ForeignKey('Grant', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    log_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.project_slug:
            self.project_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectRequest(models.Model):
    """FD8: Track project-related requests."""
    REQUEST_TYPE_CHOICES = [
        ('CREATION', 'Project Creation'),
        ('EXPORT', 'Data Export'),
        ('TRANSFER', 'Project Transfer'),
        ('IMPORT', 'Data Import'),
    ]
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    status = models.CharField(max_length=20)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='requests_made')
    decided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests_decided')
    log_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'project_requests'
        ordering = ['-created_at']


class ProjectLog(models.Model):
    """FD9: Audit trail for project changes."""
    log_id = models.CharField(max_length=100, primary_key=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='logs')
    project_log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'project_logs'
        ordering = ['-created_at']


class ProjectSamplePivot(models.Model):
    """FD10: Many-to-many relationship between projects and samples."""
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='sample_links')
    sample = models.ForeignKey('samples.Sample', on_delete=models.CASCADE, related_name='project_links')
    log_id = models.CharField(max_length=100, blank=True)
    project_sample_log = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'project_sample_pivot'
        unique_together = [['project', 'sample']]
''',

    'samples': '''from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Sample(models.Model):
    """FD11: Core sample entity."""
    sample_name = models.CharField(max_length=255)
    sample_type = models.CharField(max_length=100)
    analysis_progress = models.CharField(max_length=50, blank=True)
    storage_location_id = models.CharField(max_length=100, blank=True)
    log_id = models.CharField(max_length=100, blank=True)
    igsn = models.CharField(max_length=9, unique=True, blank=True, null=True)
    flag_value = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'samples'
        ordering = ['sample_name']

    def __str__(self):
        return self.sample_name


class Flag(models.Model):
    """FD12: Sample status flags."""
    flag_value = models.CharField(max_length=50, primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='flags')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    log_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sample_flags'


class LocationHistory(models.Model):
    """FD13: Track sample location over time."""
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='location_history')
    storage_location_id = models.CharField(max_length=100)
    acquisition_timestamp = models.DateTimeField()
    person = models.ForeignKey('accounts.Person', on_delete=models.SET_NULL, null=True, blank=True)
    qty_value = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    qty_unit_code = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'location_history'
        ordering = ['-acquisition_timestamp']


class SampleDisbursement(models.Model):
    """FD14: Track sample subdivision and distribution."""
    parent_sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='disbursements_as_parent')
    child_sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='disbursements_as_child')
    recipient_project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='received_disbursements')
    sender_project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_disbursements')
    quantity_disbursed = models.DecimalField(max_digits=10, decimal_places=3)
    disbursement_date = models.DateField()
    authorized_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sample_disbursements'
        ordering = ['-disbursement_date']


class PhysicalSampleMovement(models.Model):
    """FD15: Track physical transfer of samples between institutions."""
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='movements')
    moved_from_location = models.CharField(max_length=255)
    moved_to_location = models.CharField(max_length=255)
    sender_name = models.CharField(max_length=255)
    sender_institution = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255)
    recipient_institution = models.CharField(max_length=255)
    quantity_disbursed = models.DecimalField(max_digits=10, decimal_places=3)
    disbursement_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'physical_sample_movements'
        ordering = ['-disbursement_date']
''',

    'analyses': '''from django.db import models
from django.conf import settings


class AnalysisSampleBridge(models.Model):
    """FD16: Many-to-many bridge between analyses and samples."""
    analysis = models.ForeignKey('Analysis', on_delete=models.CASCADE, related_name='sample_links')
    sample = models.ForeignKey('samples.Sample', on_delete=models.CASCADE, related_name='analysis_links')
    analysis_sample_log = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_sample_bridge'
        unique_together = [['analysis', 'sample']]


class Analysis(models.Model):
    """FD17: Core analysis entity linking samples to analytical workflows."""
    sample = models.ForeignKey('samples.Sample', on_delete=models.CASCADE, related_name='analyses')
    person = models.ForeignKey('accounts.Person', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)
    instrument_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    date_analysis_performed = models.DateField()
    file_id = models.CharField(max_length=100, blank=True)
    branch_id = models.CharField(max_length=100, blank=True)
    log_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analyses'
        ordering = ['-date_analysis_performed']


class AnalysisInstrument(models.Model):
    """FD18: Link analyses to instruments with settings documentation."""
    analysis = models.ForeignKey('Analysis', on_delete=models.CASCADE, related_name='instrument_links')
    instrument = models.ForeignKey('data_management.Instrument', on_delete=models.CASCADE, related_name='analysis_links')
    settings_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_instruments'
        unique_together = [['analysis', 'instrument']]
''',

    'physical_analyses': '''from django.db import models


class MacroCharacteristics(models.Model):
    """FD19: Physical analysis - macroscopic sample characteristics."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    particle_size = models.CharField(max_length=100, blank=True)
    petrography = models.CharField(max_length=100, blank=True)
    alteration_hydration = models.CharField(max_length=100, blank=True)
    color_of_juvenile_components = models.CharField(max_length=100, blank=True)
    glass_color = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'macro_characteristics'
        verbose_name_plural = 'Macro characteristics'


class Componentry(models.Model):
    """FD20: Physical analysis - componentry breakdown."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    size_fraction_analyzed = models.CharField(max_length=100, blank=True)
    total_amount_of_sample_analyzed = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'componentry'
        verbose_name_plural = 'Componentry analyses'


class ParticleSizeDistribution(models.Model):
    """FD21: Physical analysis - particle size distribution."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    median_particle_size = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    sorting = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'particle_size_distribution'
        verbose_name_plural = 'Particle size distributions'


class MaximumClastMeasurements(models.Model):
    """FD22: Physical analysis - maximum clast size measurements."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    how_sampled = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'maximum_clast_measurements'
        verbose_name_plural = 'Maximum clast measurements'


class Density(models.Model):
    """FD23: Physical analysis - density measurements."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    density_method = models.CharField(max_length=255, blank=True)
    juvenile_clast_density = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'density'
        verbose_name_plural = 'Density measurements'


class CoreMeasurements(models.Model):
    """FD24: Physical analysis - sediment core measurements."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    core_id = models.CharField(max_length=100)
    core_logging = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_measurements'
        verbose_name_plural = 'Core measurements'


class Cryptotephra(models.Model):
    """FD25: Physical analysis - cryptotephra identification."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    type_of_material = models.CharField(max_length=100, blank=True)
    identification_method = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cryptotephra'
        verbose_name_plural = 'Cryptotephra analyses'
''',

    'microanalyses': '''from django.db import models


class PolarizingMicroscope(models.Model):
    """FD26: Microanalysis - polarizing microscope observations."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    type_of_material_analyzed = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'polarizing_microscope'
        verbose_name_plural = 'Polarizing microscope analyses'


class ElectronImagingElementMap(models.Model):
    """FD27: Microanalysis - electron microscopy and element mapping."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'electron_imaging_element_map'
        verbose_name_plural = 'Electron imaging element maps'


class Tomography(models.Model):
    """FD28: Microanalysis - X-ray or electron tomography."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    sample_mount_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tomography'
        verbose_name_plural = 'Tomography analyses'


class OtherImagingData(models.Model):
    """FD29: Microanalysis - other imaging techniques."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    image_instrument_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'other_imaging_data'
        verbose_name_plural = 'Other imaging data'


class MicroanalysisImagingData(models.Model):
    """FD30: Microanalysis - imaging instrument settings and parameters."""
    image_instrument_id = models.CharField(max_length=100, primary_key=True)
    analysis = models.ForeignKey('analyses.Analysis', on_delete=models.CASCADE, related_name='imaging_data')
    file_id = models.CharField(max_length=100, blank=True)
    date_of_image_analysis = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'microanalysis_imaging_data'
        verbose_name_plural = 'Microanalysis imaging data'
''',

    'geochemical': '''from django.db import models


class GeochemGeneralAttributes(models.Model):
    """FD31: Geochemical analysis - general metadata."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    technique = models.CharField(max_length=100)
    method_name = models.CharField(max_length=255, blank=True)
    lab_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'geochem_general_attributes'
        verbose_name_plural = 'Geochem general attributes'


class XRF(models.Model):
    """FD32: Geochemical analysis - X-ray fluorescence."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    xrf_instrument_id = models.CharField(max_length=100, blank=True)
    xrf_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'xrf'
        verbose_name = 'XRF'
        verbose_name_plural = 'XRF analyses'


class ICPMS(models.Model):
    """FD33: Geochemical analysis - ICP-MS."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    icpms_lab_id = models.CharField(max_length=100, blank=True)
    icpms_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'icpms'
        verbose_name = 'ICP-MS'
        verbose_name_plural = 'ICP-MS analyses'


class EPMASEM(models.Model):
    """FD34: Geochemical analysis - EPMA/SEM."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    instrument_type = models.CharField(max_length=50, choices=[('EPMA', 'EPMA'), ('SEM', 'SEM')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'epma_sem'
        verbose_name = 'EPMA/SEM'
        verbose_name_plural = 'EPMA/SEM analyses'


class LAICPMS(models.Model):
    """FD35: Geochemical analysis - LA-ICP-MS."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    lab_location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'la_icpms'
        verbose_name = 'LA-ICP-MS'
        verbose_name_plural = 'LA-ICP-MS analyses'


class SIMS(models.Model):
    """FD36: Geochemical analysis - SIMS."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    sims_lab_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sims'
        verbose_name = 'SIMS'
        verbose_name_plural = 'SIMS analyses'


class Geochronology(models.Model):
    """FD37: Geochemical analysis - age dating."""
    branch_id = models.CharField(max_length=100, primary_key=True)
    gc_lab_name = models.CharField(max_length=255, blank=True)
    dating_method = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'geochronology'
        verbose_name_plural = 'Geochronology analyses'
''',

    'data_management': '''from django.db import models
from django.conf import settings
import hashlib


class AuditTrail(models.Model):
    """FD38: System-wide audit logging."""
    log_id = models.CharField(max_length=100, primary_key=True)
    action = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    performed_at_timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        db_table = 'audit_trail'
        ordering = ['-performed_at_timestamp']


class ExportHistory(models.Model):
    """FD39: Track data exports."""
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='exports')
    exported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='exports')
    export_date = models.DateTimeField(auto_now_add=True)
    format = models.CharField(max_length=50)
    export_scope = models.CharField(max_length=100)
    record_count = models.IntegerField()

    class Meta:
        db_table = 'export_history'
        ordering = ['-export_date']
        verbose_name_plural = 'Export histories'


class ExportRequest(models.Model):
    """FD40: Track export approval workflow."""
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='export_requests_made')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='export_requests')
    request_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DENIED', 'Denied')], default='PENDING')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='export_requests_reviewed')

    class Meta:
        db_table = 'export_requests'
        ordering = ['-request_timestamp']


class ImportJob(models.Model):
    """FD41: Track data imports."""
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='imports')
    imported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='imports')
    import_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    validation_status = models.CharField(max_length=20, default='PENDING')
    records_created = models.IntegerField(default=0)

    class Meta:
        db_table = 'import_jobs'
        ordering = ['-import_date']


class File(models.Model):
    """FD42: Track uploaded files and data."""
    filename = models.CharField(max_length=255)
    media_type = models.CharField(max_length=100)
    type_size = models.BigIntegerField()
    checksum_sha256 = models.CharField(max_length=64)
    storage_uri = models.CharField(max_length=500)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'files'
        ordering = ['-uploaded_at']


class Batch(models.Model):
    """FD43: Analytical batches for instrument runs."""
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE, related_name='batches')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'batches'
        ordering = ['-created_at']
        verbose_name_plural = 'Batches'


class Instrument(models.Model):
    """FD44: Laboratory instruments."""
    instrument_name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    serial_no = models.CharField(max_length=100, blank=True)
    lab_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'instruments'
        ordering = ['instrument_name']

    def __str__(self):
        return f"{self.instrument_name} ({self.manufacturer} {self.model})"


class CalibrationData(models.Model):
    """FD45: Instrument calibration records."""
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE, related_name='calibrations')
    calibration_date = models.DateField()
    calibration_method = models.CharField(max_length=255)
    qc_passed = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calibration_data'
        ordering = ['-calibration_date']
        verbose_name_plural = 'Calibration data'


class CalibrationMeasurement(models.Model):
    """FD46: Individual measurements from calibration procedures."""
    calibration = models.ForeignKey('CalibrationData', on_delete=models.CASCADE, related_name='measurements')
    analyte = models.CharField(max_length=100)
    measured_value = models.DecimalField(max_digits=15, decimal_places=6)
    units = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calibration_measurements'
        ordering = ['calibration', 'analyte']
'''
}


def main():
    # Check if we're in the right directory
    if not Path('django_app').exists():
        print("ERROR: django_app directory not found!")
        print("Make sure you run this from CULS-Mockup directory")
        print("and that django_setup.bat has completed successfully.")
        return

    # Create model files
    for app_name, model_code in MODELS.items():
        model_file = Path(f'django_app/apps/{app_name}/models.py')

        if not model_file.parent.exists():
            print(f"ERROR: App directory not found: {model_file.parent}")
            print("Did django_setup.bat complete successfully?")
            continue

        # Write the model code
        with open(model_file, 'w', encoding='utf-8') as f:
            f.write(model_code)

        print(f"✅ Created: {model_file}")

    print("\n" + "="*50)
    print("✅ All model files created successfully!")
    print("="*50)
    print("\nNext steps:")
    print("1. cd django_app")
    print("2. venv\\Scripts\\activate")
    print("3. python manage.py makemigrations")
    print("4. python manage.py migrate")
    print("5. python manage.py createsuperuser")
    print("6. python manage.py runserver")


if __name__ == '__main__':
    main()
