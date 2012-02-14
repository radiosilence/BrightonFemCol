from flask import Blueprint, g, session, config, current_app, flash

from btnfemcol.models import User

admin = Blueprint('admin', __name__,
    template_folder='templates')

import views