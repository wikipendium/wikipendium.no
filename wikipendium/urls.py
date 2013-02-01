from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     url(r'^accounts/', include('registration.backends.simple.urls')),
     url(r'^$', 'wikipendium.wiki.views.home', name='home'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*$', 'wikipendium.wiki.views.article', name='article'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/edit/$', 'wikipendium.wiki.views.edit', name='editarticle'),
     url(r'^(?P<slug>[A-Za-z0-9]+)[^/]*/history/$', 'wikipendium.wiki.views.history', name='articlehistory'),

)
