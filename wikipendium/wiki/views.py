from django.shortcuts import render
from wiki.models import Article, ArticleContent
from markdown2 import markdown

def home(request):
    return render(request, 'index.html')

def article(request, slug):
    article = Article.objects.get(slug=slug)
    articleContent = ArticleContent.objects.order_by('-updated')[0:1].get()
    content = markdown(articleContent.content)
    return render(request, 'article.html', {
        "slug": article.slug,
        "content": content,
        "title": articleContent.title
        })
