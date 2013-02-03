from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from wikipendium.wiki.models import Article, ArticleContent
from wikipendium.wiki.forms import ArticleForm
from markdown2 import markdown
from django.contrib.auth.models import User
import diff, urllib, hashlib
from collections import Counter


@login_required
def home(request):

    articleContents = ArticleContent.objects.all().order_by('-updated')

    counter = Counter()
    for ac in articleContents:
        counter[ac.article] += 1

    print [(a,b) for a,b in counter.items()]

    popularACs = []
    try:
        popularACs = [article.get_newest_content() for article,count in counter.most_common(6)]
    except:pass

    trie = []
    articleset = set([])
    for ac in articleContents:
        article = Article.objects.get(articlecontent=ac)
        if article.pk not in articleset:
            articleset.add(article.pk)
            trie.append({
                "label": ac.get_full_title(),
                "url": ac.get_url(),
                "lang": ac.lang
                })

    return render(request, 'index.html', {
        "trie":simplejson.dumps(trie),
        'popularACs': popularACs     
    })

@login_required
def article(request, slug, lang="en"):
    try:
        article = Article.objects.get(slug=slug)
        articleContent = article.get_newest_content(lang)
    except:
        return HttpResponseRedirect("/" + slug+ "/" + lang + '/edit')

    contributors = articleContent.get_contributors()
    
    content = markdown(articleContent.content, extras=["toc", "wiki-tables"], safe_mode=True)
    return render(request, 'article.html', {
        "content": content,
        "toc": (content.toc_html or "").replace('<ul>','<ol>').replace('</ul>','</ol>'),
        "articleContent": articleContent,
        'contributors': contributors,
        "share_url": request.META['HTTP_REFERER'] + request.get_full_path()[1:], 
        })

@login_required
def new(request):
    slug = ''
    if request.POST:
        slug = request.POST.get('slug')
    return edit(request, slug.upper())


@login_required
def edit(request, slug, lang=None):
    article = None
    articleContent = None
    try:
        article = Article.objects.get(slug=slug)
    except:
        article = Article(slug=slug)

    try:
        articleContent = article.get_newest_content(lang)
    except:
        articleContent = ArticleContent(article=article, lang=lang)
        pass

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            if not article.pk:
                article.save()
            new_articleContent = form.save(commit=False)
            new_articleContent.article = article
            new_articleContent.edited_by = request.user
            new_articleContent.lang = articleContent.lang
            new_articleContent.save(lang)
            return HttpResponseRedirect(new_articleContent.get_url())
    else:
        form = ArticleForm(instance=articleContent)
    return render(request, 'edit.html', {
        "articleContent": articleContent,
        "form": form
    })

@login_required
def history(request, slug, lang="en"):
    article = Article.objects.get(slug=slug)
    articleContents = article.get_sorted_contents(lang=lang)
    for ac in articleContents:
        ac.markdowned = markdown(ac.content, safe_mode=True)
    return render(request, "history.html", {
        "articleContents": articleContents
        })

def history_single(request, slug, id):
    article = Article.objects.get(slug=slug)

    articleContents = article.get_sorted_contents()

    aclist = filter(lambda ac: ac[1].pk == int(id), enumerate(articleContents))

    if not aclist:
        return HttpResponseRedirect('/'+article.get_history_url())
    i,ac = aclist[0]

    prev_ac = articleContents[i+1] if len(articleContents) > i+1 else None
    next_ac = articleContents[i-1] if i-1 >= 0 else None

    ac.diff = diff.textDiff(
        markdown(prev_ac.content, safe_mode=True) if prev_ac else '',
        markdown(ac.content, safe_mode=True)
    )

    return render(request, 'history_single.html', {
        'ac':ac,
        'next_ac': next_ac,
        'prev_ac':prev_ac
    })

def user(request, username):
    user = User.objects.get(username=username)
    contributions = ArticleContent.objects.filter(edited_by=user).order_by('-updated')

    email = user.email
    default = "http://www.example.com/default.jpg"
    size = 150

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return render(request, "user.html", {
        "user": user,
        "contributions": contributions,
        "gravatar": gravatar_url
        })
