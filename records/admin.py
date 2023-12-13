from django.contrib import admin
from .models import Progress, Sitting

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    pass

@admin.register(Sitting)
class SittingAdmin(admin.ModelAdmin):
    pass