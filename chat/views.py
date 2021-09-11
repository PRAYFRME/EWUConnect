from django.shortcuts import render
from .models import Message
from users.models import ProfileModel, UserModel

def index(request):
    profile = ProfileModel.objects.get(user= request.user)
    context = {
        "profile" : profile, 
    }
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
    messages = Message.objects.filter(room=room_name)[0:25]

    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})