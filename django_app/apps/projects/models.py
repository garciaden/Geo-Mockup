from django.db import models
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
