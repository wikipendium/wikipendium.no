from django.shortcuts import render
from wiki.models import Article

def home(request):
    return render(request, 'index.html')

def article(request, slug):
    article = Article.objects.get(slug=slug)
    print article.slug
    print slug
    return render(request, 'article.html', {slug: article.slug})
