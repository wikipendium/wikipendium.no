from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson
from wiki.models import Article, ArticleContent
from wiki.forms import ArticleForm
from markdown2 import markdown

def home(request):

    articleContents = ArticleContent.objects.all()

    trie = []
    for ac in articleContents:
        article = Article.objects.get(articlecontent=ac)
        trie.append(article.slug+' '+ac.title)

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

def edit(request, slug):
    article = Article.objects.get(slug=slug)
    articleContent = ArticleContent.objects.order_by('-updated')[0:1].get()
    if request.method == 'POST': # If the form has been submitted...
        form = ArticleForm(request.POST) # A form bound to the POST data
        new_article = form.save(commit=False)
        new_article.article = article
        new_article.lang = articleContent.lang
        new_article.save()
        #if form.is_valid(): # All validation rules pass
        # Process the data in form.cleaned_data
        # ...
        #form.save()
    else:
        form = ArticleForm(instance=articleContent)
    return render(request, 'edit.html', {
        "slug": article.slug,
        "form": form
        })
