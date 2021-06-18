from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    try:
        return indexable[i]
    except IndexError:
        return None

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
