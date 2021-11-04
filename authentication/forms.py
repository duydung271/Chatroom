
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class ProfileForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id":"first_name",
                "placeholder": "Enter your first name",
                "class": "form-control"
            }
        ), required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id":"last_name",
                "placeholder": "Also your last name",
                "class": "form-control"
            }
        ), required=True
    )
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "id":"birthday",
                "placeholder": "mm/dd/yyyy",
                "class": "form-control",
                "data-datepicker":"",
                "type":"text",
            }
        ),
    )
    gender = forms.TypedChoiceField(
        widget=forms.Select(
            attrs={
                "id":"gender",
                "class": "form-select mb-0",
                "aria-label":"Gender select example"
            },
        ),
        choices=((0,"Gender"),(1,"Female"),(2,"Male")),
        coerce = str
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "phone",
                "placeholder": "0123 456 789",
                "class": "form-control",
                "type": "number"
            }
        )
    )


class avatarProfileForm(forms.Form):
    img_avatar = forms.ImageField(required=True, label="",
        widget=forms.FileInput({
            'id':'avatar_file'
        })
    )

class coverProfileForm(forms.Form):
    img_cover = forms.ImageField(required=True,label="",
        widget=forms.FileInput({
            'id':'cover_file'
        })
    )