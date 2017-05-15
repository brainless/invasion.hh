from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import get_current_invasion, Invader
from activities.models import Activity


class EventParticipationView(LoginRequiredMixin, TemplateView):
    template_name = 'event_participation.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        invasion = get_current_invasion()
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
