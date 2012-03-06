from sqlalchemy import *
from migrate import *

meta = MetaData()

tag = Table(
    'tag', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(63))
)

tags = Table(
    'tags', meta,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('article_id', Integer, ForeignKey('article.id'))
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    article = Table('article', meta, autoload=True)
    tag.create()
    tags.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    tags.drop()
    tag.drop()