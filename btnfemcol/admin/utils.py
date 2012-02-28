"""Admin specific utility functions and classes."""

from functools import wraps
from flask import g, redirect, flash, url_for

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