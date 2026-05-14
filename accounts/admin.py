from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "role", "is_approved")
    list_filter = ("department", "role", "is_approved")
    search_fields = ("user__username", "user__email", "department", "role")
