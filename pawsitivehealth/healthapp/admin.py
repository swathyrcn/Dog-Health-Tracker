from django.contrib import admin
from .models import DogProfile, HealthRecord

admin.site.register(DogProfile)
admin.site.register(HealthRecord)
