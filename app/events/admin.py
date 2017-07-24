import datetime
import csv
from django.contrib import admin
from django.core.mail import send_mail
from django.http import HttpResponse

from .models import Invasion, Invader, Activity


class InvasionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'default')


admin.site.register(Invasion, InvasionAdmin)


payment_reminder_message = '''
Hallo!
Hope you are doing great and gearing up for the Hamburg Invasion (July 28 - 30, 2017).

You are just a single step away from confirming your registration for the event.
You have already selected your activities, congrats! Now all you need to do is complete the payment.

--------------
Please transfer the fees earliest possible to either of the following:
=PayPal=
Fees: EUR {event_fee_paypal} (including PayPal fees)
http://paypal.me/IsaBurman

=Bank=
Fees: EUR {event_fee_bank}
Name: Isa Burman
IBAN: DE36500105175417497756
BIC: INGDDEFFXXX

Your payment reference is:
{payment_reference}
--------------

To login to your account please go to:
https://www.invasion.hamburg/app/login/

Your username is {username}
--------------

Please notice, that the online payment is available only until coming Sunday the 23rd July. If the online payment hasn't reached our accounts on time, your booked spot on Saturday tour will be unbooked and again available at registration desk on Friday the 28th July. The attendance fee upon arrival is 15€ instead of 10€ so we kindly recommend that you use the online payment.

We look forward to seeing you in Hamburg this July because it's all about you :-)
Cheers!
- The Hamburg Invasion team
'''


class InvaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'surfer', 'surfer_email', 'invasion', 'payment_reference', 'has_paid', 'activity_list')
    actions = ('mark_paid', 'send_payment_reminder', 'download_as_csv')
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

    def send_payment_reminder(self, request, queryset):
        invaders_count = 0
        for invader in queryset.all():
            if invader.payment_confirmed_at:
                continue
            total = invader.invasion.price
            for x in invader.activities.all():
                if x.price is not None:
                    total += x.price
            send_mail(
                'Finish your registration for Hamburg Invasion 2017!',
                payment_reminder_message.format(
                    username=invader.surfer.username,
                    event_fee_bank=total,
                    event_fee_paypal=round(total + 0.72, 2),
                    payment_reference=invader.payment_reference
                ),
                'hello@invasion.hamburg',
                [invader.surfer.email],
                fail_silently=False,
            )
            invaders_count += 1
        if invaders_count == 1:
            message_bit = "1 invader was"
        else:
            message_bit = "%s invaders were" % invaders_count
        self.message_user(request, "%s successfully sent a payment reminder." % message_bit)

    def download_as_csv(self, request, queryset):
        fields = ('ID', 'Surfer', 'Email', 'Payment reference', 'Paid on', 'Activities')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=invaders.csv'
        writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(list(fields))

        for invader in queryset.all():
            surfer = invader.surfer
            row = [invader.id, '%s %s' % (surfer.first_name, surfer.last_name),
                   surfer.email, invader.payment_reference,
                   invader.payment_confirmed_at.strftime('%d/%m/%Y') if invader.payment_confirmed_at else '-',
                   ', '.join([x.name for x in invader.activities.all()])]
            writer.writerow(row)
        return response


admin.site.register(Invader, InvaderAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'invasion', 'price', 'person_limit', 'starts_at', 'ends_at')


admin.site.register(Activity, ActivityAdmin)
