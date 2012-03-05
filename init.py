#!/usr/bin/env python2
from btnfemcol import create_app, db

db.create_all(app=create_app())
print "Created database."

from btnfemcol.models import *

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
welcome = Page(section=home, title="Welcome", slug='welcome',
    body='This is the home page.',
    status='live')

demo = Page(section=home, title="Demo", slug='demo', body=default_body,
    status='live')

db.session.add(welcome)
db.session.add(demo)
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

body = """Bacon ipsum dolor sit amet hamburger dolore drumstick ribeye, deserunt nisi jowl fatback short ribs. Enim proident short loin incididunt, dolore frankfurter jowl strip steak eu occaecat. In sed dolore aute flank exercitation, ex t-bone ea andouille venison qui commodo ut. Meatball occaecat shoulder ribeye sunt, ut irure chuck elit cillum.

Beef ribs chicken short loin, nisi ground round t-bone elit jerky shankle exercitation voluptate ex. Leberkas id meatball pancetta. Commodo sint aute capicola labore, tri-tip eiusmod rump ham anim qui pork loin deserunt reprehenderit pariatur. Meatball rump tri-tip culpa leberkas t-bone. Adipisicing tongue short loin aliquip venison, ut flank et elit pork loin shoulder. Leberkas cupidatat eu, commodo shankle pastrami adipisicing ullamco nulla laboris laborum irure proident. Do sausage jerky, hamburger swine brisket tenderloin sint laboris leberkas pork loin reprehenderit flank short loin boudin.
"""

body2 = """Tongue pork belly exercitation, pig tri-tip dolore ribeye pancetta. Meatball aute ex t-bone, incididunt pork labore commodo et nulla laboris capicola. Bresaola enim quis, tongue consectetur pork belly shoulder swine ut nostrud esse reprehenderit in. Officia cillum esse, filet mignon veniam pariatur adipisicing meatloaf.

Prosciutto sirloin laboris consequat. Minim short loin deserunt tenderloin commodo consectetur, ad ut jerky do ullamco ut pork chop shank. Consequat quis in boudin, turkey pig sed tongue nostrud ad pork loin adipisicing. Do adipisicing consectetur, dolore ham meatloaf ad. Biltong sed drumstick, nulla minim hamburger sint. Shankle sirloin short loin biltong culpa, drumstick fugiat ut chuck aute reprehenderit hamburger pork belly. Ham occaecat pastrami pork.

T-bone enim turducken ham, eiusmod tempor reprehenderit anim et adipisicing biltong. Proident jowl deserunt esse mollit. Filet mignon ham flank shankle pork mollit tempor incididunt ea aliqua. Eu pork loin drumstick officia biltong. Ullamco pork chop ut pig non minim. Eiusmod elit short loin non.
"""
a = Article(title='Shankle Sirloin Short', body=body, slug='first-article',
        author=u, subtitle='T-bone enim turducken ham, eiusmod tempor reprehenderit anim et adipisicing biltong.', status='published',
        category=Category.query.first())
a2 = Article(title='Drumstick Officia Biltong', body=body2, slug='another-article',
        author=u2, subtitle='Minim short loin deserunt tenderloin commodo consectetur, ad ut jerky do ullamco ut pork chop shank.', status='published',
        category=Category.query[1])

db.session.add(a)
db.session.add(a2)
db.session.commit()

print "Added article."