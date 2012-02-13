from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

from btnfemcol.backend import backend

from btnfemcol import uploaded_images, uploaded_avatars
from btnfemcol import db

from btnfemcol.models import User, Article
from btnfemcol.backend.forms import UserEditForm, UserRegistrationForm


@backend.route('/', methods=['GET', 'POST'])
def home():
    user = User()
    form = UserRegistrationForm(request.form, user)
    save_user(form, user, message="Thanks for registering.")
    return render_template('form.html', form=form, submit='Register')


def save_user(form, user, message="User %s saved."):
    if form.validate_on_submit():
        if form.password.data == '':
            form.password.data = None

        form.populate_obj(user)
        
        db.session.add(user)
        db.session.commit()
        flash(message % user.username)

@backend.route('/user/<string:username>', methods=['GET', 'POST'])
def edit_user(username):
    user = User.query.filter_by(username=username).first()
    form = UserRegistrationForm(request.form, user)
    save_user(form, user)
    return render_template('form.html', form=form, submit='Save')