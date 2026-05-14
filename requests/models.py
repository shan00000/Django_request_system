from django.db import models
from django.conf import settings

# Create your models here.

class SoftwareRequest(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("in_review", "In Review"),
        ("completed", "Completed"),
        ]
    
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    application_name = models.CharField(max_length=255)
    application_description = models.TextField()
    application_website = models.URLField(blank=True)

    purchase_required = models.BooleanField(default=False)
    need_virtual_desktop = models.BooleanField(default=False)
    alternative_software_has_been_considered = models.BooleanField(default=False)

    license_agreement_detail = models.TextField(blank=True)
    privacy_considered = models.BooleanField(default=False)

    primary_use = models.CharField(max_length=255)
    need_installing_on = models.TextField()
    need_staff_machine = models.BooleanField(default=False)

    anything_else = models.TextField(blank=True)

    start_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted"
    )

    ticket_number = models.CharField(max_length=100, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_name} requested by {self.requested_by.username} - Status: {self.status}"   