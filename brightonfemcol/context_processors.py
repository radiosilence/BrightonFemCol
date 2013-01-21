from django.conf import settings
from django.shortcuts import get_object_or_404

from suave.models import NavItem

from suave_press.models import Article
from suave_calendar.models import Event

from collections import namedtuple

from suave_press.models import Article
from suave_calendar.models import Event
from brightonfemcol.models import Tweet


def brightonfemcol(request):
    def nav():
        try:
            nav = NavItem.objects.get(text='main')
        except NavItem.DoesNotExist:
            return False

        primary = nav.get_children()
        primary_selected = None
        for item in primary:
            if item.active(request.path, exact=False):
                primary_selected = item

        if primary_selected:
            secondary = primary_selected.get_children()
        else:
            secondary = []
        secondary_selected = None
        for item in secondary:
            if item.active(request.path, exact=True):
                secondary_selected = item
                break
        return {
            'primary': {
                'items': primary,
                'selected': primary_selected,
            },
            'secondary': {
                'items': secondary,
                'selected': secondary_selected
            }
        }

    def home():
        def sorter_date(item):
            if isinstance(item, Article):
                return item.published
            else:
                return item.start
        def sorter_featured(item):
            if item.featured:
                return 0
            else:
                return 1

        articles = list(
            Article.objects.published().order_by('-published')[:5]
        )
        events = list(
            Event.objects.future().order_by('start_date', 'start_time')[:5]
        )
        boxes = articles + events
        boxes = sorted(boxes, key=sorter_date, reverse=True)
        boxes = sorted(boxes, key=sorter_featured)
        boxes[0].first = True
        return {
            'boxes': boxes[:5]
        }

    def tweets(n):
        return Tweet.objects.all().order_by('-created_at')[:n]

    return {
        'home': home(),
        'nav': nav(),
        'tweets': tweets(10),
        'SITE_DOMAIN': settings.SITE_DOMAIN,
    }