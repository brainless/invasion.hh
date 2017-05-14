from django.db import models
from django.contrib.auth.models import AbstractUser
import pycountry


class Surfer(AbstractUser):
    """
    The surfer is the user who registers to the website. The user most probably registered for a particular
    invasion.
    """
    nationality = models.CharField(
        max_length=2,
        choices=[(x.alpha_2, x.name) for x in pycountry.countries],
        blank=True
    )
    facebook_link = models.URLField(blank=True)
    cs_link = models.URLField(blank=True)
    bw_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.GenericIPAddressField(null=True)
