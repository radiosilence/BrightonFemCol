from datetime import datetime
from btnfemcol import db

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text)

    def __init__(self, title, body, slug=None):
        self.title = title,
        self.body = body
        
        if not slug:
            self.slug = self._generate_slug()
            self.slug = slug
        
    
    def _generate_slug(self):
        pass


    def __repr__(self):
        return '<Page: %r>' % self.title


class Article(Page):
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',
        backref=db.backref('articles', lazy='dynamic'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, category, pub_date=None, slug=None):
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category
        super(Article, self).__init__(title, body, slug=slug)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class User(object):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    twitter = db.Column(db.String(80), unique=True)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username