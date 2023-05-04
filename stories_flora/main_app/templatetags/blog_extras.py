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


# <img src="/media/https%3A/flora-cdn.tu-ilmenau.de/help/title_story83.jpg" alt="Title image">
# <img src="/media/stories/title_image/title_image_1223-de_84_0.jpeg" alt="Title image">
# "title_image": "https://flora-cdn.tu-ilmenau.de/help/title_story84.jpg"



@register.filter
def unquote_new(value):
    return unquote(value)

@register.filter
def remove_media(value):
    if value[7] == 'h':  # /media/https...
        return value[7:]  # https...
    else:
        return value

