"""Admin specific utility functions and classes."""

from functools import wraps
from flask import g, redirect, flash, url_for, abort, request

from btnfemcol import db
from btnfemcol import cache

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

def auth_logged_in(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user = g.user
            if not user:
                raise Exception
        except (AttributeError, Exception):
            flash("You must be logged in to view this page.", 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


def auth_allowed_to(permission):
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            try:
                user = g.user
                if not user.allowed_to(permission) and test:
                    raise Exception
            except (AttributeError, Exception):
                return abort(403)
            return f(*args, **kwargs)
        return inner
    return decorator

def section(name):
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            g.section = name
            return f(*args, **kwargs)
        return inner
    return decorator