from wikipendium.jitishcron.decorators import task
from wikipendium import settings
import subprocess

twenty_four_hours_in_seconds = 60 * 60 * 24


@task(min_interval_in_seconds=twenty_four_hours_in_seconds)
def database_backup():
    if not settings.DEBUG:
        subprocess.Popen(['venv/bin/python', 'manage.py', 'backup-to-s3'])
