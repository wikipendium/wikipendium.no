# -*- coding: utf8 -*-

from django.conf.urls import include, url
from registration.backends.simple.views import RegistrationView
import registration.auth_urls
import wikipendium.user.views


urlpatterns = [
    url(r'^accounts/register/$',
        RegistrationView.as_view(success_url='/'),
        name='registration_register'),
    url(r'^accounts/', include(registration.auth_urls)),
    url(r'^users/(?P<username>[\w|\W]+)/$',
        wikipendium.user.views.profile, name='user'),
    url(r'^accounts/username/change/$',
        wikipendium.user.views.change_username),
    url(r'^accounts/email/change/$',
        wikipendium.user.views.change_email),
]
