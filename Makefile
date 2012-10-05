VIRTUAL_ENV?=".."
UWSGI_INI?="../uwsgi.yaml"

debug:
	./manage.py runserver 0.0.0.0:8000

install_requirements:
	$(VIRTUAL_ENV)/bin/pip install -r requirements.txt

pull:
	git pull

upgrade: pull install_requirements update_static compress optimize_js update_db restart

compress:
	$(VIRTUAL_ENV)/bin/python manage.py compress --force

update_static:
	rm static -rf
	$(VIRTUAL_ENV)/bin/python manage.py collectstatic -l --noinput
	$(VIRTUAL_ENV)/bin/python manage.py compress --force

update_db:
	$(VIRTUAL_ENV)/bin/python manage.py syncdb --noinput
	$(VIRTUAL_ENV)/bin/python manage.py migrate

optimize_js:
	 r.js -o name=main out=brightonfemcol/static/js/main-built.js baseUrl=brightonfemcol/static/js


create_admin:
	$(VIRTUAL_ENV)/bin/python manage.py create_admin

init: init_db create_admin

init_db: update_db

restart:
	touch $(UWSGI_INI)

	
