from datetime import datetime

from btnfemcol import cache
from btnfemcol.models import Category, Event, Section


def get(cls, slug, status='live', cached=True):
    """Return an object, cached by a few seconds"""
    key = str('%s:%s:%s:first' % (cls.__name__, slug, status))
    instance = cache.get(key)
    if not instance or not cached:
        print "getting", key, "from cache"
        instance = cls.query.filter_by(status=status, slug=slug).first()
        cache.set(key, instance, 10)
    return instance
    
def secondary_nav_pages(section_slug):
    """Return the secondary menu items for normal sections."""
    key = str('%s:secondary_nav_pages' % section_slug)
    instances = cache.get(key)
    if not instances:
        print "getting", key, "from cache"
        instances = get(Section, section_slug).pages.filter_by(
            status='live').all()
        cache.set(key, instances, 30)
    return instances

def secondary_nav_categories():
    """Return the secondary menu items for the articles section."""
    key = 'categories'
    instances = cache.get(key)
    if not instances:
        instances = Category.query.filter_by(status='live').all()
        cache.set(key, instances, 30)
    return instances

def q_events_upcoming(q=None):
    if not q:
        q = Event.query.filter_by(status='live')
    return q.order_by(Event.start.asc()).filter( \
        Event.end > datetime.utcnow())