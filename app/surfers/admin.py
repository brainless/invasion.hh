from django.contrib import admin

from .models import Surfer


class SurferAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'nationality', 'date_joined')


admin.site.register(Surfer, SurferAdmin)
