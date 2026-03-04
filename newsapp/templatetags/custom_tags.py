from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    data = context['request'].GET.copy()
    for key, value in kwargs.items():
        data[key] = value
    return data.urlencode()
