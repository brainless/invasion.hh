from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import TemplateView
from ipware.ip import get_real_ip
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from .forms import RegistrationForm, LoginForm, ProfileForm
from events.models import Invasion, Invader
from .models import Surfer


welcome_message = '''
Hallo!
Thank you for registering with Hamburg Invasion 2017.

Please remember to select your tours and complete your registration by transfering the fees.
The online payment will be closing on Sunday the 23rd July.

To login to your account please go to:
https://www.invasion.hamburg/app/login/

Your username is {username}

--------------
Please transfer the registration fee and tour fees (if applicable) earliest possible to either of the following:
=PayPal=
http://paypal.me/IsaBurman

=Bank=
Name: Isa Burman
IBAN: DE36500105175417497756
BIC: INGDDEFFXXX

Your payment reference is:
{payment_reference}
--------------

We look forward to seeing you in Hamburg this July because it's all about you :-)
Cheers!
- The Hamburg Invasion team
'''

class RegistrationView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/app/select-activities/'
    model = Surfer

    def form_valid(self, form):
        form.instance.created_from = get_real_ip(self.request)
        invasion = Invasion.objects.get(default=True)

        with transaction.atomic():
            ret = super().form_valid(form)
            invader = Invader.objects.create(
                surfer=self.object,
                invasion=invasion,
                created_from=get_real_ip(self.request)
            )
            send_mail(
                'Welcome to Hamburg Invasion 2017!',
                welcome_message.format(
                    username=self.object.username,
                    payment_reference=invader.payment_reference
                ),
                'hello@invasion.hamburg',
                [self.object.email],
                fail_silently=False,
            )
            login(self.request, self.object)
            return ret


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/app/dash/'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = '/app/dash/'
    model = Surfer

    def get_object(self):
        return self.request.user


class DashView(LoginRequiredMixin, TemplateView):
    template_name = 'dash.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['invasions'] = [inv.invasion for inv in Invader.objects.filter(surfer=self.request.user).all()]
        return ctx
