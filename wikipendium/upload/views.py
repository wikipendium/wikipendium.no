import boto.s3
from boto.s3.key import Key
import boto
import time
import random
from wikipendium import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@require_POST
@csrf_exempt
@login_required
def upload(request):

    aws_id = settings.AWS_ID
    aws_key = settings.AWS_KEY
    aws_bucket_name = settings.AWS_PUBLIC_BUCKET_NAME
    aws_public_url = settings.AWS_PUBLIC_URL

    conn = boto.connect_s3(aws_id, aws_key)
    buckets = conn.get_all_buckets()

    filename = str(int(time.time())) + \
        str(hex(int(random.random() * 1000000))) + '.jpg'

    for bucket in buckets:
        if bucket.name == aws_bucket_name:
            k = Key(bucket)
            k.key = filename
            image = str(request.FILES['image'].read())
            k.set_contents_from_string(image)
            k.set_acl('public-read')
            break

    return HttpResponse('{"image":"%s"}' % (aws_public_url + '/' + filename),
                        content_type='application/json')
