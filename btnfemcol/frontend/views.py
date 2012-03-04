from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

from btnfemcol.frontend import frontend
from btnfemcol import uploaded_images, uploaded_avatars

from btnfemcol import db, cache

from btnfemcol.models import Article, User, Page, Section

@frontend.before_request
def before_request():
    g.sections = Section.get_live()

@frontend.route('/article/<path:slug>')
def show_article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        return abort(404)
    return render_template('article.html', article=article)

#@cache.memoize(60)
def get_page(slug):
    return Page.query.filter_by(slug=slug, status='live').first()

#@cache.memoize(60)
def get_section(slug):
    return Section.query.filter_by(slug=slug, status='live').first()

#@cache.memoize(5)
def secondary_nav_pages(section_slug):
    return get_section(section_slug).pages.filter_by(status='live').all()


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
        return Article.query.all()

    return show_page(
        'home',
        'welcome',
        template='home.html',
        articles=articles(),
        events=[]
    )