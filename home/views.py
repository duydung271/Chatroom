from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def homeView(request):
    list_items =list()
  
    context = {'segment': 'home', 'list_items': list_items}

    html_template = loader.get_template('home/home.html')
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