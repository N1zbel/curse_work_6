from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def mediafile(value):
    return f'/media/{value}'


@register.filter
def media_url(value):
    media_root = settings.MEDIA_URL
    return f"{media_root}{value}"
