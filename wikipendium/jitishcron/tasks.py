from wikipendium.jitishcron.decorators import task
from wikipendium import settings
import subprocess

twenty_four_hours_in_seconds = 60 * 60 * 24
fifteen_minutes_in_seconds = 60 * 15


@task(min_interval_in_seconds=twenty_four_hours_in_seconds)
def database_backup():
    if not settings.DEBUG:
        subprocess.Popen(['venv/bin/python', 'manage.py', 'backup-to-s3'])


@task(min_interval_in_seconds=fifteen_minutes_in_seconds)
def rebuild_search_index():
    if not settings.DEBUG:
        subprocess.Popen(['venv/bin/python', 'manage.py',
                          'rebuild_index', '--noinput'])
