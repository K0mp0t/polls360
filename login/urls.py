from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('signup/', SingUpView.as_view(template_name='login/sign_up.html'), name='signup'),
    path(r'profile/', profile, name='profile'),
    path(r'profile/edit', edit_profile, name='edit_profile'),
    path(r'logout/', include('django.contrib.auth.urls'), name='logout'),
    path(r'login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path(r'teams/', teams, name='teams'),
    path(r'team/<int:team_id>/', team_info, name='team_info'),
    path(r'team/leave/', leave_team, name='leave_team'),
    path(r'team/<int:team_id>/join/', join_team, name='join_team'),
    path(r'teams/create/', create_team, name='create_team'),
    path(r'team/<int:team_id>/delete/', delete_team, name='delete_team'),
    path(r'team/<int:team_id>/edit/', edit_team, name='edit_team'),
]