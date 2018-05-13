from django import forms

from .models import Message

class MarkAsReadForm(forms.Form):

    def mark_as_read(self):
        Message.objects.filter(
            status=Message.UNREAD).update(status=Message.READ)