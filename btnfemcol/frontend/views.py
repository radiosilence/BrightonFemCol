from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

from btnfemcol.frontend import frontend
from btnfemcol import uploaded_images, uploaded_avatars

from btnfemcol.models import Article, User, Page



@frontend.route('/article/<path:slug>')
def show_article(slug):
    page = Article.query.filter_by(slug=slug).first()
    if not article:
        abort(404)
    return render_template('article.html', article=article)


@frontend.route('/<path:slug>')
def show_page(slug):
    page = Page.query.filter_by(slug=slug).first()
    if not page:
        abort(404)
    return render_template('page.html', page=page)

@frontend.route('/')
def home():
    articles = Article.query.filter_by(status='published').all()
    return render_template('home.html', articles=articles, events=[])