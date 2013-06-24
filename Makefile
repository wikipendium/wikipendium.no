

all: update migrate 

run:
	python manage.py runserver

serve:
	python manage.py runserver 0.0.0.0:8000

update:
	pip install -r requirements.txt

migrate:
	python manage.py syncdb --migrate

lint:
	flake8 wikipendium/ --exclude=migrations,settings,diff.py

test:
	python manage.py test
