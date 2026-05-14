from django.db import models
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    role_choice = [
        ("academic","Academic"),
        ("cms_it","CMS IT")
    ]
    DEPARTMENT_CHOICES = [
    ("cs", "Computer Science"),
    ("math", "Mathematics"),
    ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=role_choice,
        default="academic"
    )

    is_approved = models.BooleanField(default=False)
    department = models.CharField(max_length=50,choices=DEPARTMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"