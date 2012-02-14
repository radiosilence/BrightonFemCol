from flask import Blueprint, g, session, config, current_app

from btnfemcol.models import User

frontend = Blueprint('frontend', __name__,
    template_folder='templates')

import views