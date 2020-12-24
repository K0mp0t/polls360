from django.urls import path, include
from .views import *

urlpatterns = [
    path('', polls, name='polls'),
    path(r'<int:poll_id>/', poll, name='poll'),
    path(r'new/', new_poll, name='new_poll'),
    path(r'delete/<int:poll_id>/', delete_poll, name='delete_poll'),
]
