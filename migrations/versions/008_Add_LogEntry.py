from sqlalchemy import *
from migrate import *

meta = MetaData()

log_entry = Table(
    'log_entry', meta,
    Column('id', Integer, primary_key=True),
    Column('subject_id', Integer, ForeignKey('user.id')),
    Column('target_id', Integer),
    Column('verb', String),
    Column('when', DateTime)
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    log_entry.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    log_entry.drop()