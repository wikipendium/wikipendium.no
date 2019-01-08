from django.conf.urls import url
import wikipendium.stats.views

urlpatterns = [
    url(r'^$', wikipendium.stats.views.index),
]
