from datetime import datetime
from sqlalchemy.ext.declarative import AbstractConcreteBase

from flask import url_for, abort

from btnfemcol import db
from btnfemcol import cache
from btnfemcol.utils import Hasher


class SiteEntity(object):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120), unique=True)
    status = db.Column(db.String(255))
    order = db.Column(db.Integer)

    def __init__(self, title=None, slug=None, body=None, order=0, status=None):
        self.slug = slug
        self.title = title
        self.status = status
        self.order = order


class Displayable(SiteEntity):
    body = db.Column(db.Text)

    def __init__(self, title=None, slug=None, body=None):
        self.body = body
        super(Displayable, self).__init__(title=title, slug=slug)


class Category(SiteEntity, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, title, slug, order, live=True):
        self.title = title
        self.slug = slug
        self.order = order


class Section(SiteEntity, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pages = db.relationship('Page', backref='section')

    def __init__(self, title, slug, order, live=True):
        self.title = title
        self.slug = slug
        self.order = order


class Page(Displayable, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

    @property
    def excerpt(self):
        return self.body[:140]

    def _generate_slug(self):
        pass

    def __repr__(self):
        return '<Page: %r>' % self.title

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)
 
class Article(Displayable, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',
        backref=db.backref('articles', lazy='dynamic'))
    pub_date = db.Column(db.DateTime)
    subtitle = db.Column(db.Text)
    revision = db.Column(db.Integer)

    tags = db.relationship('Tag', secondary=tags, 
        backref=db.backref('articles', lazy='dynamic'))


    def __init__(self, title=None, body=None, pub_date=None, slug=None,
        author=None, subtitle=None):
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.author = author
        self.subtitle = subtitle
        super(Article, self).__init__(title=title, body=body, slug=slug)

    @property
    def json_dict(self, exclude=[]):
        """This is a form of serialisation but specifically for the output to
        JSON for asyncronous requests."""
        d = {
            'id': self.id,
            'title': self.title,
            'revision': self.revision,
            'pub_date': self.pub_date.strftime('%c'),
            'urls': {
                'edit': url_for('admin.edit_article', id=self.id),
                'bin': '#'
            },
            'status': self.status,
            'author': {
                'username': self.author.username,
                'fullname': '%s %s' % (self.author.firstname, self.author.surname),
                'url': url_for('admin.edit_user', id=self.author.id)
            }
        }
        for key in exclude:
            del d[key]
        return d

    def __unicode__(self):
        return self.title


class Event(Displayable, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(255))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(80))
    twitter = db.Column(db.String(80))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group',
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, group, username=None, email=None, firstname=None,
        surname=None, password=None):
        
        if password:
            h = Hasher()
            self.password = h.hash(password)

        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.group = group
        self.group_id = group.id

    @cache.memoize(20)
    def allowed_to(self, name):
        """This will check if a user can do a certain action."""
        permission = Permission.query.filter_by(name=name).first()
        return permission in self.group.permissions

    def __repr__(self):
        return '<User %r>' % self.username

    def __unicode__(self):
        return '%s %s (%s) <%s>' % (
            self.firstname,
            self.surname,
            self.username,
            self.email
        )


permissions = db.Table('permissions',
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name
    
    def __repr__(self):
        return '<Group %r>' % self.name


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255))

    groups = db.relationship('Group', secondary=permissions,
        backref=db.backref('permissions', lazy='dynamic'))

    def __init__(self, name, title):
        self.name = name
        self.title = title
    
    def __repr__(self):
        return '<Permission %s:%r>' % (self.id, self.name)
