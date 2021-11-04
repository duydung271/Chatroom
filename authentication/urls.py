from django.urls import path
from .views import login_view, profileView, register_user,forgotPasswordView,resetPasswordView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('profile/<str:username>/', profileView, name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('forgot_password/',forgotPasswordView, name='forgot_password'),
    path('reset_password/',resetPasswordView, name='reset_password')

]