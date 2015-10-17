wikipendium.no
==============

kompendie-wiki

![](http://i.imgur.com/Fc1mtDN.png)

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

#### Setup on Windows
* If you do not have make installed, open Makefile to see what f.ex `make setup` corresponds to. Or get [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm).
* pip may fail to install PyCrypto. In that case, download [binaries for Windows](http://www.voidspace.org.uk/python/modules.shtml#pycrypto). You can install pycrypto by running the exe file with easy_install (f.ex `easy_install pycrypto-2.6.win32-py2.7.exe`)
* You may have to install six. Simply run `pip install six`.

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
