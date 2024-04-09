from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'signup/',
        views.SignUpView.as_view(),
        name='signup'
    ),
    path(
        'confirm-email/',
        views.ConfirmEmailView.as_view(),
        name='confirm-email'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'badges/',
        views.UserBadgesView.as_view(),
        name='badges'    
    ),
    path(
        'notifications/',
        views.UserNotificationsView.as_view(),
        name='notifications'    
    ),
    path(
        'notifications/<int:id>/read/',
        views.ReadNotificationView.as_view(),
        name='read-notifications'    
    ),
]