# -*- coding: utf8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from wikipendium.sitemap import ArticleSitemap
from wikipendium.wiki.feeds import ArticleLatestChangesRSSFeed
from wikipendium.wiki.models import Article
from wikipendium.cache.decorators import cache
from haystack.views import SearchView

sitemaps = {
    'articles': ArticleSitemap,
}

admin.autodiscover()

article_regex = ur'(?P<slug>[' + Article.slug_regex + ']+)[^/]*'

article_patterns = patterns(
    'wikipendium.wiki.views',
    url(r'^add_tag/$', 'add_tag_to_article'),
    url(r'^edit/$', 'edit'),
    url(r'^preview/$', 'preview'),
    url(r'^history/$', 'history'),
    url(r'^history/(?P<id>\d+)/$', 'history_single'),
    url(r'^rss/$', ArticleLatestChangesRSSFeed()),
)

urlpatterns = patterns(
    'wikipendium.wiki.views',
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/', include('wikipendium.stats.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^upload/', include('wikipendium.upload.urls')),
    url(r'^search/partial/',
        cache(SearchView(template='search/results.partial.html'),
              key=lambda request:
              'wikipendium.wiki.partial_search_view(q=%s)' %
              request.META['QUERY_STRING'])),
    url(r'^search/$', 'home'),
    url(r'^$', 'home', name='home'),
    url(r'^new/(?P<slug>[' + Article.slug_regex + ']+)?$',
        'new', name='newarticle'),

    url(r'^', include('wikipendium.user.urls')),

    url(r'^tag/(?P<tag>[a-zA-Z0-9_-]+)/$', 'tag'),

    url(r'^' + article_regex + '/$',
        RedirectView.as_view(url='/%(slug)s', permanent=True)),

    url(r'^' + article_regex + '$', 'article'),
    url(r'^' + article_regex + '/',
        include(article_patterns)),
    url(r'^' + article_regex + '/add_language/((?P<lang>[a-z]+)/)?$',
        'add_language'),

    url(r'^' + article_regex + '/(?P<lang>[a-z]+)/$',
        'article'),
    url(r'^' + article_regex + '/(?P<lang>[a-z]+)/',
        include(article_patterns)),
)
