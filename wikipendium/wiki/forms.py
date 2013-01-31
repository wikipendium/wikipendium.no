from django.forms import ModelForm
from wikipendium.wiki.models import Article, ArticleContent

class ArticleForm(ModelForm):
    class Meta:
        model = ArticleContent
        fields = ('title', 'content')

