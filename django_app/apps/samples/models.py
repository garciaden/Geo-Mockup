from django.db import models
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
