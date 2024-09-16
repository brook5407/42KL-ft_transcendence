import json
from django import template

register = template.Library()

@register.filter
def serialize_flash_messages(messages):
    return [
        {
            'message': message.message,
            'tags': message.tags
        }
        for message in messages
    ]