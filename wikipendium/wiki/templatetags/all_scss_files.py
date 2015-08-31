from django import template
from django.contrib.staticfiles import finders
from wikipendium import settings
import operator
import re


register = template.Library()


@register.simple_tag
def all_scss_files():
    '''
    Finds all .scss files that are in a scss folder in all staticfiles search
    locations, and returns a list of HTML <link> tags that contain references
    to those .scss files ready for consumption by e.g. django-compressor.
    '''

    # First, we need to get all the django.contrib.staticfiles
    # finders that are loaded for this project, since the common
    # finders interface does not support generic file listings.
    all_finders = [finders.get_finder(finder)
                   for finder in settings.STATICFILES_FINDERS]

    # For each of the finders, we get a get a list of all the
    # the static files available, and filter out all files
    # that are not .scss files.
    all_found_scss_files = reduce(operator.add, [
        filter(lambda filename: re.match('scss/[^/]*.scss$', filename),
               [filename for filename, _ in finder.list('')])
        for finder in all_finders])

    # Finally, we wrap in HTML <link> tags and return
    return '\n'.join(
        ['<link rel=stylesheet href=%s%s type=text/x-scss />' %
         (settings.STATIC_URL, filename)
         for filename in all_found_scss_files])
