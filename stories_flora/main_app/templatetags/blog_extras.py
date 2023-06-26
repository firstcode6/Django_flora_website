import markdown

from django import template
from django.template.defaultfilters import stringfilter

from django.template.defaultfilters import register
from urllib.parse import unquote

register = template.Library()


@register.filter
@stringfilter
def convert_markdown(value):
    return markdown.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter
def unquote_new(value):
    # we receive:
    # media/https%3A/flora-cdn.tu-ilmenau.de/help/title_story71.jpg
    # media/http%3A/127.0.0.1%3A8000/stories/title_image/title_image_None-de_107_0.jpg
    value = unquote(value[7:])
    # it is converted:
    # https:/flora-cdn.tu-ilmenau.de/help/title_story71.jpg - it works
    # http:/127.0.0.1:8000/stories/title_image/title_image_None-de_107_0.jpg  it does not work
    value = value.replace(':/', '://')
    # it is converted:
    # https://flora-cdn.tu-ilmenau.de/help/title_story71.jpg - it works
    # http://127.0.0.1:8000/stories/title_image/title_image_None-de_107_0.jpg  it works
    return value
