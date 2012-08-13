from suave.models import NavItem

def brightonfemcol(request):
    def nav():
        try:
            nav = NavItem.objects.get(text='main')
        except NavItem.DoesNotExist:
            return False

        primary = nav.get_children()
        primary_selected = None
        for item in primary:
            if item.url in request.path:
                primary_selected = item
                break

        if primary_selected:
            secondary = primary_selected.get_children()
        else:
            secondary = []

        secondary_selected = None
        for item in secondary:
            if request.path == item.url:
                secondary_selected = item
                break
        print secondary
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

    return {
        'nav': nav()
    }