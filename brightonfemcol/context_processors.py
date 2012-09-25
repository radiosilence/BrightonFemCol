import babylon

from django.conf import settings

from suave.models import NavItem

from suave_press.models import Article
from suave_calendar.models import Event

def brightonfemcol(request):
    def nav():
        return babylon.get('NavCache', request.path)

    def home():
        return {
            'articles': babylon.get('HomeArticlesCache'),
            'events': babylon.get('HomeEventsCache')
        }

    def twitter():
        return babylon.get('TwitterCache', 1)

    return {
        'home': home(),
        'nav': nav(),
        'twitter': twitter(),
        'SITE_DOMAIN': settings.SITE_DOMAIN,
    }