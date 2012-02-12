from flask import Blueprint, g, session, config, current_app

from btnfemcol.models import User

frontend = Blueprint('frontend', __name__,
    template_folder='templates')


@frontend.before_request
def before_request():
    g.logged_in = False
    g.GMAPS_KEY = current_app.config['GMAPS_KEY']
    try:
        if session['logged_in']:
            g.logged_in = True
            g.user.load(session['logged_in'])
    except KeyError:
        pass
    except UserNotFoundError:
        from views import logout
        logout()


@frontend.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    return response

import views