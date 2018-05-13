from django.views.generic import ListView, FormView
from django.urls import reverse_lazy

from .models import Message
from .forms import MarkAsReadForm

class UnreadNotificationsView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'notifications/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=Message.UNREAD)


class MarkAsReadView(FormView):
    success_url = reverse_lazy('notifications')
    form_class = MarkAsReadForm

    def form_valid(self, form):
        form.mark_as_read()
        return super().form_valid(form)
