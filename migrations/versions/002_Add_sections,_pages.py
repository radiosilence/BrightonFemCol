from sqlalchemy import *
from migrate import *

meta = MetaData()

section = Table(
    'section', meta,
    Column('id', Integer, primary_key=True),
    Column('slug', String(120), unique=True, nullable=False),
    Column('title', String(120), unique=True, nullable=False),
    Column('status', String(255)),
    Column('order', Integer)
)

page = Table(
    'page', meta,
    Column('id', Integer, primary_key=True),
    Column('slug', String(120), unique=True, nullable=False),
    Column('title', String(120), unique=True, nullable=False),
    Column('status', String(255)),
    Column('order', Integer),
    Column('body', Text, nullable=False),
    Column('section_id', Integer, ForeignKey('section.id'))
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    section.create()
    page.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    page.drop()
    section.drop()