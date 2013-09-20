wikipendium.no
==============

kompendie-wiki


## Getting started

This is a short guide to setting up the project for developing.

### Dependencies

* python-dev
* pip
* build-essential

These can be installed on ubuntu with:
    (as root)$ apt-get install python-dev python-pip build-essential

You also need virtualenv, which can be installed with pip:
    (as root)$ pip install virtualenv

Then simply:

```
git clone git@github.com:stianjensen/wikipendium.no.git
cd wikipendium.no
make setup
source venv/bin/activate
make
```

When you've pulled updates, you can run `make` to udpate dependencies and migrate the database.

If you want newrelic reporting in prod, `cp wikipendium/settings/newrelic.ini.example wikipendium/settings/newrelic.ini`, and put the proper newrelic licence key in the .ini file.

#### E-mail sending

Some parts of wikipendium (such as password recovery) relies on e-mail sending.
For this to work, mailgun needs to be set up on the prod server.

```
MAILGUN_ACCESS_KEY = 'ACCESS-KEY'
MAILGUN_SERVER_NAME = 'SERVER-NAME'
```

## Coding style

Wikipendium uses Flake8.
Getting a plugin for your editor is highly recommended.
