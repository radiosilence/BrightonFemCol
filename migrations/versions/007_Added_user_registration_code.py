from sqlalchemy import *
from migrate import *

def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('user', meta, autoload=True)
    reg_codec = Column('reg_code', String(255))
    reg_codec.create(user)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('user', meta, autoload=True)
    user.c.reg_code.drop()
