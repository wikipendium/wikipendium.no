from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from wikipendium.wiki.models import Article, ArticleContent
from wikipendium.wiki.forms import (
    NewArticleForm, AddLanguageArticleForm, EditArticleForm
    )
from wikipendium.wiki.langcodes import LANGUAGE_NAMES
from wikipendium.cache.decorators import cache_page_per_user
from taggit.models import Tag
import diff
import json
import itertools


@cache_page_per_user
def home(request):

    all_newest_contents = Article.get_all_newest_contents_all_languages()

    compendiums = [{
        'label': ac.get_full_title(),
        'url': ac.get_absolute_url(),
        'lang': ac.lang,
        'updated': str(ac.updated),
    } for ac in all_newest_contents]

    return render(request, 'index.html', {
        'compendiums': json.dumps(compendiums),
    })


@cache_page_per_user
def _cachable_article(request, articleContent, lang='en'):
    contributors = articleContent.get_contributors()

    content = articleContent.get_html_content()
    available_languages = articleContent.article.get_available_languages(
        articleContent)
    language_list = map(lambda x: (x[0], x[1].get_absolute_url),
                        available_languages or [])

    return render(request, 'article.html', {
        'mathjax': True,
        'content': content['html'],
        'toc': content['toc'],
        'articleContent': articleContent,
        'language_list': language_list,
        'contributors': contributors,
    })


def article(request, slug, lang='en'):

    try:
        article = Article.objects.get(slug=slug.upper())
    except:
        return no_article(request, slug.upper())

    articleContent = article.get_newest_content(lang)

    if articleContent is None:
        language_codes = article.get_available_language_codes()
        if len(language_codes) == 1:
            new_lang = language_codes[0]
            return HttpResponseRedirect(article.get_absolute_url(new_lang))
        return missing_language(request, article, lang)

    if request.path != article.get_absolute_url(lang):
        return HttpResponseRedirect(article.get_absolute_url(lang))
    return _cachable_article(request, articleContent, lang=lang)


@cache_page_per_user
def tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    articles_with_tag = Article.objects.filter(tags=tag)
    all_newest_contents = Article.get_all_newest_contents_all_languages()
    filtered_contents = filter(lambda ac: ac.article in articles_with_tag,
                               all_newest_contents)
    if len(filtered_contents) == 0:
        raise Http404
    compendiums = [{
        'label': ac.get_full_title(),
        'url': ac.get_absolute_url(),
        'lang': ac.lang,
        'updated': str(ac.updated),
    } for ac in filtered_contents]

    return render(request, 'index.html', {
        'compendiums': json.dumps(compendiums),
        'tag': tag,
    })


@csrf_exempt
def add_tag_to_article(request, slug):

    if not request.POST:
        return HttpResponseBadRequest()

    article = get_object_or_404(Article, slug=slug)

    if 'tag' not in request.POST:
        return HttpResponseBadRequest()

    slug = original_slug = slugify(request.POST['tag'])
    for i in itertools.count(1):
        try:
            tag, _ = Tag.objects.get_or_create(
                name=request.POST['tag'],
                slug=slug)
            break
        except:
            slug = '%s-%d' % (original_slug, i)
    article.tags.add(tag)
    return HttpResponse(json.dumps({
        'name': tag.name,
        'slug': tag.slug
    }))


def no_article(request, slug):
    create_url = '/new/' + slug
    return render(request, 'no_article.html', {
        'slug': slug,
        'create_url': create_url,
    })


def missing_language(request, article, lang='en'):
    language_name = ''
    language_does_not_exist = False
    create_url = '/' + article.get_slug() + '/add_language/' + lang + '/'

    if lang in LANGUAGE_NAMES:
        language_name = LANGUAGE_NAMES[lang].lower()
    else:
        language_does_not_exist = True

    available_languages = article.get_available_languages()
    language_list = map(lambda x: (x[0], x[1].get_absolute_url),
                        available_languages or [])

    return render(request, 'missing_language.html', {
        'create_url': create_url,
        'language_name': language_name,
        'available_languages': language_list,
        'language_does_not_exist': language_does_not_exist,
    })


@login_required
def new(request, slug=None):
    if request.POST:
        form = NewArticleForm(request.POST)
        if form.is_valid():
            slug = request.POST.get('slug')
            article = Article(slug=slug)
            article.save()

            articleContent = form.save(commit=False)
            articleContent.article = article
            articleContent.edited_by = request.user
            articleContent.save()
            return HttpResponseRedirect(articleContent.get_absolute_url())
    else:
        articleContent = None
        if slug:
            slug = slug.upper()
            articleContent = ArticleContent(article=Article(slug=slug),
                                            lang=None)
        form = NewArticleForm(instance=articleContent)

    return render(request, 'edit.html', {
        'mathjax': True,
        'form': form,
        'title': 'Create compendium',
    })


@login_required
def add_language(request, slug, lang=None):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        form = AddLanguageArticleForm(article, request.POST)
        if form.is_valid():
            articleContent = form.save(commit=False)
            articleContent.article = article
            articleContent.edited_by = request.user
            articleContent.save()
            return HttpResponseRedirect(articleContent.get_absolute_url())
    else:
        form = AddLanguageArticleForm(article=article, lang=lang)

    available_languages = article.get_available_languages()
    language_list = map(lambda x: (x[0], x[1].get_edit_url),
                        available_languages or [])

    return render(request, 'edit.html', {
        'mathjax': True,
        'language_list': language_list,
        'form': form,
        'title': 'Add language: ' + article.slug,
    })


@login_required
def edit(request, slug, lang='en'):
    article = get_object_or_404(Article, slug=slug)
    articleContent = article.get_newest_content(lang)

    if request.method == 'POST':
        new_articleContent = ArticleContent(article=article, lang=lang)
        form = EditArticleForm(request.POST, instance=new_articleContent)
        if form.is_valid():
            new_articleContent.article = article
            new_articleContent.edited_by = request.user
            new_articleContent.parent = articleContent
            new_articleContent.save()

            articleContent.child = new_articleContent
            articleContent.save(change_updated_time=False)

            return HttpResponseRedirect(new_articleContent.get_absolute_url())
    else:
        form = EditArticleForm(instance=articleContent)

    available_languages = article.get_available_languages(articleContent)
    language_list = map(lambda x: (x[0], x[1].get_edit_url),
                        available_languages or [])

    return render(request, 'edit.html', {
        'mathjax': True,
        'language_list': language_list,
        'articleContent': articleContent,
        'form': form,
        'title': 'Edit: ' + article.slug,
    })


@csrf_exempt
def preview(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        articleContent = ArticleContent(content=content)
        html = articleContent.get_html_content()
        return JsonResponse(html)
    return JsonResponse({'error': 'Method not allowed'})


def history(request, slug, lang='en'):
    try:
        article = Article.objects.get(slug=slug)
    except:
        return no_article(request, slug.upper(), lang)

    articleContents = article.get_sorted_contents(lang=lang)

    originalArticle = article.get_newest_content(lang=lang)

    return render(request, 'history.html', {
        'articleContents': articleContents,
        'back_url': originalArticle.get_absolute_url,
        'article': article
    })


def history_single(request, slug, lang='en', id=None):
    try:
        article = Article.objects.get(slug=slug)
    except:
        return no_article(request, slug.upper(), lang)

    ac = ArticleContent.objects.get(id=id)

    @cache_page_per_user
    def cachable_history_single(request, ac, has_parent,
                                has_child, lang='en', id=None):

        ac.diff = diff.render_diff_as_html(
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

    return cachable_history_single(request, ac, bool(ac.parent),
                                   bool(ac.child), lang=lang, id=id)
