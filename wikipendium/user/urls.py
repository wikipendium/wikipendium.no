# -*- coding: utf8 -*-

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'wikipendium.user.views',

    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/(?P<username>[\w|\W]+)/$',
        'profile', name='user'),
)
