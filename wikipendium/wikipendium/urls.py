from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.backends.default.urls')),

     url(r'^$', 'wiki.views.home', name='home'),

     url(r'^(?P<slug>[A-Za-z0-9]+)/edit/$', 'wiki.views.edit', name='editarticle'),
     url(r'^article_trie/$', 'wiki.views.article_trie', name='article_trie'),
     url(r'^(?P<slug>[A-Za-z0-9]+).*$', 'wiki.views.article', name='article'),

)
