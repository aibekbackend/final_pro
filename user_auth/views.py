from django.shortcuts import render
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status, exceptions, generics, response
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token



class СlientSignupViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ClientLoginviewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])

        if not user:
            raise exceptions.AuthenticationFailed()
        user.last_login = timezone.now()
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        # if created:
        #     token_key = token.key
        # else:
        #     token_key = token.key

        return response.Response(data={"token": token.key},
                                 status=status.HTTP_200_OK)







