from btnfemcol.models import User, Page, Article, Event, Section

from flask import g
from flaskext.wtf import *
from flaskext.wtf.html5 import *
from wtforms.ext.sqlalchemy.orm import model_form

from btnfemcol.utils import Hasher

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


class ForeignKeyField(SelectField):
    def pre_validate(self, form):
        if not self.data:
            return False
        for v in self.choices:
            if self.coerce(self.data) == v.id:
                break
        else:
            raise ValueError(self.gettext(u'Not a valid choice'))

    def iter_choices(self):
        yield (None, 'Please select...', not self.data)
        if not self.data:
            self.data = -1
        for choice in self.choices:
            yield (choice.id, u'%s' % choice, choice.id == self.coerce(self.data))

    def process_formdata(self, valuelist):
        if not valuelist:
            return False
        if valuelist:
            try:
                self.data = self.coerce(valuelist[0])
            except ValueError:
                raise ValueError(self.gettext(u'Not a valid choice'))


# Page Forms
PageFormBase = model_form(Page, Form, exclude=['id'], field_args={
    'title': {
        'validators': [
            Unique(Page, Page.title),
            Required()
        ]
    },
    'slug': {
        'validators': [
            Unique(Page, Page.slug),
            Required()
        ]
    }
})

class SectionField(ForeignKeyField):
    def __init__(self, label=u'', validators=None, choices=None, **kwargs):
        super(SelectField, self).__init__(label, validators, **kwargs)
        self.coerce = int
        self.choices = Section.query.all()

    def iter_choices(self):
        if not self.data:
            self.data = 1
        for choice in self.choices:
            yield (choice.id, u'%s' % choice, choice.id == self.coerce(self.data))


class PageEditForm(PageFormBase):
    section_id = SectionField(label='Section')
    status = SelectField(label='Page Status', choices=[
        ('draft', 'Draft'),
        ('live', 'Live'),
        ('binned', 'Binned')
    ])

    def __init__(self, form, page, *args, **kwargs):
        self._model = page
        super(PageEditForm, self).__init__(form, page, *args, **kwargs)

# Event Forms
EventFormBase = model_form(Event, PageEditForm)

class EventEditForm(EventFormBase):
    pass

# Article Forms
class AuthorField(ForeignKeyField):
    def __init__(self, label=u'', validators=None, choices=None, **kwargs):
        super(SelectField, self).__init__(label, validators, **kwargs)
        self.coerce = int
        self.choices = User.query.all()


class ArticleStatusField(SelectField):
    def __init__(self, label=u'', validators=None, choices=None, **kwargs):
        super(SelectField, self).__init__(label, validators, **kwargs)
        self.coerce = str
        self.choices = [
            ('draft', u'Draft'),
            ('edit-queue', u'Submitted')
        ]
        if g.user.allowed_to('manage_articles'):
            self.choices.append(('published', 'Published'))

    def iter_choices(self):
        if not self.data:
            self.data = self.choices[0][0]
        for choice in self.choices:
            yield (choice[0], u'%s' % choice[1], choice[0] == self.coerce(self.data))

    def pre_validate(self, form):
        for v in self.choices:
            if self.coerce(self.data) == v[0]:
                break
        else:
            raise ValueError(self.gettext(u'Not a valid choice'))

ArticleFormBase = model_form(Article, PageEditForm, exclude=['id'], field_args={
    'title': {
        'validators': [
            Unique(Article, Article.title),
            Required()
        ]
    },
    'slug': {
        'validators': [
            Unique(Article, Article.slug),
            Required()
        ],
        'label': 'Permalink'
    }
})

class ArticleEditForm(ArticleFormBase):
    author_id = AuthorField(label='Author')
    status = ArticleStatusField(label='Publish Status')
    pub_date = DateTimeField(label='Publication Date')

    def __init__(self, form, article, *args, **kwargs):
        self._model = article
        super(ArticleEditForm, self).__init__(form, article, *args, **kwargs)


# User Forms
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
    password = PasswordField('Password',
        [optional()])

    def __init__(self, form, user, *args, **kwargs):
        self._model = user
        super(UserEditForm, self).__init__(form, user, *args, **kwargs)

    def populate_obj(self, user):
        if len(self.password.data) < 1:
            self.password.data = user.password
        else:
            h = Hasher()
            self.password.data = h.hash(self.password.data)
        x = super(Form, self).populate_obj(user)
        return x

class UserRegistrationForm(UserEditForm):
    password = PasswordField('Password',
        [optional(), equal_to('confirm_pass',
            message='Passwords must match.')])
    confirm_pass = PasswordField('Confirm Password')


# Generic Forms
class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')

