from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Activity, Invader, Invasion
from .forms import SelectActivitiesForm


class SelectActivitiesView(LoginRequiredMixin, UpdateView):
    template_name = 'select_activities.html'
    model = Invader
    form_class = SelectActivitiesForm
    login_url = '/app/login/'
    redirect_field_name = 'redirect_to'
    success_url = '/app/participation/'

    def get_object(self):
        return Invader.objects.get(surfer=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['activities'] = Activity.objects.filter(invasion__default=True)
        return ctx

    def form_valid(self):
        super().save()


class EventParticipationView(LoginRequiredMixin, TemplateView):
    template_name = 'event_participation.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        invasion = Invasion.objects.get(default=True)
        invader = Invader.objects.get(invasion=invasion, surfer=self.request.user)
        ctx['event'] = invasion
        ctx['invader'] = invader
        ctx['activities'] = invader.activities.all()

        total = invasion.price
        for x in invader.activities.all():
            if x.price is not None:
                total += x.price
        ctx['total_price'] = total
        return ctx
