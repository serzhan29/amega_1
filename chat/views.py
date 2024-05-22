from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Message
from users.models import User
from django.urls import reverse


def chat_room(request, sender_id, receiver_id):
    sender = User.objects.get(pk=sender_id)
    receiver = User.objects.get(pk=receiver_id)
    messages = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
    context = {'sender': sender, 'receiver': receiver, 'messages': messages}
    return render(request, 'chat/chat_room.html', context)


def send_message(request):
    if request.method == 'POST':
        sender_id = request.POST['sender_id']
        receiver_id = request.POST['receiver_id']
        content = request.POST['content']
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)
        message = Message.objects.create(sender=sender, receiver=receiver, content=content)
        return HttpResponseRedirect(reverse('chat_room', args=[sender_id, receiver_id]))
