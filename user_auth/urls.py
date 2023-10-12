from django.urls import path, include
from .views import ClientLoginviewSet, СlientSignupViewSet

urlpatterns = [
    path('signup/', СlientSignupViewSet.as_view(), name='signup'),
    path('login/', ClientLoginviewSet.as_view(), name='login'),

]