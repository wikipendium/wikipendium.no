from django.shortcuts import render
from wiki.models import Article, ArticleContent

def home(request):
    return render(request, 'index.html')

def article(request, slug):
    article = Article.objects.get(slug=slug)
    articleContent = ArticleContent.objects.order_by('-updated')[0:1].get()
    print articleContent.content
    return render(request, 'article.html', {
        "slug": article.slug,
        "content": articleContent.content,
        "title": articleContent.title
        })
