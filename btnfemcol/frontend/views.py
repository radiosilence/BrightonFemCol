from datetime import datetime

from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

from btnfemcol.frontend import frontend

from btnfemcol import uploaded_images, uploaded_avatars
from btnfemcol import db, cache, mail

from btnfemcol.models import Article, User, Page, Section, Category, Event

from btnfemcol.frontend.forms import UserRegistrationForm
from btnfemcol.frontend.utils import get, secondary_nav_pages, \
    secondary_nav_categories, q_events_upcoming

from btnfemcol.admin.utils import edit_instance

@frontend.before_request
def before_request():
    g.sections = Section.get_live()


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
    event = get(Event, slug)
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
    category = get(Category, category_slug)
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
@cache.memoize(60)
def show_article(category_slug, article_slug):
    article = get(Article, article_slug, status='published')
    if not article:
        return abort(404)
    
    g.secondary_nav = secondary_nav_categories()
    return render_template('article.html',
        article=article,
        selected_section_slug='articles',
        selected_secondary_slug=category_slug
    )

@frontend.route('/register', methods=['GET', 'POST'])
def register():
    g.secondary_nav = secondary_nav_pages('home')
    return edit_instance(User, UserRegistrationForm,
        edit_template='registration.html')

@frontend.route('/activate/<int:user_id>/<string:reg_code>')
def activate(user_id, reg_code):
    return render_template('registration.html')

@frontend.route('/<string:slug>')
def show_section(slug):
    section = get(Section, slug)
    if not section:
        return abort(404)
    page = section.pages.filter_by(status='live').first()
    if not page:
        return abort(404)
    else:
        page_slug = page.slug
    return show_page(slug, page_slug)


@frontend.route('/<string:section_slug>/<string:page_slug>')
@cache.memoize(10)
def show_page(section_slug, page_slug, template='page.html',
    **kwargs):
    
    page = get(Page, page_slug)

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
@cache.memoize(10)
def home():
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