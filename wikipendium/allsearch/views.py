from django.shortcuts import render
from django.utils import simplejson
from wikipendium.wiki.models import Article


def all_search(request):
    all_articles = Article.get_all_newest_contents()

    trie = [{
        "label": ac.get_full_title(),
        "url": ac.get_absolute_url(),
        "lang": ac.lang
    } for ac in all_articles]

    return render(request, 'all_articles.html', {
        "trie": simplejson.dumps(trie),
    })
