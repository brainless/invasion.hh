from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from .models import Surfer


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', _('Register')))
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['nationality'].required = True

    class Meta:
        model = Surfer
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'nationality', 'facebook_link',
                                                 'cs_link', 'bw_link')


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Username/Email'),
        strip=True,
        required=True
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', _('Login')))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                self.user_cache = authenticate(email=username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError(
                        _('Username/email and password do not match')
                    )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', _('Update')))
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['nationality'].required = True

    class Meta:
        model = Surfer
        fields = ('username', 'first_name', 'last_name', 'nationality', 'facebook_link',
                  'cs_link', 'bw_link')
