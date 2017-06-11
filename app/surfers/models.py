from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import pycountry


class Surfer(AbstractUser):
    """
    The surfer is the user who registers to the website. The user most probably registered for a particular
    invasion.
    """
    email = models.EmailField(
        _('email address'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    nationality = models.CharField(
        max_length=2,
        choices=[(x.alpha_2, x.name) for x in pycountry.countries],
        blank=True
    )
    facebook_link = models.URLField(blank=True, verbose_name='Facebook profile link')
    cs_link = models.URLField(blank=True, verbose_name='CouchSurfing profile link')
    bw_link = models.URLField(blank=True, verbose_name='BeWelcome profile link')

    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.GenericIPAddressField(null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
