from django.db import models
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
