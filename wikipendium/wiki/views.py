from django.shortcuts import render
from wiki.models import Article

def home(request):
    return render(request, 'index.html')

def article(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'article.html', {article: article})
