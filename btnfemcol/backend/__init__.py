from flask import Blueprint, g, session, config, current_app

from btnfemcol.models import User

backend = Blueprint('backend', __name__,
    template_folder='templates')


@backend.before_request
def before_request():
    g.logged_in = False
    try:
        if session['logged_in']:
            g.logged_in = True
            g.user.load(session['logged_in'])
    except KeyError:
        pass
    except UserNotFoundError:
        from views import logout
        logout()


@backend.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    return response

import views