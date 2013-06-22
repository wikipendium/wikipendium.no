from django import template

register = template.Library()


@register.inclusion_tag('language_chooser.html')
def language_chooser(language_list, articleContent):
    return {'language_list': language_list,
            'articleContent': articleContent
            }
