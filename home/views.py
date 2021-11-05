from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls.base import reverse

from chatroom.models import Room


def index(request):
    if  request.user.is_authenticated:
        return redirect(reverse('home:home'))
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def homeView(request):
    list_room = Room.objects.all()
    list_items=list()
    for room in list_room:
        infor={}
        infor['room_name']= room.room_name
        infor['cover']= room.cover.url
        infor['categories']='all'
        infor['host']=room.host
        if room.host==request.user.username:
            infor['categories']+=' '+'your'
        if request.user.profile.is_friend(room.host):
            infor['categories']+=' '+'friend'
        list_items.append(infor)

    context = {'segment': 'home', 'list_items': list_items}

    html_template = loader.get_template('home/home.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def friendView(request):
    context = {'segment': 'friends'}
    html_template = loader.get_template('home/friends.html')
    return HttpResponse(html_template.render(context, request))

def components_buttons(request):
    context = {'segment': 'components-buttons'}
    html_template = loader.get_template('home/components-buttons.html')
    return HttpResponse(html_template.render(context, request))

def components_forms(request):
    context = {'segment': 'components_forms'}
    html_template = loader.get_template('home/components-forms.html')
    return HttpResponse(html_template.render(context, request))


def components_modals(request):
    context = {'segment': 'components_modals'}
    html_template = loader.get_template('home/components-modals.html')
    return HttpResponse(html_template.render(context, request))


def components_notifications(request):
    context = {'segment': 'components_notifications'}
    html_template = loader.get_template('home/components-notifications.html')
    return HttpResponse(html_template.render(context, request))

def components_typography(request):
    context = {'segment': 'components_typography'}
    html_template = loader.get_template('home/components-typography.html')
    return HttpResponse(html_template.render(context, request))

def page_403(request):
    context = {'segment': 'page_403'}
    html_template = loader.get_template('home/page-403.html')
    return HttpResponse(html_template.render(context, request))

def page_404(request):
    context = {'segment': 'page_404'}
    html_template = loader.get_template('home/page-404.html')
    return HttpResponse(html_template.render(context, request))

def page_500(request):
    context = {'segment': 'page_500'}
    html_template = loader.get_template('home/page-500.html')
    return HttpResponse(html_template.render(context, request))