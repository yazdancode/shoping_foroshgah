import markdown
from django import template
from django.template.defaultfilters import upper
from django.utils import timezone
from django.utils.safestring import mark_safe

from blog.models import Post

register = template.Library()


@register.simple_tag(name="total_posts")
def number_of_posts(is_today=False):
    today = timezone.now().date()
    if is_today:
        return Post.published.filter(publish__date=today).count()
    return Post.published.count()


@register.simple_tag(name="latest_posts")
def latest_posts(count=3):
    return Post.published.order_by("-publish")[:count]


@register.filter(name="markdown")
def markdown_format(text):
    if "script" not in text:
        return mark_safe(markdown.markdown(text))
    else:
        return ""
