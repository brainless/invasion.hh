from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Surfer


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = Surfer
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'nationality', 'facebook_link',
                                                 'cs_link', 'bw_link')
