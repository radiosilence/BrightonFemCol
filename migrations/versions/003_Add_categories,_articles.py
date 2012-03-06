from sqlalchemy import *
from migrate import *

meta = MetaData()


category = Table(
    'category', meta,
    Column('id', Integer, primary_key=True),
    Column('slug', String(120), unique=True, nullable=False),
    Column('title', String(120), unique=True, nullable=False),
    Column('status', String(255)),
    Column('order', Integer)
)

article = Table(
    'article', meta,
    Column('id', Integer, primary_key=True),
    Column('slug', String(120), unique=True, nullable=False),
    Column('title', String(120), unique=True, nullable=False),
    Column('status', String(255)),
    Column('order', Integer),
    Column('body', Text, nullable=False),
    Column('author_id', Integer, ForeignKey('user.id')),
    Column('pub_date', DateTime),
    Column('subtitle', Text),
    Column('revision', Integer),
    Column('category_id', Integer, ForeignKey('category.id'))
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    category.create()
    article.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    article.drop()
    category.drop()