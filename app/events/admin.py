import datetime
from django.contrib import admin

from .models import Invasion, Invader, Activity


class InvasionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'default')


admin.site.register(Invasion, InvasionAdmin)


class InvaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'surfer', 'surfer_email', 'invasion', 'payment_reference', 'has_paid', 'activity_list')
    actions = ('mark_paid',)
    search_fields = ('surfer__first_name', 'surfer__last_name', 'surfer__email', 'surfer__username',
                     'payment_reference')

    @staticmethod
    def surfer_email(obj):
        return obj.surfer.email

    def mark_paid(self, request, queryset):
        rows_updated = queryset.update(payment_confirmed_at=datetime.datetime.utcnow())
        if rows_updated == 1:
            message_bit = "1 invader was"
        else:
            message_bit = "%s invaders were" % rows_updated
        self.message_user(request, "%s successfully marked as paid." % message_bit)


admin.site.register(Invader, InvaderAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'invasion', 'price', 'person_limit', 'starts_at', 'ends_at')


admin.site.register(Activity, ActivityAdmin)
