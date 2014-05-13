from django.shortcuts import render, get_object_or_404
from wikipendium.wiki.models import ArticleContent
from django.contrib.auth.models import User
import hashlib
import urllib
from collections import defaultdict


def profile(request, username):
    user = get_object_or_404(User, username=username)

    contribution_article_contents = ArticleContent.objects.filter(
        edited_by=user).order_by('-updated')

    contributions = defaultdict(list)
    for article_content in contribution_article_contents:
        contributions[(article_content.article,
                       article_content.lang)].append(article_content)

    email = user.email
    default = "mm"
    size = 150

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + \
        hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
    return render(request, 'user/profile.html', {
        "user": user,
        "contributions": sorted(contributions.items(),
                                key=lambda item:
                                item[1][0].get_last_descendant()
                                .get_full_title()),
        "gravatar": gravatar_url
    })
