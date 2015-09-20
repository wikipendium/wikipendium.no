from django.contrib.syndication.views import Feed
from wikipendium import settings
from wikipendium.wiki.models import Article
from wikipendium.wiki.models import ArticleContent


class ArticleLatestChangesRSSFeed(Feed):

    def get_object(self, request, slug=None, lang='en'):
        self.lang = lang
        return Article.objects.get(slug=slug)

    def link(self, obj):
        return '%s/%s/%s/' % (settings.BASE_URL, obj.slug, self.lang)

    def feed_url(self, obj):
        return self.link(obj)

    def items(self, obj):
        return ArticleContent.objects.filter(
            article=obj, lang=self.lang).order_by('-updated')[:5]

    def title(self, obj):
        return 'Recent changes to the %s (%s) compendium.' % (
            obj.slug, self.lang)

    def item_title(self, item):
        return '%s (#%s)' % (item.title, item.pk)

    def item_description(self, item):
        return 'Change by %s at %s.' % (item.edited_by, item.updated)

    def item_link(self, item):
        return '%s%s' % (settings.BASE_URL, item.get_history_single_url())
