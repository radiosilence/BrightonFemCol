import babylon

from django.conf import settings

from suave.models import NavItem

from suave_press.models import Article
from suave_calendar.models import Event

from collections import namedtuple


def brightonfemcol(request):
    def nav():
        return babylon.get('NavCache', request.path)

    def home():
        def sorter(item):
            if isinstance(item, Article):
                return item.published
            else:
                return item.start

        articles = list(babylon.get('HomeArticlesCache'))
        events = list(babylon.get('HomeEventsCache'))
        boxes = []
        boxes.extend(articles)
        boxes.extend(events)
        sorted(boxes, key=sorter)

        return {
            'boxes': boxes
        }

    def twitter():
        return babylon.get('TwitterCache', 1)

    return {
        'home': home(),
        'nav': nav(),
        'twitter': twitter(),
        'SITE_DOMAIN': settings.SITE_DOMAIN,
    }