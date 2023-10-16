from django.urls import path, include
from .views import (ClientLoginviewSet, СlientSignupViewSet, SendToRecoverPassword,
                    UserProfileAPIView, UpdatePasswordView, Change_photo, VerificationCodeAPIView)

urlpatterns = [
    path('signup/', СlientSignupViewSet.as_view(), name='signup'),
    path('login/', ClientLoginviewSet.as_view(), name='login'),
    path('verify/', VerificationCodeAPIView.as_view(), name='verify_email'),
    path('send_code/', SendToRecoverPassword.as_view(), name='send_code'),
    path('profil/<str:username>/', UserProfileAPIView.as_view(), name='profil'),
    path('update_pass/', UpdatePasswordView.as_view(), name='update_pass'),
    path('photo/<str:username>/', Change_photo.as_view(), name='update_pass'),
]