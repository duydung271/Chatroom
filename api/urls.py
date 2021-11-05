from django.urls import path



from . import views
app_name = 'api'
urlpatterns = [
    path('infor/<str:username>/', views.UserInfor.as_view()),
    path('delete/<str:room_name>/', views.RoomAPI.as_view()),
    path('friend/<str:user1>/<str:user2>/', views.FriendAPI.as_view()),
    path('delete_user_in_room/<str:room_name>/<str:username>/', views.DeleteUserInRoomAPI.as_view()),
]
