#!/usr/bin/env python2
from btnfemcol import create_app, db

db.create_all(app=create_app())
print "Created database."

from btnfemcol.models import User, Group, Permission, Section, Page

# Add sections

sections = [
    ('uncategorized', 'Uncategorised', False),
    ('home', 'Home', True),
    ('events', 'Events', True),
    ('articles', 'Articles', True),
    ('about', 'About', True),
    ('contact', 'Contact', True)
]

i = 0
for s in sections:
    section = Section(s[1], s[0], i, live=s[2])
    db.session.add(section)
    i += 1

db.session.commit()
print "Added sections."

# Add a home page
default_body = """Welcome to DapperCMS. This is a default page, please delete
or edit it.

You can use **Markdown** to edit your pages, so it's easy to make text *italic*
or **bold** or ***both***.

You can also do quotes like this:

> This is a quote.

Indented code blocks:

    this is some code()

Bullet points:

* One
* Two
* Three

Links - [I am a link](http://www.google.com/)

and even subheadings:

## Bleep bloop

Amazing, no?
"""
home = Section.query.filter_by(slug='home').first()
welcome = Page(section=home, title="Welcome", slug='welcome', body=default_body,
    status='live')

db.session.add(welcome)
db.session.commit()

print "Added default page."

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
print "Added permissions."

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
print "Added groups."

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
print "Added test users."