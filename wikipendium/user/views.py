from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from wikipendium.wiki.models import ArticleContent
from wikipendium.user.forms import UserChangeForm, EmailChangeForm
from django.contrib.auth.models import User
import hashlib
import urllib
from collections import defaultdict
from registration.backends.simple.views import RegistrationView


def profile(request, username):
    user = get_object_or_404(User, username=username)

    contribution_article_contents = (
        ArticleContent.objects.filter(edited_by=user)
                              .order_by('-updated')
                              .select_related('article', 'edited_by')
    )

    contributions = defaultdict(list)
    for article_content in contribution_article_contents:
        contributions[(article_content.article,
                       article_content.lang)].append(article_content)

    email = user.email
    default = 'mm'
    size = 300

    # construct the url
    gravatar_url = 'https://www.gravatar.com/avatar/' + \
        hashlib.md5(email.lower()).hexdigest() + '?'
    gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
    return render(request, 'user/profile.html', {
        'user': user,
        'contributions': sorted(contributions.items(),
                                key=lambda item:
                                item[1][0].get_last_descendant()
                                .get_full_title()),
        'gravatar': gravatar_url
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
                'username': new_username,
            })

    return render(request, 'user/change_username.html', {
        'form': user_change_form,
    })


@login_required
def change_email(request):
    email_change_form = EmailChangeForm()

    if request.method == 'POST':
        email_change_form = EmailChangeForm(request.POST)
        if email_change_form.is_valid():
            new_email = email_change_form.cleaned_data['email']
            request.user.email = new_email
            request.user.save()

            return render(request, 'user/change_email_complete.html', {
                'email': new_email,
            })

    return render(request, 'user/change_email.html', {
        'form': email_change_form,
        'email': request.user.email,
    })


class WikipendiumRegistrationView(RegistrationView):
    def get_success_url(self, request=None, user=None):
        return '/'
