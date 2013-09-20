import time
import getpass
from fabric.api import *
from fabric.contrib.console import confirm
import subprocess

class Site(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def run(self, cmd):
        with cd(self.dir):
            sudo(cmd, user=self.user_id)

    def backup(self):
        self.run('venv/bin/python manage.py backup-to-s3')

    def deploy(self):
        self.git_pull()
        self.update_packages()
        self.run('venv/bin/python manage.py syncdb --migrate')
        self.run('venv/bin/python manage.py collectstatic --noinput')
        self.restart()

    def git_pull(self):
        # .pyc files can create ghost behavior when .py files are deleted...
        self.run("find . -name '*.pyc' -delete")
        self.run("git fetch origin && git reset --hard origin/master")

    def git_tag(self):
        if confirm("Give new tag for this deployment?"):
            self.run("git tag |tail -n 5")
            tag = prompt('Give new tag for this deployment: ')
            self.run("git tag %s" % tag)
            self.run("git push --tags && git push")

    def update_packages(self):
        self.run("./venv/bin/pip install -r requirements.txt")

    def restart(self):
        #header("Running: Restart server script: %s" % self.gunicorn)
        #run("sudo /etc/init.d/%s restart" % self.gunicorn)
        run("touch wikipendium_uswgi.ini")

PROD = Site(
    dir='/home/prods/wikipendium.no/',
    user_id='www-data'
)

env.hosts = ['wikipendium.no']

@task
def clone_prod_data():
    """
    Download production data (database and uploaded files) and insert locally
    """

    env.user = prompt("Username on prod server:", default=getpass.getuser())
    dump_file = str(time.time()) + ".json"

    # Ignore errors on these next steps, so that we are sure we clean up no matter what
    with settings(warn_only=True):

        # Dump the database to a file...
        PROD.run('source venv/bin/activate && nice python manage.py dumpdata > ' + dump_file)

        # clean password hashes
        PROD.run('sed -i \'s/"password": "[^"]*"/"password": ""/\' ' + dump_file)

        # Then download that file
        get(PROD.dir + dump_file, dump_file)

        # Replace this db with the contents of the dump
        local('python manage.py loaddata_ex ' + dump_file)

    # ... then cleanup the dump files
    PROD.run('rm ' + dump_file)
    local('rm ' + dump_file)

@task
def deploy():
    """
    """
    # mac-only command, just for fun
    try:
        subprocess.call(['say', '"Ship! Ship! Ship!"'])
    except:
        pass
    print "ship! ship! ship!"

    env.user = prompt("Username on prod server:", default=getpass.getuser())

    PROD.backup()
    PROD.deploy()

    # Check if we want to tag the deployment
    PROD.git_tag()

def header(text):
    print ("#" * 45) + "\n# %s\n" % text + ("#" * 45)

@task
def restart():
    PROD.restart()

@task
def backup():
    """
    Dump a full backup to S3.
    """
    env.user = prompt("Username on prod server:", default=getpass.getuser())
    PROD.backup()
