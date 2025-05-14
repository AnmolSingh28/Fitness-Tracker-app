from django.contrib import admin
from .models import Workout, Exercise  # Import your models

# Register your models so they appear in the admin panel
admin.site.register(Workout)
admin.site.register(Exercise)
