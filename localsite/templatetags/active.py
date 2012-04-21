from django import template
register = template.Library()


@register.simple_tag
def active(request, pattern):

    if pattern == '/' and request.path == '/':
        return ' active'
    elif pattern == '/':
        return ''
    elif request.path.startswith(pattern):
        return ' active'
    return ''
