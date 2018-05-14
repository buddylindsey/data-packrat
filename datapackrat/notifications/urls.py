from django.urls import path

from .views import UnreadNotificationsView, MarkAsReadView

urlpatterns = [
    path('', UnreadNotificationsView.as_view(), name='notifications'),
    path('mark_as_read/', MarkAsReadView.as_view(), name='mark_as_read')
]