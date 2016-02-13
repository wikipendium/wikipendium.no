# -*- coding: utf8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from wikipendium.sitemap import ArticleSitemap
from wikipendium.wiki.feeds import ArticleLatestChangesRSSFeed
from wikipendium.wiki.models import Article
from wikipendium.cache.decorators import cache
from haystack.views import SearchView
import wikipendium.wiki.views
import wikipendium.stats.urls
import wikipendium.upload.urls
import wikipendium.user.urls

sitemaps = {
    'articles': ArticleSitemap,
}

admin.autodiscover()

article_regex = ur'(?P<slug>[' + Article.slug_regex + ']+)[^/]*'

article_patterns = [
    url(r'^add_tag/$', wikipendium.wiki.views.add_tag_to_article),
    url(r'^edit/$', wikipendium.wiki.views.edit),
    url(r'^history/$', wikipendium.wiki.views.history),
    url(r'^history/(?P<id>\d+)/$', wikipendium.wiki.views.history_single),
    url(r'^rss/$', ArticleLatestChangesRSSFeed()),
    url(r'^history/(?P<id>\d+)/rendered/$',
        wikipendium.wiki.views.history_single_rendered),
]

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/', include(wikipendium.stats.urls)),
    url(r'^upload/', include(wikipendium.upload.urls)),
    url(r'^search/partial/',
        cache(SearchView(template='search/results.partial.html'),
              key=lambda request:
              'wikipendium.wiki.partial_search_view(q=%s)' %
              request.META['QUERY_STRING'])),
    url(r'^search/$', wikipendium.wiki.views.home),
    url(r'^$', wikipendium.wiki.views.home, name='home'),
    url(r'^new/(?P<slug>[' + Article.slug_regex + ']+)?$',
        wikipendium.wiki.views.new, name='newarticle'),
    url(r'^preview/$', wikipendium.wiki.views.preview),

    url(r'^', include(wikipendium.user.urls)),

    url(r'^tag/(?P<tag_slug>[a-zA-Z0-9_-]+)/$', wikipendium.wiki.views.tag),

    url(r'^' + article_regex + '/$',
        RedirectView.as_view(url='/%(slug)s', permanent=True)),

    url(r'^' + article_regex + '$', wikipendium.wiki.views.article),
    url(r'^' + article_regex + '/',
        include(article_patterns)),
    url(r'^' + article_regex + '/add_language/((?P<lang>[a-z]+)/)?$',
        wikipendium.wiki.views.add_language),

    url(r'^' + article_regex + '/(?P<lang>[a-z]+)/$',
        wikipendium.wiki.views.article),
    url(r'^' + article_regex + '/(?P<lang>[a-z]+)/',
        include(article_patterns)),
]
