from django.db import models


class Activity(models.Model):
    name = models.CharField(max_length=100)
    invasion = models.ForeignKey("events.Invasion")
    description = models.TextField()
    location = models.CharField(max_length=200)
    link = models.URLField()
    price = models.FloatField(blank=True, null=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    def __str__(self):
        return '{} at {}'.format(self.name, self.invasion.name)
