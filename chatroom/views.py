from django.shortcuts import redirect, render
from django.urls.base import reverse

from chatroom.forms import  SettingChatroomForm, IndexChatroomForm
from chatroom.models import Room

# Create your views here.

def index_join(request, room_name):
    form = IndexChatroomForm(request.POST.copy() or None,initial={'room_name':room_name})
    form.fields['room_name'].widget.attrs['disabled'] = True
    form.fields['cover'].widget.attrs['disabled'] = True
    form.fields['cover'].widget.attrs['style'] = "display:none;"

    context ={'notice':'', 'title':'Join', 'cover':'/media/join.png'}

    try:
        room=Room.objects.get(room_name=room_name)
        context['cover']=room.cover.url
        if len(room.password)==0:
            if not (request.user.username in room.get_list_user_names()):
                room.add_user(request.user.username)
            return redirect(reverse('chatroom:room', kwargs={"room_name": room_name}))
        form.data["room_name"]=room_name
        if form.is_valid():
            password = form.cleaned_data["password"]
            if (room.password == password):
                if not request.user.username in room.get_list_user_names():
                    room.add_user(request.user.username)
                return redirect(reverse('chatroom:room', kwargs={"room_name": room_name}))
            else:
                context['notice']='Wrong Password!'
    except:
        context['notice']='Wrong Room Name!'        

    context['form'] =form
    return render(request, 'chatroom/index.html', context)

def index(request):
    form = IndexChatroomForm(request.POST or None)
    form.fields['cover'].widget.attrs['disabled'] = True
    form.fields['cover'].widget.attrs['style'] = "display:none;"
    context ={'form':form,'title':'Join', 'notice':'', 'cover':'/media/join.png'}

    if (form.is_valid()):
        room_name = form.cleaned_data["room_name"]
        password = form.cleaned_data["password"]
        try:
            room=Room.objects.get(room_name=room_name)
            if (room.password == password):
                if not request.user.username in room.get_list_user_names():
                    room.add_user(request.user.username)
                return redirect(reverse('chatroom:room', kwargs={"room_name": room_name}))
            else:
                context['notice']='Wrong Password!'
        except:
            context['notice']='Wrong Name!'
    
    return render(request, 'chatroom/index.html', context)

def index_create(request):
    form = IndexChatroomForm(request.POST,request.FILES)
    context ={'title':'Create', 'notice':'', 'cover':'/media/create.png'}
    if (form.is_valid()):
        room_name = form.cleaned_data["room_name"]
        password = form.cleaned_data["password"]
        try:
            Room.objects.get(room_name=room_name)
            context['notice']='This name was used!'
        except:
            room = Room.objects.create(room_name=room_name, password=password, host=request.user.username)
            if form.cleaned_data['cover']:
                room.cover=form.cleaned_data['cover']
                room.save()
            room.add_user(request.user.username)
            return redirect(reverse('chatroom:room', kwargs={"room_name": room_name}))

    else:
        form = IndexChatroomForm(None)
    
    context['form']=form
    return render(request, 'chatroom/index.html', context)

def room(request, room_name):
    try:
        room=Room.objects.get(room_name=room_name)
    except:
        return redirect(reverse('home:page_404'))
    if not request.user.username in room.get_list_user_names():
         return redirect(reverse('home:page_403'))
    if request.method=='POST':
        setting_form = SettingChatroomForm(request.POST)
        if setting_form.is_valid():
            username= setting_form.cleaned_data["kick"]
            room.delete_user(username)
            password= setting_form.cleaned_data['password']
            room.password = password
            room.save()
    else:
        setting_form = SettingChatroomForm(initial={'password': room.password})
    context ={'room_name':room_name,'host':room.host,'setting_form':setting_form}
    return render(request,'chatroom/room.html', context)