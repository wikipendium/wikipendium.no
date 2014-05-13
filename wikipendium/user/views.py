from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from wikipendium.wiki.models import ArticleContent
from wikipendium.user.forms import UserChangeForm
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


@login_required
def change_username(request):
    user_change_form = UserChangeForm()

    if request.method == 'POST':
        user_change_form = UserChangeForm(request.POST)
        if user_change_form.is_valid():
            new_username = user_change_form.cleaned_data['username']
            request.user.username = new_username
            request.user.save()

            return render(request, 'user/change_username_complete.html', {
                "username": new_username,
            })

    return render(request, 'user/change_username.html', {
        'form': user_change_form,
    })
