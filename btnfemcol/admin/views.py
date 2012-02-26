import inspect
import json

from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

import btnfemcol

from btnfemcol.admin import admin

from btnfemcol import uploaded_images, uploaded_avatars
from btnfemcol import db
from btnfemcol import cache

from btnfemcol.models import User, Article
from btnfemcol.admin.forms import UserEditForm, UserRegistrationForm, \
    ArticleEditForm, LoginForm

from btnfemcol.utils import Auth, AuthError

@admin.before_request
def b4():
    users =  User.query.filter_by().all()
    for user in users:
        print user
        print user.articles.all()
@admin.route('/articles')
def list_articles():
    articles = Article.query.all()
    return render_template('admin_list_articles.html',
        articles=articles)

@admin.route('/<string:type>/<int:id>/<string:action>')
def action(type, id, action):
    return id, type


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        a = Auth(session, db, User)
        try:
            g.user = a.log_in(form.username.data, form.password.data)
            session['logged_in'] = g.user.id
            flash("Successfully logged in.")
            return redirect(url_for('admin.home'))
        except AuthError:
            flash('Invalid username or password.')
    return render_template('form.html', form=form, submit='Login')

def save_object(form, object, message=u"%s saved."):
    if form.validate_on_submit():
        form.populate_obj(object)
        db.session.add(object)
        db.session.commit()
        flash(message % object.__unicode__())
        return True
    return False

@admin.route('/user/new', methods=['GET', 'POST'])
def create_user():
    return edit_user()

@admin.route('/user/<int:id>', methods=['GET', 'POST'])
def edit_user(id=None):
    if id:
        user = User.query.filter_by(id=id).first()
        submit = 'Save'
    else:    
        user = User()
        submit = 'Create'
    if not user:
        abort(404)
    form = UserEditForm(request.form, user)
    if save_object(form, user):
        return redirect(url_for('admin.home'))
    return render_template('form.html', form=form, submit=submit)

@admin.route('/article/<int:id>', methods=['GET', 'POST'])
def edit_article(id=None):
    if id:
        article = Article.query.filter_by(id=id).first()
        submit = 'Update'
    else:
        article = Article()
        submit = 'Publish'
    
    form = ArticleEditForm(request.form, article)
    save_object(form, article)
    return render_template('editor.html', form=form, submit=submit)

@admin.route('/article/new', methods=['GET', 'POST'])
def create_article():
    return edit_article()


def dashboard_writer():
    return render_template('articles.html')

@admin.route('/async/articles/<string:user>/filter/<string:filter>/<int:page>')
@admin.route('/async/articles/<string:user>/<string:status>/<int:page>')
def json_user_articles(user, status='any', page=1, per_page=20, filter=None):
    if isinstance(user, basestring):
        user = User.query.filter_by(username=user).first()
        if not user:
            return abort(404)
    
    start = per_page * (page - 1)
    end = per_page * page

    if filter:
        articles = user.articles.filter(
            Article.title.like('%' + filter + '%'))[start:end]
    elif status == 'any':
        articles = user.articles[start:end]
    else:
        articles = user.articles.filter_by(status=status)[start:end]
    
    return json.dumps({'articles': [{
            'id': a.id,
            'title': a.title,
            'revision': a.revision,
            'pub_date': {
                'weekday': a.pub_date.strftime('%a')
            }
        } for a in articles
    ]})

@admin.route('/')
def home():
    # Do some logic to get the right dashboard for the person
    return dashboard_writer()

