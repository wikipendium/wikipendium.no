from django.shortcuts import render
from wikipendium.wiki.models import Article
from django.utils import timezone
from collections import Counter
from django.utils.timezone import utc
from datetime import datetime
from wikipendium.cache.decorators import cache


def index(request):
    acs = Article.get_all_newest_contents_all_languages()
    now = timezone.now()

    acs_updated_in_the_last_24_hours = filter(
        lambda ac: ac.updated > now - timezone.timedelta(hours=24), acs)

    user_stats = _generate_user_statistics_for_one_day(
        year=now.year, month=now.month, day=now.day
    )

    return render(request, 'stats/index.html', {
        'number_of_acs_updated_in_the_last_24_hours':
            len(acs_updated_in_the_last_24_hours),
        'users': user_stats
    })


@cache
def _generate_user_statistics_for_one_day(year=None, month=None, day=None):
    now = datetime(year, month, day)
    now = now.replace(tzinfo=utc)
    users_24_hours = map(
        lambda a: a.edited_by,
        Article.get_all_contents(timezone.timedelta(hours=24), now)
        )
    users_week = map(
        lambda a: a.edited_by,
        Article.get_all_contents(timezone.timedelta(weeks=1), now)
        )
    users_month = map(
        lambda a: a.edited_by,
        Article.get_all_contents(timezone.timedelta(weeks=4), now)
        )

    user_most_contributions_24_hours = next(
        iter(Counter(users_24_hours).most_common(1)), [None, 0])
    user_most_contributions_week = next(
        iter(Counter(users_week).most_common(1)), [None, 0])
    user_most_contributions_month = next(
        iter(Counter(users_month).most_common(1)), [None, 0])

    return {
        'most_contrib_24_hours': {
            'user': user_most_contributions_24_hours[0],
            'contributions': user_most_contributions_24_hours[1],
        },
        'most_contrib_week': {
            'user': user_most_contributions_week[0],
            'contributions': user_most_contributions_week[1],
        },
        'most_contrib_month': {
            'user': user_most_contributions_month[0],
            'contributions': user_most_contributions_month[1],
        }
    }
