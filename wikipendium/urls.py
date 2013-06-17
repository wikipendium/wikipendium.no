# -*- coding: utf8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import redirect_to

admin.autodiscover()

slug_regex = ur'[A-Za-z0-9æøåÆØÅ]+'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^$', 'wikipendium.wiki.views.home', name='home'),
    url(r'^new/$', 'wikipendium.wiki.views.new', name='newarticle'),
    url(r'^all/$', 'wikipendium.wiki.views.all_articles', name='allarticles'),

    url(r'^(?P<x>' + slug_regex + '[^/]*)/$', redirect_to, {'url': '/%(x)s'}),
    url(r'^(?P<slug>' + slug_regex + ')[^/]*$',
        'wikipendium.wiki.views.article'),
    url(r'^(?P<slug>' + slug_regex + ')[^/]*/edit/$',
        'wikipendium.wiki.views.edit'),
    url(r'^(?P<slug>' + slug_regex + ')[^/]*/history/$',
        'wikipendium.wiki.views.history'),
    url(r'^(?P<slug>' + slug_regex + ')[^/]*/history/(?P<id>\d+)/$',
        view='wikipendium.wiki.views.history_single', kwargs={'lang': 'en'}),
    url(r'^(?P<slug>' + slug_regex + ')[^/]*/add_language/$',
        'wikipendium.wiki.views.add_language'),

    url(r'^users/(?P<username>' + slug_regex + ')/$',
        'wikipendium.wiki.views.user', name='user'),

    url(r'^(?P<slug>' + slug_regex + ')[^/]*/(?P<lang>[a-z]+)/$',
        'wikipendium.wiki.views.article'),

    url(r'^(?P<slug>' + slug_regex + ')[^/]*/(?P<lang>[a-z]+)/edit/$',
        'wikipendium.wiki.views.edit'),
    url(r'^(?P<slug>' + slug_regex + ')[^/]*/(?P<lang>[a-z]+)/history/$',
        'wikipendium.wiki.views.history'),
    url(r'^(?P<slug>' + slug_regex + ')[^/]*/(?P<lang>[a-z]+)/history/(?P<id>\d+)/$',
        'wikipendium.wiki.views.history_single'),

)
