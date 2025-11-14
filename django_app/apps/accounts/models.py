from django.db import models
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
