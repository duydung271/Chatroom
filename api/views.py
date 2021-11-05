from django.http.response import JsonResponse
from django.views import View
from django.core import serializers
from django.contrib.auth.models import User

from chatroom.models import Room
from chatroom.views import room

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
            data["friends"] = user.profile.friends
        except:
            pass

        return JsonResponse(data, safe=False)

class RoomAPI(View):
    def get(self, request, room_name):
        data={}
        try:
            data['room_name']=room_name
            room = Room.objects.get(room_name=room_name)
            data['cover']=room.cover.url
        except:
            pass
        return JsonResponse(data, safe=False)
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


class FriendAPI(View):
    def get(self, request, user1, user2):
        data = {"status":"success!"}
        try:
            user_1= User.objects.get(username=user1)
            user_2= User.objects.get(username=user2)
            user_1.profile.add_friend(user2)
            user_2.profile.add_friend(user1)
        except:
            data["status"]="Fail"
        return JsonResponse(data, safe=False)
    def delete(self, request, user1, user2):
        data = {"status":"success!"}
        try:
            user_1= User.objects.get(username=user1)
            user_2= User.objects.get(username=user2)
            user_1.profile.unfriend(user2)
            user_2.profile.unfriend(user1)
        except:
            data["status"]="Fail"
        return JsonResponse(data, safe=False)
