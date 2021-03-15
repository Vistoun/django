from django.contrib import admin

# Register your models here.
from django.contrib import admin
# Import všech modelů, které obsahuje models.py
from .models import *
# Registrace modelů v administraci aplikace
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Attachment)