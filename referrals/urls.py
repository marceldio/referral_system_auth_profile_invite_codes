from django.urls import path
from . import views

urlpatterns = [
    path('auth/send-code/', views.SendAuthCodeView.as_view(), name='send-auth-code'),
    path('auth/verify-code/', views.VerifyAuthCodeView.as_view(), name='verify-auth-code'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/invite/', views.ActivateInviteCodeView.as_view(), name='activate-invite'),
]
