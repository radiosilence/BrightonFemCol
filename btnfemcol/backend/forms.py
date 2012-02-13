from btnfemcol.models import User, Page, Article

from flaskext.wtf import *
from flaskext.wtf.html5 import *
from wtforms.ext.sqlalchemy.orm import model_form


class Unique(object):
    """Validator that checks field uniqueness."""
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'Must be unique.'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data) \
            .filter(self.model.id != form._model.id) \
            .first()
            
        if check:
            raise ValidationError(self.message)


UserFormBase = model_form(User, Form, exclude=['id'], field_args={
    'username': {
        'validators': [
            Unique(User, User.username)
        ],
        'description': 'Eg. lady_derpington'
    },
    'firstname': {
        'label': u'First Name',
        'validators': [
            Required()
        ],
        'description': 'Eg. Jane'
    },
    'surname': {
        'validators': [
            Required()
        ],
        'description': 'Eg. Derp'
    },
    'url': {
        'label': u'URL',
        'description': 'Eg. http://www.derpsworth.com'
    },
    'email': {
        'validators': [
            Required()
        ],
        'description': 'Eg. derping@gmail.com'
    },
    'phone': {
        'description': 'Eg. 07688283555'
    },
    'twitter': {
        'description': 'Eg. @derpslife'
    }
})

class UserEditForm(UserFormBase):
    def __init__(self, form, user, *args, **kwargs):
        self._model = user
        super(UserEditForm, self).__init__(form, user, *args, **kwargs)

class UserRegistrationForm(UserEditForm):
    #email = EmailField()
    password = PasswordField('Password',
        [optional(), equal_to('confirm_pass',
            message='Passwords must match.')])
    confirm_pass = PasswordField('Confirm Password')


PageFormBase = model_form(Page, Form, exclude=['id'], field_args={
    'title': {
        'validators': [
            Required()
        ]
    }
})

class PageEditForm(PageFormBase):
    pass

class AuthorField(SelectField):
    def iter_choices(self):
        yield (None, 'Please select an author.', not self.data)
        for user in User.query.all():
            yield (user.id, user.username, user.id == self.data)

ArticleFormBase = model_form(Article, PageEditForm, exclude=['id'])

class ArticleEditForm(ArticleFormBase):
    author_id = AuthorField()
