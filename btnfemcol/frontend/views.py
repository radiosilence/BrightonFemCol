from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

from btnfemcol.frontend import frontend
from btnfemcol import uploaded_images, uploaded_avatars

from btnfemcol.models import Article, User


@frontend.route('/')
def home():
    user = User('jderp', 'derp@derp.com', firstname='James',
        surname='Derpington')
    article = Article('An Article', 'Derp derp', author=user, subtitle="herp")
    return render_template('article.html',
        article=article)