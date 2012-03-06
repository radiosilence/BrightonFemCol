from datetime import datetime

from btnfemcol.models import Category, Event, Section


def get(cls, slug, status='live'):
    return cls.query.filter_by(status=status, slug=slug).first()

def secondary_nav_pages(section_slug):
    return get(Section, section_slug).pages.filter_by(status='live').all()

def secondary_nav_categories():
    return Category.query.filter_by(status='live').all()

def q_events_upcoming(q=None):
    if not q:
        q = Event.query.filter_by(status='live')
    return q.order_by(Event.start.asc()).filter( \
        Event.end > datetime.utcnow())