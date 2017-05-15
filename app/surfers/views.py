from django.views.generic.edit import CreateView
from ipware.ip import get_real_ip
from django.db import transaction
from django.contrib.auth import authenticate, login

from .forms import RegistrationForm
from events.models import Invasion, Invader
from .models import Surfer


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
            Invader.objects.create(
                surfer=self.object,
                invasion=invasion,
                created_from=get_real_ip(self.request)
            )
            login(self.request, self.object)
            return ret
