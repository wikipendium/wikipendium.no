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
```

When you've pulled updates, you can run `make` to udpate dependencies and migrate the database.

## Coding style

Wikipendium uses Flake8.
Getting a plugin for your editor is highly recommended.
