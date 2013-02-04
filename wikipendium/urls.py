from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     url(r'^accounts/', include('registration.backends.simple.urls')),
     url(r'^$', 'wikipendium.wiki.views.home', name='home'),
     url(r'^new/$', 'wikipendium.wiki.views.new', name='newarticle'),

     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*$', 'wikipendium.wiki.views.article'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/edit/$', 'wikipendium.wiki.views.edit'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/history/$', 'wikipendium.wiki.views.history'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/history/(?P<id>\d+)/$', view='wikipendium.wiki.views.history_single', kwargs={'lang':'en'}),

     url(r'^users/(?P<username>[A-Za-z0-9]+)/$', 'wikipendium.wiki.views.user', name='user'),

     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/(?P<lang>[a-z]+)/$', 'wikipendium.wiki.views.article'),

     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/(?P<lang>[a-z]+)/edit/$', 'wikipendium.wiki.views.edit'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/(?P<lang>[a-z]+)/history/$', 'wikipendium.wiki.views.history'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/(?P<lang>[a-z]+)/history/(?P<id>\d+)/$', 'wikipendium.wiki.views.history_single'),

)
