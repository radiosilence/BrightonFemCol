#!/usr/bin/env python
from btnfemcol import create_app, db

print "We need to create a superuser..."
SU_USERNAME = raw_input('\t username? ')
SU_PASSWORD = raw_input('\t password? ')
SU_EMAIL    = raw_input('\t email? ')
SU_FIRSTNAME= raw_input('\t first name? ')
SU_SURNAME  = raw_input('\t surname? ')
print "Thanks! Doing things now..."

db.create_all(app=create_app())
print "Created database."

from btnfemcol.models import *

# Add sections

sections = [
    ('uncategorized', 'Uncategorised', 'draft'),
    ('home', 'Home', 'live'),
    ('events', 'Events', 'live'),
    ('articles', 'Articles', 'live'),
    ('about', 'About', 'draft'),
    ('contact', 'Contact', 'draft')
]

i = 0
for s in sections:
    section = Section(slug=s[0], title=s[1], order=i, status=s[2])
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
events = Section.query.filter_by(slug='events').first()
welcome = Page(section=home, title="Welcome", slug='welcome',
    body="""Site will soon be updated to have articles, stories, events and information about our constitution, philosophy and organisation.""",
    status='live', order=0)
db.session.add(welcome)

demo = Page(section=home, title="Demo", slug='demo', body=default_body,
    status='live', order=0)
db.session.add(demo)
print "Added default page."

events_upcoming = Page(section=events, title="Upcoming", slug="upcoming",
    body="""These are events which are happening in the future.""",
    status="live", order=0)
db.session.add(events_upcoming)

events_past = Page(section=events, title="Past", slug="past",
    body="""These are events which have happened already.""",
    status="live", order=1)
db.session.add(events_past)

db.session.commit()
print "Added events."


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
    username=SU_USERNAME,
    password=SU_PASSWORD,
    email=SU_EMAIL,
    firstname=SU_FIRSTNAME,
    surname=SU_SURNAME
)

db.session.add(u)

db.session.commit()
print "Added superuser %s" % u

categories = [
    ('News', 'news'),
    ('Feminism', 'feminism'),
    ('Pro-Choice', 'pro-choice')
]

i = 0

for c in categories:
    category = Category(c[0], c[1], i, status='live')
    i += 1
    db.session.add(category)

db.session.commit()
print "Added categories."

body = """I've finally managed to get the site code into a usable state in so much as we can start writing articles, posting events, and adding pages.

This is excellent, and members should contact me to create usernames and passwords.

Editors, moderators, and administrators will be democratically selected.

Code is *very* new, so expect there to be some teething issues.
"""
a = Article(title='Website Launched', body=body, slug='site-launched',
        author=u, subtitle='Now serving pages.', status='published',
        category=Category.query.first())

db.session.add(a)
db.session.commit()

print "Added article."
format = '%Y-%m-%d %H:%M'
event_future = Event(location='The Blind Tiger',
    start=datetime.strptime('2012-04-05 20:00', format),
    end=datetime.strptime('2012-04-06 01:00', format),
    slug='reclaim-the-dancefloor',
    status='draft0',
    title='Reclaim the Dancefloor',
    body='I hope you like possums.'
)
db.session.add(event_future)
db.session.commit()
print "Added default events."