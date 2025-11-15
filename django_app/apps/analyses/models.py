from django.db import models
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
