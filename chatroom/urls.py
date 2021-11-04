from django.urls import path


from . import views
app_name = 'chatroom'
urlpatterns = [
     path('join/', views.index, name='index'),
    path('join/<str:room_name>/', views.index_join, name='index_join'),
    path('create/', views.index_create, name='index_create'),
    path('<str:room_name>/', views.room, name='room'),
]
