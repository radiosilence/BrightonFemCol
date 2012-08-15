VIRTUAL_ENV?=".."
UWSGI_INI?="../uwsgi.ini"

debug:
	./manage.py runserver 0.0.0.0:8000

install_requirements:
	$(VIRTUAL_ENV)/bin/pip install -r requirements.txt

pull:
	git pull

upgrade: pull uninstall_suave install_requirements update_static update_db restart

upgrade_suave: uninstall_suave install_requirements

uninstall_suave:
	yes | $(VIRTUAL_ENV)/bin/pip uninstall django-suave

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

	