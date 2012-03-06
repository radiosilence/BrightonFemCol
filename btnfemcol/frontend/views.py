from datetime import datetime

from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

from btnfemcol.frontend import frontend
from btnfemcol import uploaded_images, uploaded_avatars

from btnfemcol import db, cache

from btnfemcol.models import Article, User, Page, Section, Category, Event

@frontend.before_request
def before_request():
    g.sections = Section.get_live()


def get(cls, slug, status='live'):
    return cls.query.filter_by(status=status, slug=slug).first()

def get_page(slug):
    return get(Page, slug)

def get_section(slug):
    return get(Section, slug)

def get_article(slug):
    return get(Article, slug, status='published')

def get_category(slug):
    return get(Category, slug)

def get_event(slug):
    return get(Event, slug)

def secondary_nav_pages(section_slug):
    return get_section(section_slug).pages.filter_by(status='live').all()

def secondary_nav_categories():
    return Category.query.filter_by(status='live').all()

def q_events_upcoming(q=None):
    if not q:
        q = Event.query.filter_by(status='live')
    return q.order_by(Event.start.asc()).filter( \
        Event.end > datetime.utcnow())

@frontend.route('/events')
@frontend.route('/events/<string:type>')
def show_events(type='upcoming'):
    def inner(type, limit=10):
        q = Event.query.filter_by(status='live')
        if type == 'upcoming':
            q = q_events_upcoming(q)
        else:
            q = q.order_by(Event.start.desc()).filter( \
                Event.start < datetime.utcnow())
        return q[:limit]

    return show_page('events', type, template='event_listing.html', events=inner(type))

@frontend.route('/event/<string:slug>')
def show_event(slug):
    event = get_event(slug)
    if not event:
        return abort(404)
    
    g.secondary_nav = secondary_nav_pages('events')
    return render_template('event.html',
        page=event,
        selected_section_slug='events',
        selected_secondary_slug='changeme'
    )


@frontend.route('/articles/<string:category_slug>')
def show_category(category_slug):
    category = get_category(category_slug)
    if not category:
        return abort(404)

    articles = category.articles.filter_by(status='published').all()

    g.secondary_nav = secondary_nav_categories()
    return render_template('category.html',
        category=category,
        articles=articles,
        selected_section_slug='articles',
        selected_secondary_slug=category_slug
    )

@frontend.route('/articles/<string:category_slug>/<string:article_slug>')
def show_article(category_slug, article_slug):
    article = get_article(article_slug)
    if not article:
        return abort(404)
    
    g.secondary_nav = secondary_nav_categories()
    return render_template('article.html',
        article=article,
        selected_section_slug='articles',
        selected_secondary_slug=category_slug
    )

@frontend.route('/<string:slug>')
def show_section(slug):
    section = get_section(slug)
    if not section:
        return abort(404)
    page = section.pages.filter_by(status='live').first()
    if not page:
        return abort(404)
    else:
        page_slug = page.slug
    return show_page(slug, page_slug)


@frontend.route('/<string:section_slug>/<string:page_slug>')
#@cache.memoize(200)
def show_page(section_slug, page_slug, template='page.html',
    **kwargs):
    
    page = get_page(page_slug)

    if not page:
        return abort(404)

    g.secondary_nav = secondary_nav_pages(section_slug)

    return render_template(template,
        page=page,
        selected_section_slug=section_slug,
        selected_secondary_slug=page_slug,
        **kwargs
    )

@frontend.route('/')
def home():
#    @cache.memoize(20)
    def articles():
        return Article.query.filter_by(status='published')[:2]
    def events():
        return q_events_upcoming()[:2]

    first_section = Section.query.filter_by(status='live').first()
    first_page = first_section.pages.filter_by(status='live').first()
    return show_page(
        first_section.slug,
        first_page.slug,
        template='home.html',
        articles=articles(),
        events=events()
    )