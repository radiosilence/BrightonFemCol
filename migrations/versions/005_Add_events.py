from sqlalchemy import *
from migrate import *

meta = MetaData()

event = Table(
    'event', meta,
    Column('id', Integer, primary_key=True),
    Column('slug', String(120), unique=True, nullable=False),
    Column('title', String(120), unique=True, nullable=False),
    Column('status', String(255)),
    Column('order', Integer),
    Column('body', Text, nullable=False),
    Column('start', DateTime),
    Column('end', DateTime),
    Column('location', String(255))
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    event.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    event.drop()