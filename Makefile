VIRTUAL_ENV?=".."
UWSGI_INI?="../uwsgi.yaml"

debug:
	./manage.py runserver 0.0.0.0:8000

install_requirements:
	$(VIRTUAL_ENV)/bin/pip install -r requirements.txt

pull:
	git pull

upgrade: pull install_requirements update_static update_db restart


update_static:
	$(VIRTUAL_ENV)/bin/python manage.py collectstatic -l --noinput

update_db:
	$(VIRTUAL_ENV)/bin/python manage.py syncdb --noinput
	$(VIRTUAL_ENV)/bin/python manage.py migrate

create_admin:
	$(VIRTUAL_ENV)/bin/python manage.py create_admin

init: init_db create_admin

init_db: update_db

restart:
	touch $(UWSGI_INI)

	
