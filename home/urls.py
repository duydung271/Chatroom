from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    # The home page
    path('', views.index, name='index'),
    path('home/', views.homeView, name='home'),
    path('components_buttons/', views.components_buttons),
    path('components_forms/', views.components_forms),
    path('components_modals/', views.components_modals),
    path('components_notifications/', views.components_notifications),
    path('components_typography/', views.components_typography),
]