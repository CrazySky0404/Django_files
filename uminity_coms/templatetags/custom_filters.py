from django import template

register = template.Library()

@register.filter
def pluralize_ukr(value):
    if value == 1:
        return ''
    elif 2 <= value <= 4:
        return 'і'
    else:
        return 'ів'
