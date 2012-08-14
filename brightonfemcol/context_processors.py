from suave.models import NavItem

from suave_press.models import Article
from suave_calendar.models import Event

def brightonfemcol(request):
    def nav():
        try:
            nav = NavItem.objects.get(text='main')
        except NavItem.DoesNotExist:
            return False

        primary = nav.get_children()
        primary_selected = None
        for item in primary:
            if request.path.startswith(item.url):
                primary_selected = item

        if primary_selected:
            secondary = primary_selected.get_children()
        else:
            secondary = []

        secondary_selected = None
        for item in secondary:
            if request.path == item.url:
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
        return {
            'articles': Article.objects.published()[:3],
            'events': Event.objects.future()[:3]
        }

    return {
        'home': home(),
        'nav': nav()
    }