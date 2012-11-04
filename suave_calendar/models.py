import datetime

from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy as reverse
from django.utils.timezone import utc

from model_utils.managers import PassThroughManager
from suave.models import (Displayable, Ordered, Image, SiteEntityQuerySet,
    Attachment)

from suave.utils import get_default_image


class Category(Displayable):
    @property
    def events(self):
        return Event.objects.live().filter(
            Q(category=self)
            | Q(categories__in=[self])
        ).order_by('start_date')

    class Meta:
        verbose_name_plural = 'categories'


class EventQuerySet(SiteEntityQuerySet):

    def future(self):
        return self.live().filter(
            Q(end_date__gte=datetime.date.today())
            | Q(start_date__gte=datetime.date.today())
        )


    def past(self):
        return self.live().filter(start_date__lte=datetime.date.today())


class Event(Displayable):
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)

    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    category = models.ForeignKey(Category, related_name='primary_events',
        null=True, blank=True,)
    categories = models.ManyToManyField(Category,
        related_name='secondary_events', null=True, blank=True,
        verbose_name="extra categories")

    price = models.DecimalField(max_digits=5, decimal_places=2,
        null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    
    dark_bg = models.BooleanField()
    header_image = models.BooleanField()

    objects = PassThroughManager.for_queryset_class(EventQuerySet)()

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        s = '{:02n}'
        return reverse('suave_calendar:event', kwargs={
            'slug': self.slug,
            'year': self.start_date.year,
            'month': self.start_date.strftime('%B').lower(),
            'day': s.format(self.start_date.day)
        })

    @property
    def start(self):
        time = self.start_time
        date = self.start_date
        if not time:
            time = datetime.time(0, 0)
        return datetime.datetime.combine(date, time).replace(tzinfo=utc)

    @property
    def end(self):
        date = self.end_date
        time = self.end_time
        if not date:
            date = self.start_date
        if not time and self.start_time:
            time = (self.start_time + datetime.timedelta(hours=1))
        elif not time:
            time =  datetime.time(0, 0)
        return datetime.datetime.combine(date, time).replace(tzinfo=utc)

    @property
    def image(self):
        try:
            return self.images.all()[0]
        except IndexError:
            return get_default_image()

    class Meta:
        ordering = ('-start_date',)


class EventLink(Ordered):
    url = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    information = models.CharField(max_length=255, null=True, blank=True)
    event = models.ForeignKey(Event, related_name='links')


class EventImage(Image):
    event = models.ForeignKey(Event, related_name='images')
    gallery = models.BooleanField(default=True)


class EventAttachment(Attachment):
    event = models.ForeignKey(Event, related_name='attachments')


from caches import *
