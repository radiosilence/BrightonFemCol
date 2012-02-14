import inspect

from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

import btnfemcol

from btnfemcol.admin import admin

from btnfemcol import uploaded_images, uploaded_avatars
from btnfemcol import db

from btnfemcol.models import User, Article
from btnfemcol.admin.forms import UserEditForm, UserRegistrationForm, \
    ArticleEditForm, LoginForm

from btnfemcol.utils import Auth, AuthError

"""@admin.route('/userreg', methods=['GET', 'POST'])
def home():
    user = User()
    form = UserRegistrationForm(request.form, user)
    save_user(form, user, message="Thanks for registering.")
    return render_template('form.html', form=form, submit='Register')
"""



@admin.route('/your-articles')
def list(type):
    articles = articles.filter_by(author=g.user)
    return render_template('admin_list.html',
        objects=object)

@admin.route('/<string:type>/<int:id>/<string:action>')
def action(type, id, action):
    return id, type


@admin.route('/login', methods=['GET', 'POST'])
def log_in():
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

def save_object(form, object, message="%s saved."):
    if form.validate_on_submit():
        form.populate_obj(object)
        db.session.add(object)
        db.session.commit()
        flash(message % object)

@admin.route('/user/create', methods=['GET', 'POST'])
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
    save_object(form, user)
    return render_template('form.html', form=form, submit=submit)

@admin.route('/article/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    article = Article.query.filter_by(id=id).first()
    form = ArticleEditForm(request.form, article)
    save_object(form, article)
    return render_template('editor.html', form=form, submit='Save')

@admin.route('/article/new')
def create_article():
    article = Article()
    form = ArticleEditForm(request.form, article)
    save_object(form, article)
    return render_template('editor.html', form=form, submit='Create')


@admin.route('/')
def home():
    classes = filter(lambda x: issubclass(x, db.Model),
        [x[1] for x in inspect.getmembers(btnfemcol.models, inspect.isclass)])
    #for member in inspect.getmembers(btnfemcol.models, inspect.isclass):
    #    if issubclass(member[1], db.Model):
    #        classes.append(member)
    return render_template('admin_home.html',
        classes=classes)
