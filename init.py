#!/usr/bin/env python2
from btnfemcol import create_app, db

db.create_all(app=create_app())

from btnfemcol.models import User, Group, Permission

# Add permissions
perms = [
    ('manage_articles', 'Manage and Publish Articles'),
    ('manage_events', 'Manage Events'),
    ('manage_pages', 'Manage Site Content'),
    ('manage_site', 'Manage Site Settings'),
    ('manage_users', 'Manage Users'),
    ('moderate', 'Moderate Forums and Comments'),
    ('post_comments', 'Post Comments'),
    ('write_articles', 'Write Articles'),
    ('change_authors', 'Change the author of an article.')
]

permissions = {}
for name, title in perms:
    p = Permission(name, title)
    permissions[name] = p
    db.session.add(p)

db.session.commit()

# Basic User
g_user = Group(name='User')
for name in ['post_comments']:
    g_user.permissions.append(permissions[name])
db.session.add(g_user)

# Writer
g_writer = Group(name='Writer')
for p in g_user.permissions:
    g_writer.permissions.append(p)
for name in ['write_articles']:
    g_writer.permissions.append(permissions[name])
db.session.add(g_writer)

# Editor
g_editor = Group(name='Editor')
for p in g_writer.permissions:
    g_editor.permissions.append(p)
for name in ['manage_articles']:
    g_editor.permissions.append(permissions[name])
db.session.add(g_editor)

# Moderator
g_moderator = Group(name='Moderator')
for p in g_writer.permissions:
    g_moderator.permissions.append(p)
for name in ['moderate']:
    g_moderator.permissions.append(permissions[name])
db.session.add(g_moderator)

# Administrator
g_admin = Group(name='Administrator')
for p in g_editor.permissions:
    g_admin.permissions.append(p)
for name in ['manage_events', 'manage_pages', 'manage_users', 'moderate']:
    g_admin.permissions.append(permissions[name])
db.session.add(g_admin)

# Super User
g_su = Group(name='Super User')
for name, _ in perms:
    g_su.permissions.append(permissions[name])
db.session.add(g_su)

# Commit users
db.session.commit()

# Create our first SU
u = User(
    g_su,
    username='admin',
    password='admin',
    email='admin@example.com',
    firstname='Overseer',
    surname='Alpha'
)

db.session.add(u)

u2 = User(
    g_writer,
    username='writer',
    password='writer',
    email='writer@example.com',
    firstname='Writer',
    surname='Omega'
)

db.session.add(u2)

u3 = User(
    g_editor,
    username='editor',
    password='editor',
    email='editor@example.com',
    firstname='Editor',
    surname='Zeta'
)

db.session.add(u3)

db.session.commit()
