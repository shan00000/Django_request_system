from django.contrib import admin
from .models import SoftwareRequest, RequestCycle

# Register your models here.

admin.site.register(SoftwareRequest)
admin.site.register(RequestCycle)
