from notifications.models import Message

from django_jinja import library

@library.global_function
def notification_count():
    return Message.objects.filter(status=Message.UNREAD).count()
