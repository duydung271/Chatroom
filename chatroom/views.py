from django.shortcuts import render

# Create your views here.

def index(request):
    context ={}
    return render(request, 'chatroom/index.html', context)

def room(request, room_name):
    context ={'room_name':room_name}
    return render(request,'chatroom/room.html', context)