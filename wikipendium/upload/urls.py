from django.conf.urls import patterns, url


urlpatterns = patterns(
    'wikipendium.upload.views',
    url(r'$', 'upload'),
)
