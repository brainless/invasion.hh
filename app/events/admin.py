from django.contrib import admin

from .models import Invasion, Invader, Activity


class InvasionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'default')


admin.site.register(Invasion, InvasionAdmin)


class InvaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'surfer', 'invasion', 'payment_reference')


admin.site.register(Invader, InvaderAdmin)


class ActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Activity, ActivityAdmin)
