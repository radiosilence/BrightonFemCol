from btnfemcol import create_app, db

db.create_all(app=create_app())

from btnfemcol.models import User, Group

g = Group(name='Administrator')
db.session.add(g)
db.session.add(Group(name='Editor'))
db.session.add(Group(name='Writer'))
db.session.commit()

u = User(
    g,
    username='admin',
    password='admin',
    email='admin@example.com',
    firstname='Overseer',
    surname='Alpha'
)

db.session.add(u)
db.session.commit()

