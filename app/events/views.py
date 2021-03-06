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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        return Invader.objects.get(surfer=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['activities'] = Activity.objects.filter(invasion__default=True)
        return ctx


class EventParticipationView(LoginRequiredMixin, TemplateView):
    template_name = 'event_participation.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if kwargs.get('pk', None):
            invasion = Invasion.objects.get(pk=kwargs['pk'])
        else:
            invasion = Invasion.objects.get(default=True)
        invader = Invader.objects.get(invasion=invasion, surfer=self.request.user)
        ctx['event'] = invasion
        ctx['invader'] = invader
        ctx['activities'] = invader.activities.all()

        total = invasion.price + 5
        for x in invader.activities.all():
            if x.price is not None:
                total += x.price
        ctx['total_price'] = total
        ctx['paypal_price'] = round(total + 0.72, 2)
        return ctx


class ParticipantsView(LoginRequiredMixin, TemplateView):
    template_name = 'coming.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['invasion'] = Invasion.objects.get(pk=kwargs['pk'])
        invaders = [inv.surfer for inv in Invader.objects.filter(invasion__id=kwargs.get('pk')).all()]
        ctx['invaders'] = invaders
        return ctx
