from django.db import models
from suave.models import Displayable, Ordered, Image
from django.core.urlresolvers import reverse_lazy as reverse


class Event(Displayable):
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2,
        null=True, blank=True)
    location = models.TextField(null=True, blank=True)

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        s = '{:02n}'
        return reverse('suave_calendar:event', kwargs={
            'slug': self.slug,
            'year': self.start.year,
            'month': s.format(self.start.month),
            'day': s.format(self.start.day)
        })


class EventLink(Ordered):
    url = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    information = models.TextField(null=True, blank=True)
    event = models.ForeignKey(Event, related_name='links')


class EventImage(Image):
    event = models.ForeignKey(Event, related_name='images')
    gallery = models.BooleanField(default=True)
