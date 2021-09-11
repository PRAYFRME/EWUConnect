from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
import users.views as vu
import posts.views as postView

urlpatterns = [
    path('', postView.post_home_view, name='home'),

    # user logout
    path('logout', vu.logout_view, name='logout'),

    path('accounts/profile/<str:pk>', vu.profile_view, name='profile'),
    path('accounts/edit-profile', vu.edit_profile_view, name='edit-profile'),

    # utilities
    path('account-settings', vu.account_settings_view, name='settings'),
    path('about', vu.about_view, name='about'),
    path('contact', vu.contact_view, name='contact'),
]