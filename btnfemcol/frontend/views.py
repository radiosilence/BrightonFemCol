from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)

from btnfemcol.frontend import frontend
from flaskext.wtf import Form
from wtforms.ext.appengine.orm import model_form

from btnfemcol import uploaded_images, uploaded_avatars

@frontend.route('/'):
def home():
    return "DERPS"