from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.backends.default.urls')),

     url(r'^$', 'wiki.views.home', name='home'),
)
