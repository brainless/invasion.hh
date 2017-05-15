from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Activity
from .forms import SelectActivitiesForm
from events.models import Invader, get_current_invasion


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
        ctx['activities'] = Activity.objects.filter(invasion=get_current_invasion())
        return ctx
