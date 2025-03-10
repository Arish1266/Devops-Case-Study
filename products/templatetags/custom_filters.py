from django import template

register = template.Library()

@register.filter
def truncate_chars(value, max_length):
    """
    Truncate a string to a specified number of characters with ellipsis.
    """
    if not value:
        return ''
    
    # Remove leading/trailing whitespace
    value = value.strip()
    
    # If the string is already shorter than max_length, return it
    if len(value) <= max_length:
        return value
    
    # Truncate and add ellipsis
    return value[:max_length].rsplit(' ', 1)[0] + '...'