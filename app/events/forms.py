from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Activity, Invader


class SelectActivitiesForm(forms.ModelForm):
    activities = forms.ModelMultipleChoiceField(queryset=Activity.objects.filter(invasion__default=True))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Save'))

    def clean_activities(self):
        """
        Check if any of the selected activities are already booked out.
        :return:
        """
        data = self.cleaned_data['activities']
        # Here data is a QuerySet of all the selected activities
        fully_booked_activities_error = []
        for act in data:
            if act.person_limit and \
                Invader.objects.filter(activities__in=[act]).exclude(surfer=self.user).count() >= act.person_limit:
                fully_booked_activities_error.append(
                    forms.ValidationError("%(act)s is fully booked :(", params={'act': act.name})
                )
        if fully_booked_activities_error:
            raise forms.ValidationError(fully_booked_activities_error)
        return data

    class Meta:
        model = Invader
        fields = ('activities',)
