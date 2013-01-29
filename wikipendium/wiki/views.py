from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson
from wiki.models import Article, ArticleContent
from markdown2 import markdown

def home(request):

    articleContents = ArticleContent.objects.all()

    trie = []
    for ac in articleContents:
        article = Article.objects.get(articlecontent=ac)
        trie.append(article.slug+': '+ac.title)

    return render(request, 'index.html', {"trie":simplejson.dumps(trie)})

def article(request, slug):
    article = Article.objects.get(slug=slug)
    articleContent = ArticleContent.objects.order_by('-updated')[0:1].get()
    content = markdown(articleContent.content)
    return render(request, 'article.html', {
        "slug": article.slug,
        "content": content,
        "title": articleContent.title
        })


