from datetime import datetime
from flask import url_for

from btnfemcol import db
from btnfemcol.utils import Hasher


class Administrable(object):
    @classmethod
    def __url__(cls):
        return cls.__name__.lower()

    @classmethod
    def admin_url(cls, action, id=None):
        if action == 'list':
            return url_for('admin.list', type=cls.__url__())
        else:
            return url_for('admin.action', type=cls.__url__(), id=id, action=action)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text)

    def __init__(self, title, body, slug=None):
        self.title = title
        self.body = body
        
        if not slug:
            self.slug = self._generate_slug()
            self.slug = slug

    def _generate_slug(self):
        pass

    def __repr__(self):
        return '<Page: %r>' % self.title

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)
 
class Article(Page):
    __mapper_args__ = {'polymorphic_identity': 'article'}
    id = db.Column(db.Integer, db.ForeignKey('page.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',
        backref=db.backref('articles', lazy='dynamic'))
    pub_date = db.Column(db.DateTime)
    subtitle = db.Column(db.String(255))

    tags = db.relationship('Tag', secondary=tags, 
        backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title=None, body=None, pub_date=None, slug=None,
        author=None, subtitle=None):
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.author = author
        self.subtitle = subtitle
        super(Article, self).__init__(title, body, slug=slug)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    

class Category(db.Model):
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

    def __init__(self, username=None, email=None, firstname=None, surname=None):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def __unicode__(self):
        return '{0} {1} ({2}) <{4}>'.format(
            self.firstname,
            self.surname,
            self.username,
            self.email
        )

    def update_password(self, password):
        if len(password) < 1:
            return False
        
        h = Hasher()
        self.password = h.hash(password)


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
    groups = db.relationship('Group', secondary=permissions,
        backref=db.backref('permissions', lazy='dynamic'))

    def __init__(self, name=None):
        self.name = name
    
    def __repr__(self):
        return '<Permission %r>' % self.name
