from django.contrib import admin

from .models import Invasion, Invader


class InvasionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invasion, InvasionAdmin)


class InvaderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invader, InvaderAdmin)
