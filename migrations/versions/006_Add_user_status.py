from sqlalchemy import *
from migrate import *

def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('user', meta, autoload=True)
    statusc = Column('status', String(10))
    statusc.create(user)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('user', meta, autoload=True)
    user.c.email.drop()
