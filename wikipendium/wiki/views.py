from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from wikipendium.wiki.models import Article, ArticleContent
from wikipendium.wiki.forms import ArticleForm
from wikipendium.wiki.langcodes import LANGUAGE_NAMES
from django.contrib.auth.models import User
import diff
import urllib
import hashlib


def article(request, slug, lang="en"):

    try:
        article = Article.objects.get(slug=slug.upper())
    except:
        return no_article(request, slug.upper(), lang)

    articleContent = article.get_newest_content(lang)
    if articleContent is None:
        return missing_language(request, article, lang)

    if request.path != article.get_absolute_url(lang):
        return HttpResponseRedirect(article.get_absolute_url(lang))

    contributors = articleContent.get_contributors()

    content = articleContent.get_html_content()
    available_languages = article.get_available_languages(articleContent)
    language_list = map(lambda x: (x[0], x[1].get_absolute_url),
                        available_languages or [])

    return render(request, 'article.html', {
        "mathjax": True,
        "content": content['html'],
        "toc": content['toc'],
        "articleContent": articleContent,
        "language_list": language_list,
        'contributors': contributors,
        "share_url": "http://" + request.META['HTTP_HOST'] +
        request.get_full_path(),
    })


def no_article(request, slug, lang="en"):
    create_url = "/" + slug + "/add_language/"
    return render(request, 'no_article.html', {
        "slug": slug,
        "create_url": create_url,
    })


def missing_language(request, article, lang="en"):
    language_name = ""
    language_does_not_exist = False
    create_url = "/" + article.get_slug() + "/" + lang + "/edit/"

    if lang in LANGUAGE_NAMES:
        language_name = LANGUAGE_NAMES[lang].lower()
    else:
        language_does_not_exist = True

    available_languages = article.get_available_languages()
    language_list = map(lambda x: (x[0], x[1].get_absolute_url),
                        available_languages or [])

    return render(request, 'missing_language.html', {
        "create_url": create_url,
        "language_name": language_name,
        "available_languages": language_list,
        "language_does_not_exist": language_does_not_exist,
    })


@login_required
def new(request):
    slug = ''
    if request.POST:
        slug = request.POST.get('slug')
    return edit(request, slug.upper(), None)


@login_required
def add_language(request, slug):
    return edit(request, slug, None)


@login_required
def edit(request, slug, lang='en'):
    article = None
    articleContent = None
    try:
        article = Article.objects.get(slug=slug)
    except:
        article = Article(slug=slug)

    articleContent = article.get_newest_content(lang)
    if articleContent is None:
        articleContent = ArticleContent(article=article, lang=lang)

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            if not article.pk:
                article.save()

            new_articleContent = form.save(commit=False)
            new_articleContent.article = article
            new_articleContent.edited_by = request.user
            if lang is not None:
                new_articleContent.lang = lang
            if articleContent.pk is not None:
                new_articleContent.lang = articleContent.lang
                new_articleContent.parent = articleContent
            new_articleContent.save()
            if articleContent.pk is not None:
                articleContent.child = new_articleContent
                articleContent.save(change_updated_time=False)
            return HttpResponseRedirect(new_articleContent.get_absolute_url())
    else:
        form = ArticleForm(instance=articleContent)

    available_languages = article.get_available_languages(articleContent)
    language_list = map(lambda x: (x[0], x[1].get_edit_url),
                        available_languages or [])

    return render(request, 'edit.html', {
        "mathjax": True,
        "language_list": language_list,
        "articleContent": articleContent,
        "form": form
    })


def history(request, slug, lang="en"):
    article = Article.objects.get(slug=slug)
    articleContents = article.get_sorted_contents(lang=lang)

    originalArticle = article.get_newest_content(lang=lang)

    return render(request, "history.html", {
        "articleContents": articleContents,
        "back_url": originalArticle.get_absolute_url,
        "article": article
    })


def history_single(request, slug, lang="en", id=None):
    article = Article.objects.get(slug=slug)

    ac = ArticleContent.objects.get(id=id)

    ac.diff = diff.textDiff(
        ac.parent.content if ac.parent else '',
        ac.content
    )

    originalArticle = article.get_newest_content(lang=lang)

    return render(request, 'history_single.html', {
        'ac': ac,
        'next_ac': ac.child,
        'prev_ac': ac.parent,
        'back_url': originalArticle.get_absolute_url
    })


def user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    contributions = ArticleContent.objects.filter(
        edited_by=user).order_by('-updated')

    email = user.email
    default = "mm"
    size = 150

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + \
        hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
    return render(request, "user.html", {
        "user": user,
        "contributions": contributions,
        "gravatar": gravatar_url
    })
