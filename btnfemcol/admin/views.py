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

from btnfemcol.admin.utils import auth_logged_in, auth_allowed_to


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
            flash("Successfully logged in.", 'success')
            return redirect(url_for('admin.home'))
        except AuthError:
            flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form, submit='Login')


@admin.route('/logout')
def logout():
    g.user = None
    del session['logged_in']
    flash('Logged out.')
    return redirect(url_for('admin.login'))


def save_object(form, object, message=u"%s saved."):
    """This function handles the simple cyle of testing if an object's form
    validates and then saving it.
    """
    if request.method == 'POST':
        if not form.validate():
            flash("There were errors saving, see below.", 'error')
            return False
        form.populate_obj(object)
        db.session.add(object)
        db.session.commit()
        flash(message % object.__unicode__(), 'success')
        return object.id
    return False

@admin.route('/user/new', methods=['GET', 'POST'])
@auth_logged_in
def create_user():
    return edit_user()

@admin.route('/user/<int:id>', methods=['GET', 'POST'])
@auth_logged_in
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


@admin.route('/articles')
@auth_logged_in
def list_articles():
    return render_template('articles.html')


@admin.route('/article/<int:id>', methods=['GET', 'POST'])
@auth_logged_in
@auth_allowed_to('write_articles')
def edit_article(id=None):
    if id:
        article = Article.query.filter_by(id=id).first()
        if not article:
            return abort(404)
        submit = 'Update'

        if g.user != article.author and not g.user.allowed_to('manage_articles'):
            return abort(403)
    else:
        article = Article()
        submit = 'Create'
    
    form = ArticleEditForm(request.form, article)

    if not g.user.allowed_to('change_authors'):
        if article.id:
            form.author_id.data = article.author.id
        else:
            form.author_id.data = g.user.id
    
    created = save_object(form, article)
    if created:
        return redirect(url_for('admin.edit_article', id=created))
    return render_template('edit_article.html', form=form, submit=submit)

@admin.route('/article/new', methods=['GET', 'POST'])
@auth_logged_in
@auth_allowed_to('write_articles')
def create_article():
    return edit_article()


def dashboard_writer():
    """This is the dashboard for the writer group type, it just returns the
    article list because that's all writers really need to do.
    """
    return list_articles()


def dashboard_editor():
    """Editor dashboard has things for proof-reading and accepting submitted
    articles, and also writing one's own."""
    return render_template('dashboard_editor.html')


def dashboard_admin():
    """Administrator dashboard will cover page editing, event uploading, user
    management."""
    return render_template('dashboard_admin.html')


def dashboard_superuser():
    """Superuser can anything an admin can, but with the ability to change site
    settings, manage permissions, etc."""
    return render_template('dashboard_superuser.html')


@admin.route('/async/articles/<string:username>/filter/<string:filter>/<int:page>')
@admin.route('/async/articles/<string:username>/<string:status>/<int:page>')
@admin.route('/async/articles/filter/<string:filter>/<int:page>')
@admin.route('/async/articles/<string:status>/<int:page>')
@auth_logged_in
@auth_allowed_to('write_articles')
def json_user_articles(username=None, *args, **kwargs):
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            return abort(404)
    else:
        user = g.user
    
    if g.user != user and not g.user.allowed_to('manage_articles'):
        return abort(403)

    @cache.memoize(5)
    def inner(user, status='any', page=1, per_page=20, filter=None):
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
                'pub_date': a.pub_date.strftime('%c'),
                'urls': {
                    'edit': url_for('admin.edit_article', id=a.id),
                    'bin': '#'
                }
            } for a in articles
        ]})

    return inner(user, *args, **kwargs)

@admin.route('/async/articles/edit-queue')
@auth_logged_in
@auth_allowed_to('manage_articles')
@cache.memoize(5)
def json_articles_edit_queue():
    articles = Article.query.filter_by(status='edit-queue')
    return json.dumps({'articles': [{
            'id': a.id,
            'title': a.title,
            'revision': a.revision,
            'pub_date': a.pub_date.strftime('%c'),
            'author': {
                'fullname': '%s %s' % (a.author.firstname, a.author.surname),
                'url': url_for('admin.edit_user', id=a.author.id)
            },
            'urls': {
                'edit': url_for('admin.edit_article', id=a.id),
                'bin': '#'
            }
        } for a in articles
    ]})

@admin.route('/')
@auth_logged_in
def home():
    # Do some logic to get the right dashboard for the person
    return dashboard_editor()