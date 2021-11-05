from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    # The home page
    path('', views.index, name='index'),
    path('home/', views.homeView, name='home'),
    path('friends/', views.friendView, name='friends'),
    path('components_buttons/', views.components_buttons),
    path('components_forms/', views.components_forms),
    path('components_modals/', views.components_modals),
    path('components_notifications/', views.components_notifications),
    path('components_typography/', views.components_typography),
    path('page_403/', views.page_403,name='page_403'),
    path('page_404/', views.page_404,name='page_404'),
    path('page_500/', views.page_500,name='page_500'),
]