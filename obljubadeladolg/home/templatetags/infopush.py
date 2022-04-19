from django import template
from home.models.settings import Infopush

register = template.Library()

# Infopush snippets
@register.inclusion_tag('home/tags/infopush.html', takes_context=True)
def infopush(context):
    return {
        'infopushes': Infopush.objects.filter(),
        'request': context['request'],
    }