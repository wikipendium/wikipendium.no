# -*- coding: utf8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

slug_regex = ur'[A-Za-z0-9æøåÆØÅ]+'
article_regex = ur'(?P<slug>' + slug_regex + ')[^/]*'

article_patterns = patterns(
    'wikipendium.wiki.views',
    url(r'^edit/$', 'edit'),
    url(r'^history/$', 'history'),
    url(r'^history/(?P<id>\d+)/$', 'history_single'),
)

urlpatterns = patterns(
    'wikipendium.wiki.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/', include('wikipendium.upload.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^$', 'home', name='home'),
    url(r'^new/$', 'new', name='newarticle'),
    url(r'^all/$', 'all_articles', name='allarticles'),

    url(r'^users/(?P<username>' + slug_regex + ')/$',
        'user', name='user'),

    url(r'^' + article_regex + '/$',
        RedirectView.as_view(url='/%(slug)s')),

    url(r'^' + article_regex + '$', 'article'),
    url(r'^' + article_regex + '/',
        include(article_patterns)),
    url(r'^' + article_regex + '/add_language/$',
        'add_language'),

    url(r'^' + article_regex + '/(?P<lang>[a-z]+)/$',
        'article'),
    url(r'^' + article_regex + '/(?P<lang>[a-z]+)/',
        include(article_patterns)),
)
