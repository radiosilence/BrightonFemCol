import inspect

from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

import btnfemcol

from btnfemcol.backend import backend

from btnfemcol import uploaded_images, uploaded_avatars
from btnfemcol import db

from btnfemcol.models import User, Article
from btnfemcol.backend.forms import UserEditForm, UserRegistrationForm, \
    ArticleEditForm

"""@backend.route('/userreg', methods=['GET', 'POST'])
def home():
    user = User()
    form = UserRegistrationForm(request.form, user)
    save_user(form, user, message="Thanks for registering.")
    return render_template('form.html', form=form, submit='Register')
"""



@backend.route('/your-articles')
def list(type):

    return render_template('admin_list.html',
        objects=object)

@backend.route('/<string:type>/<int:id>/<string:action>')
def action(type, id, action):
    return id, type


def save_object(form, object, message="%s saved."):
    if form.validate_on_submit():
        if issubclass(object, User):
            if form.password.data == '':
                form.password.data = None
        form.populate_obj(object)
        
        db.session.add(object)
        db.session.commit()
        flash(message % object)

@backend.route('/user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    form = UserRegistrationForm(request.form, user)
    save_object(form, user)
    return render_template('form.html', form=form, submit='Save')

@backend.route('/article/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    article = Article.query.filter_by(id=id).first()
    form = ArticleEditForm(request.form, article)
    save_object(form, article)
    return render_template('editor.html', form=form, submit='Save')

@backend.route('/article/new')
def create_article():
    article = Article()
    form = ArticleEditForm(request.form, article)
    save_object(form, article)
    return render_template('editor.html', form=form, submit='Create')


@backend.route('/')
def home():
    classes = filter(lambda x: issubclass(x, db.Model),
        [x[1] for x in inspect.getmembers(btnfemcol.models, inspect.isclass)])
    #for member in inspect.getmembers(btnfemcol.models, inspect.isclass):
    #    if issubclass(member[1], db.Model):
    #        classes.append(member)
    return render_template('admin_home.html',
        classes=classes)
