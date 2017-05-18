import datetime
from django.contrib import admin

from .models import Invasion, Invader, Activity


class InvasionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'default')


admin.site.register(Invasion, InvasionAdmin)


class InvaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'surfer', 'invasion', 'payment_reference', 'has_paid')
    actions = ('mark_paid',)
    search_fields = ('surfer__first_name', 'surfer__last_name', 'surfer__email', 'surfer__username',
                     'payment_reference')

    def mark_paid(self, request, queryset):
        rows_updated = queryset.update(payment_confirmed_at=datetime.datetime.utcnow())
        if rows_updated == 1:
            message_bit = "1 invader was"
        else:
            message_bit = "%s invaders were" % rows_updated
        self.message_user(request, "%s successfully marked as paid." % message_bit)


admin.site.register(Invader, InvaderAdmin)


class ActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Activity, ActivityAdmin)
