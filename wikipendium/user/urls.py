# -*- coding: utf8 -*-

from django.conf.urls import patterns, include, url
from .views import WikipendiumRegistrationView


urlpatterns = patterns(
    'wikipendium.user.views',

    url(r'^accounts/register/$',
        WikipendiumRegistrationView.as_view(success_url='/'),
        name='registration_register'),
    url(r'^accounts/', include('registration.auth_urls')),
    url(r'^users/(?P<username>[\w|\W]+)/$',
        'profile', name='user'),
    url(r'^accounts/username/change/$', 'change_username'),
)
