from django.core.management.commands.loaddata import Command as loaddata
from django.db import connection, transaction


class Command(loaddata):
    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('DELETE FROM django_content_type;')
        cursor.execute('DELETE FROM auth_permission;')
        transaction.commit_unless_managed()
        super(Command, self).handle(*args, **kwargs)
