from django.conf.urls import patterns, url

urlpatterns = patterns(
    'wikipendium.stats.views',
    url(r'^$', 'index'),
)
