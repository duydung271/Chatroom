from django import forms

class JoinChatroomForm(forms.Form):
    room_name=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Room Name",
                "class": "form-control"
            }
        ), required=False
    )
    password=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ), required=False
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