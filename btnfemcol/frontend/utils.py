from datetime import datetime

from btnfemcol import cache, db
from btnfemcol.models import Category, Event, Section


def get(cls, slug=None, status='live', cached=True):
    """Return an object, cached by a few seconds"""
    key = str('%s:%s:%s:first' % (cls.__name__, slug, status))
    instance = cache.get(key)
    if instance and cached:
        instance = db.session.merge(instance, load=False)
    else:
        if slug:
            instance = cls.query.filter_by(status=status, slug=slug).first()
        else:
            instance = cls.query.filter_by(status=status).first()
        cache.set(key, instance, 10)
    return instance
    
def secondary_nav_pages(section_slug):
    """Return the secondary menu items for normal sections."""
    key = str('%s:secondary_nav_pages' % section_slug)
    instances = cache.get(key)
    if instances:
        sections = []
        for s in instances:
            sections.append(db.session.merge(s, load=False))
        instances = sections
    else:
        section = get(Section, section_slug)
        instances = section.pages.filter_by(
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