from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from wiki.models import Article, ArticleContent
from wiki.forms import ArticleForm
from markdown2 import markdown

def home(request):

    articleContents = ArticleContent.objects.all().order_by('-updated')

    trie = []
    articleset = set([])
    for ac in articleContents:
        article = Article.objects.get(articlecontent=ac)
        if article.pk not in articleset:
            articleset.add(article.pk)
            trie.append({
                "label": ac.get_full_title(),
                "url": ac.get_url()
                })

    return render(request, 'index.html', {"trie":simplejson.dumps(trie)})

def article(request, slug):
    article = Article.objects.get(slug=slug)
    articleContent = ArticleContent.objects.filter(article=article).order_by('-updated')[0:1].get()
    content = markdown(articleContent.content)
    return render(request, 'article.html', {
        "articleContent": articleContent,
        "content": content
        })

def edit(request, slug):
    article = Article.objects.get(slug=slug)
    articleContent = ArticleContent.objects.filter(article=article).order_by('-updated')[0:1].get()
    if request.method == 'POST': # If the form has been submitted...
        form = ArticleForm(request.POST) # A form bound to the POST data
        new_article = form.save(commit=False)
        new_article.article = article
        new_article.lang = articleContent.lang
        new_article.save()
        return HttpResponseRedirect(new_article.get_url())
    else:
        form = ArticleForm(instance=articleContent)
    return render(request, 'edit.html', {
        "slug": article.slug,
        "form": form
        })
