from flask import Blueprint, g, session, config, current_app

from btnfemcol.models import User

admin = Blueprint('admin', __name__,
    template_folder='templates')


@admin.before_request
def before_request():
    g.logged_in = False
    try:
        if session['logged_in']:
            g.logged_in = True
            g.user = User.session.filter_by(id=session['logged_in']).first()
    except KeyError:
        pass
    except UserNotFoundError:
        from views import logout
        logout()


@admin.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    return response

import views