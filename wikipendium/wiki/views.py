from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from wiki.models import Article, ArticleContent
from wiki.forms import ArticleForm
from markdown2 import markdown

@login_required
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

@login_required
def article(request, slug):
    article = Article.objects.get(slug=slug)
    articleContent = ArticleContent.objects.filter(article=article).order_by('-updated')[0:1].get()
    content = markdown(articleContent.content, extras=["toc"])
    return render(request, 'article.html', {
        "content": content,
        "toc": (content.toc_html or "").replace('<ul>','<ol>').replace('</ul>','</ol>'),
        "articleContent": articleContent
        })

@login_required
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
