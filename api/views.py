from django.http.response import JsonResponse
from django.views import View
from django.core import serializers
from django.contrib.auth.models import User

from chatroom.models import Room

class UserInfor(View):
    def get(self, request, username):
        data = {}
        try:
            user = User.objects.get(username=username)
            data["username"]=user.username
            data["avatar_url"]=user.profile.avatar.url
            data["cover_url"]=user.profile.cover.url
            data["status"]=user.status.status
            if (data["status"]=="offline"):
                data["last_login"]=user.last_login.strftime("%d/%m/%Y")
            else:
                data["last_login"]=""
            
        except:
            pass

        return JsonResponse(data, safe=False)

class RoomAPI(View):
    def delete(self, request, room_name):
        data = {"status":"success!"}
        try:
            room= Room.objects.get(room_name=room_name)
            if request.user.username==room.host:
                room.delete()
            else:
                data["status"]="Fail"
        except:
            data["status"]="Fail"
        return JsonResponse(data, safe=False)


class DeleteUserInRoomAPI(View):
    def delete(self, request, room_name, username):
        data = {"status":"success!"}
        try:
            room= Room.objects.get(room_name=room_name)
            room.delete_user(username)
            print("xoa user")
        except:
            data["status"]="Fail"
        return JsonResponse(data, safe=False)
