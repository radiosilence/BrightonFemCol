"""Admin specific utility functions and classes."""
import math
import json

from functools import wraps
from flask import g, redirect, flash, url_for, abort, request, render_template

from btnfemcol import db
from btnfemcol import cache


def edit_instance(cls, form_cls, edit_template='form.html', id=None):
    if id:
        instance = cls.query.filter_by(id=id).first()
        if not instance:
            return abort(404)
        submit = 'Update'
    else:
        instance = cls()
        submit = 'Create'
    
    form = form_cls(request.form, instance)
    
    created = save_instance(form, instance)
    if created:
        return redirect(url_for('admin.edit_%s' % cls.__name__.lower(), id=created))
    return render_template(edit_template, form=form, submit=submit)


def save_instance(form, instance, message=u"%s saved."):
    """This function handles the simple cyle of testing if an instance's form
    validates and then saving it.
    """
    if request.method == 'POST':
        if not form.validate():
            flash("There were errors saving, see below.", 'error')
            return False
        form.populate_obj(instance)
        if not instance.id:
            db.session.add(instance)
        db.session.commit()
        flash(message % instance.__unicode__(), 'success')
        return instance.id
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


def calc_pages(results, per_page):
    return int(math.ceil(float(results) / float(per_page)))


def json_inner(cls, base, status=None, page=None, per_page=None, filter=None,
    order=None):
    """This function handles getting json for instances once arguments have
    already been decided.
    """
    if not status:
        status = request.args.get('status', default='any')
    if not page:
        page = request.args.get('page', default=1, type=int)
    if not per_page:
        per_page = request.args.get('per_page', default=20, type=int)
    if not filter:
        filter = request.args.get('filter', default=None)

    start = per_page * (page - 1)
    end = per_page * page

    if filter and status != 'any':
        q = base.filter_by(status=status).filter(
            cls.title.like('%' + filter + '%'))
    elif filter:
        q = base.filter(
            cls.title.like('%' + filter + '%'))
    elif status == 'any':
        q = base
    else:
        q = base.filter_by(status=status)
    
    if order:
        q = q.order_by(*order)

    instances = q[start:end]
    num_pages = calc_pages(q.count(), per_page)
    return json.dumps({
        'items': [o.json_dict for o in instances],
        'num_pages': num_pages
    })
