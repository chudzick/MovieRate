from django import template

register = template.Library()


@register.filter
def replace_pipe_with_comma(value):
    return value.replace('|', ", ")
