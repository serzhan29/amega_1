from django.urls import path
from .views import chat_room, send_message

urlpatterns = [
    path('chat/<int:sender_id>/<int:receiver_id>/', chat_room, name='chat_room'),
    path('send_message/', send_message, name='send_message'),
]
