from haystack import indexes
from wikipendium.wiki.models import Article, ArticleContent


class ArticleContentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='content')
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return ArticleContent

    def index_queryset(self, using=None):
        return ArticleContent.objects.filter(
            pk__in=[ac.pk
                    for ac in Article.get_all_newest_contents_all_languages()])
