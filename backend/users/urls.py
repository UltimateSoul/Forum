from django.urls import path
from rest_framework.authtoken import views

from users.views import RegistrationView, EmailConfirmationHandleView

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate-account/<str:uidb64>/<str:token>/', EmailConfirmationHandleView.as_view(), name='confirm-email'),
]
