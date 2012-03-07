from sqlalchemy import *
from migrate import *

def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    log_entry = Table('log_entry', meta, autoload=True)
    class_namec = Column('class_name', String(255))
    class_namec.create(log_entry)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    log_entry = Table('log_entry', meta, autoload=True)
    log_entry.c.class_name.drop()
