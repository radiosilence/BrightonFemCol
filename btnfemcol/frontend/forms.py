from flaskext.wtf import *
from flaskext.wtf.html5 import *

from btnfemcol.admin.forms import UserEditForm

class UserFrontendForm(UserEditForm):
    password = PasswordField('Password',
        [optional(), equal_to('confirm_pass',
            message='Passwords must match.')])
    confirm_pass = PasswordField('Confirm Password')
    
class UserProfileForm(UserFrontendForm):
    username = None


class UserRegistrationForm(UserFrontendForm):
    password = PasswordField('Password',
        [Required(), equal_to('confirm_pass',
            message='Passwords must match.')])
    group_id = None
    status = None
    location = None
    website = None
    phone = None
    twitter = None
