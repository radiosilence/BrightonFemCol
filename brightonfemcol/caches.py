import babylon

from suave.models import NavItem

from suave_press.models import Article
from suave_calendar.models import Event


class NavCache(babylon.Cache):
    model = NavItem
    def generate(self, path=None, *args, **kwargs):
        if not path or not isinstance(path, basestring):
            return False
        try:
            nav = NavItem.objects.get(text='main')
        except NavItem.DoesNotExist:
            return False

        primary = nav.get_children()
        primary_selected = None
        for item in primary:
            if path.startswith(item.url):
                primary_selected = item

        if primary_selected:
            secondary = primary_selected.get_children()
        else:
            secondary = []

        secondary_selected = None
        for item in secondary:
            if path == item.url:
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

babylon.register(NavCache, parents=('PageCache',))

class HomeArticlesCache(babylon.Cache):
    model = Article

    def generate(self, *args, **kwargs):
        return Article.objects.published().order_by('-published')[:3]

babylon.register(HomeArticlesCache, parents=('PageCache',))


class HomeEventsCache(babylon.Cache):
    model = Article

    def generate(self, *args, **kwargs):
        return Event.objects.future().order_by('start_date', 'start_time')[:3]

babylon.register(HomeEventsCache, parents=('PageCache',))
