from django.contrib import admin

from .models import Invasion, Invader, Activity


class InvasionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invasion, InvasionAdmin)


class InvaderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invader, InvaderAdmin)


class ActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Activity, ActivityAdmin)
