from django import template

from newsapp.models import Post

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()

@register.simple_tag
def total_posts_count(post_type=None):
    queryset = Post.objects.all()
    if post_type:
        queryset = queryset.filter(post_type=post_type)
    return queryset.count()

