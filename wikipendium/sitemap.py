from django.contrib.sitemaps import Sitemap
from wikipendium.wiki.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Article.get_all_newest_contents_all_languages()

    def lastmod(self, obj):
        return obj.updated
