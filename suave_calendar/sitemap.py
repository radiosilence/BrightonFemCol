from datetime import date

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import Event

try:
    LASTMOD = Event.objects.order_by('-updated')[0].updated
except:
    LASTMOD = date.today()


class CalendarSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return list(Event.objects.live()) + [
            reverse('suave_calendar:home'),
            reverse('suave_calendar:archive')
        ]

    def lastmod(self, obj):
        if isinstance(obj, Event):
            return obj.updated
        else:
            return LASTMOD

    def location(self, obj):
        if isinstance(obj, Event):
            return obj.url
        else:
            return obj
