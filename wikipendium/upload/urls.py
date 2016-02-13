from django.conf.urls import url
import wikipendium.upload.views


urlpatterns = [
    url(r'$', wikipendium.upload.views.upload),
]
