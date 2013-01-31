from django.contrib import admin
from wikipendium.wiki.models import Article, ArticleContent

admin.site.register(Article)
admin.site.register(ArticleContent)
