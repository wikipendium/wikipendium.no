.PHONY: all
all: update migrate

.PHONY: run
run:
	python -Wd manage.py runserver

.PHONY: serve
serve:
	python -Wd manage.py runserver 0.0.0.0:8000

.PHONY: update
update:
	pip install -r requirements.txt

.PHONY: migrate
migrate:
	python -Wd manage.py migrate

.PHONY: migrations
migrations:
	python -Wd manage.py makemigrations

.PHONY: lint
lint:
	flake8 wikipendium/ --exclude=migrations,settings,diff.py

.PHONY: test
test:
	DJANGO_SETTINGS_MODULE=wikipendium.settings.test python -Wd manage.py test

.PHONY: setup
setup:
	python3 -m venv venv
	cp wikipendium/settings/local.py.example wikipendium/settings/local.py

.PHONY: shell
shell:
	python -Wd manage.py shell

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -type d -empty -delete
