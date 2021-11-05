from django import forms

class IndexChatroomForm(forms.Form):
    room_name=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Room Name",
                "class": "form-control"
            }
        ), required=True
    )
    password=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ), required=False
    )
    cover = forms.ImageField(required=False, label="",
        widget=forms.FileInput({
            'name':"cover-form",
            'id':"cover-form"
        })
    )


class SettingChatroomForm(forms.Form):
    password=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "id":"settings_password"
            }
        ), required=False
    )
    kick=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter username",
                "class": "form-control",
                "id":"settings_kick"
            }
        ), required=False
    )