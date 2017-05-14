from django.db import models
from django.contrib.auth import get_user_model


class Invasion(models.Model):
    name = models.CharField(max_length=100)
    surfers = models.ManyToManyField(get_user_model(), through="events.Invader")

    default = models.BooleanField(default=False)


class Invader(models.Model):
    surfer = models.ForeignKey(get_user_model())
    invasion = models.ForeignKey("events.Invasion")
    payment_reference = models.CharField(max_length=40, blank=True)

    activities = models.ManyToManyField("activities.Activity", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.GenericIPAddressField(null=True)

    payment_confirmed_at = models.DateTimeField(blank=True)
