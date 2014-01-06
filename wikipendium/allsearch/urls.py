from django.conf.urls import patterns, url


urlpatterns = patterns(
    'wikipendium.allsearch.views',
    url(r'^$', 'all_search'),
)
