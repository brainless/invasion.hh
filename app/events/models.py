import random
import string
from django.db import models
from django.conf import settings


def create_payment_reference():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))


class Invasion(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Invader(models.Model):
    surfer = models.ForeignKey(settings.AUTH_USER_MODEL)
    invasion = models.ForeignKey("events.Invasion")
    payment_reference = models.CharField(max_length=40, default=create_payment_reference)

    activities = models.ManyToManyField("events.Activity", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.GenericIPAddressField(blank=True, null=True)

    payment_confirmed_at = models.DateTimeField(blank=True, null=True)


class Activity(models.Model):
    name = models.CharField(max_length=100)
    invasion = models.ForeignKey("events.Invasion")
    description = models.TextField()
    location = models.CharField(max_length=200)
    link = models.URLField()
    price = models.FloatField(blank=True, null=True)
    person_limit = models.IntegerField(blank=True, null=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    def __str__(self):
        return '{} at {}'.format(self.name, self.invasion.name)
