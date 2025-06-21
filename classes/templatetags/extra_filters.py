from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return False  # or None, or whatever you want as default
    return dictionary.get(key)
