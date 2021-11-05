from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from authentication.models import Profile, Status
from .forms import LoginForm, ProfileForm, avatarProfileForm, SignUpForm, coverProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home:home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True
            login(request, user)
            Profile.objects.create(user=request.user)
            Status.objects.create(user=request.user)
            return redirect(reverse('profile', kwargs={"username": username}))
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url='login')
def profileView(request,username):
    context = {'segment': 'profile'}
    user = User.objects.get(username=username)
    if user.is_authenticated:
        context['user']=user
        profile = user.profile

        data_profile={'first_name': user.first_name,
            'last_name': user.last_name,
            'gender':profile.gender,
            'phone': profile.phone,
            'birthday': profile.birthday.strftime("%m/%d/%Y"),
        }
        #request avatar from user
        avatar_form = avatarProfileForm(request.POST,request.FILES)
        if avatar_form.is_valid():
            profile.avatar=avatar_form.cleaned_data['img_avatar']
            profile.save()
        else:
            avatar_form = avatarProfileForm(None)
        #request cover from user
        cover_form = coverProfileForm(request.POST, request.FILES)
        if cover_form.is_valid():
            profile.cover=cover_form.cleaned_data['img_cover']
            profile.save()
        else:
            cover_form = coverProfileForm(None)

        #request profile data from user
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            profile.gender = form.cleaned_data['gender']
            profile.phone = form.cleaned_data['phone']
            profile.birthday = form.cleaned_data['birthday']
            profile.save()
            user.save()
        else:
            #protect information away others
            form = ProfileForm(initial=data_profile)
            if request.user.username != user.username:
                for i in data_profile:
                    form.fields[i].widget.attrs['disabled'] = True

        context['form']=form
        context['email']= user.email
        context['avatar_form']=avatar_form
        context['cover_form']=cover_form
        context['is_friend']=profile.is_friend(request.user.username)
    else:
        return redirect("/login/")
        # return ERROR
        #will return a user error 403
    html_template = loader.get_template('accounts/profile.html')
    return HttpResponse(html_template.render(context, request))


def forgotPasswordView(request):
    context = {'segment': 'forgot_password'}

    html_template = loader.get_template('accounts/page-forgot-password.html')
    return HttpResponse(html_template.render(context, request))

def resetPasswordView(request):
    context = {'segment': 'reset_password'}

    html_template = loader.get_template('accounts/page-reset-password.html')
    return HttpResponse(html_template.render(context, request))
