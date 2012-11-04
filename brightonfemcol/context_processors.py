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

        articles = list(babylon.get('HomeArticlesCache'))
        events = list(babylon.get('HomeEventsCache'))
        boxes = articles + events
        boxes = sorted(boxes, key=sorter_date, reverse=True)
        boxes = sorted(boxes, key=sorter_featured)
        boxes[0].first = True
        return {
            'boxes': boxes[:5]
        }

    def twitter():
        return babylon.get('TwitterCache', 1)

    return {
        'home': home(),
        'nav': nav(),
        'twitter': twitter(),
        'SITE_DOMAIN': settings.SITE_DOMAIN,
    }