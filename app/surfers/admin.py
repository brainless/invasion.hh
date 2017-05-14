from django.contrib import admin

from .models import Surfer


class SurferAdmin(admin.ModelAdmin):
    pass


admin.site.register(Surfer, SurferAdmin)
