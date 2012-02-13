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
    user = User('btnfemcol', 'derp@derp.com', firstname='Brighton',
        surname='Feminist Collective')

    front_text = """
Brighton Feminist Collective is a feminist activist group that started in December 2011,
we are a sex-positive, pro-choice, trans-inclusive, and anti-exploitation group.

Check out our [Facebook Page](http://www.facebook.com/groups/brightonfeminists/) or our [Twitter](http://twitter.com/BrightonFemCol).

Site will soon be updated to have articles, stories, events and information about our constitution, philosophy and organisation.

The links at the top don't work because the site isn't complete.
"""
    article = Article('Coming Soon', front_text, author=user, subtitle="Website still in production.")
    return render_template('article.html',
        article=article)