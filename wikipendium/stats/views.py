from django.shortcuts import render
from wikipendium.wiki.models import Article
from django.utils import timezone


def index(request):
    acs = Article.get_all_newest_contents_all_languages()
    now = timezone.now()

    acs_updated_in_the_last_24_hours = filter(
        lambda ac: ac.updated > now - timezone.timedelta(hours=24), acs)
    return render(request, 'stats/index.html', {
        'number_of_acs_updated_in_the_last_24_hours':
            len(acs_updated_in_the_last_24_hours)
    })
