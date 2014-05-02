from django.core.management.base import BaseCommand
from django.core.management import call_command
import datetime
import time
import zipfile
from subprocess import call
from StringIO import StringIO
import boto.s3
from boto.s3.key import Key
import socket
import boto
from wikipendium import settings


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Dumps the database to a json file, zips it and sends it to s3.
        """

        filename = str(time.mktime(datetime.datetime.now().timetuple())) \
            + "-" + socket.gethostname() + "-wikipendium-backup.dump"
        filename_zip = filename + '.zip'
        content = StringIO()
        call_command("dumpdb", stdout=content)

        with open(filename, 'w') as f:
            f.write(content.getvalue())

        with zipfile.ZipFile(filename_zip, 'w', zipfile.ZIP_DEFLATED) as z:
                z.write(filename)

        try:
            aws_id = settings.AWS_ID
            aws_key = settings.AWS_KEY
            aws_bucket_name = settings.AWS_BUCKET_NAME
        except:
            print "Please configure AWS credentials in settings/local.py!"
            return

        conn = boto.connect_s3(aws_id, aws_key)
        buckets = conn.get_all_buckets()

        for bucket in buckets:
            if bucket.name == aws_bucket_name:
                k = Key(bucket)
                k.key = filename_zip
                k.set_contents_from_filename(filename_zip)
                break

        call(['rm', filename])
        call(['rm', filename_zip])
