from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
import home.views as vu
urlpatterns = [
    path("register/", views.signup_view, name="register"),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view,name="logout"),
    path('profile/<str:pk>', views.profile_view, name='profile'),
    path('edit-profile', views.edit_profile_view, name='edit-profile'),
    ]