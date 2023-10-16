import random, smtplib, base64
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status, exceptions, generics, response
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser
from .serializers import (RegisterSerializer, LoginSerializer, RecoverPasswordSerializer,
                          UsersProfileSerializer, UpdatePasswordSerializer, PhotoChangeSerializer, SendCodeSerializer)
from .models import Register

def authenticate_user(username, password):
    try:
        my_user = Register.objects.get(username=username)
        if check_password(password, my_user.password):
            return my_user
    except Register.DoesNotExist:
        return None

class СlientSignupViewSet(generics.CreateAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ClientLoginviewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate_user(username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed()
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return response.Response(data={"token": token.key},
                                 status=status.HTTP_200_OK)

class VerificationCodeAPIView(APIView):
    @extend_schema(
        description="code verify",
        request=SendCodeSerializer,
        responses={200: {"message": "mail successfully verified."}}
    )
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data['verification_code']
            user = Register.objects.filter(email_token=verification_code).first()
            if user:
                my_data = user.date_of_join
                current_time = timezone.now()
                time_difference = current_time - my_data
                time_difference_in_minutes = time_difference.total_seconds() / 60
                if time_difference_in_minutes > 2:
                    user.delete()
                    return response.Response({'message': "bay"})
                user.is_email = True
                user.save()
                return response.Response({'message': 'Verification code is valid.'}, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToRecoverPassword(APIView):
    @extend_schema(
        description=" send Recover_token Password",
        request=RecoverPasswordSerializer,
        responses={200: {"message": "code successfully sended."}}
    )
    def post(self, request):
        serializer = RecoverPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']

            verification_code = ''.join([str(random.randint(0, 9)) for i in range(6)])
            user = Register.objects.get(username=username)
            user.recover_token = verification_code
            user.save()


            subject = 'Восстановление пароля'
            message = f'Здравствуйте, {username}!\n\nВаш код для восстановле пароля: {verification_code}'
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]

            try:

                send_mail(subject, message, from_email, to_email)
                return response.Response({'message': 'Код отправлен на указанный адрес.'}, status=status.HTTP_200_OK)
            except smtplib.SMTPException:
                return response.Response({'message': 'Произошла ошибка при отправке письма.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return response.Response({'message': 'Неверные данные.'}, status=status.HTTP_400_BAD_REQUEST)





class UserProfileAPIView(APIView):
    parser_classes = [MultiPartParser]
    def get(self, request, username):
        user_profile = get_object_or_404(Register, username=username)
        if user_profile.photo:
            with open(user_profile.photo.path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        else:
            encoded_image = None

        profile_data = {
            'username': user_profile.username,
            'last_name': user_profile.last_name,
            'first_name': user_profile.first_name,
            'email': user_profile.email,
            'photo': encoded_image,
            'phone_number': str(user_profile.phone_number),
            'gender': user_profile.gender,
            'date_of_birth': user_profile.date_of_birth,
            'country': user_profile.country
        }
        return response.Response(profile_data)


class UserUpdateAPIVIEW(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        description="user's profile",
        request=UsersProfileSerializer,
        responses={200: {"message": "user successfully got."}}
    )
    def put(self, request, username, role):
        data = request.data
        serializer = UsersProfileSerializer(data=data)
        if serializer.is_valid():
            user_profile = get_object_or_404(Register, username=username)
            last_name = serializer.validated_data['last_name']
            first_name = serializer.validated_data['first_name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            country = serializer.validated_data['country']

            user_profile.last_name = last_name
            user_profile.first_name = first_name
            user_profile.email = email
            user_profile.phone_number = phone_number
            user_profile.country = country
            user_profile.save()
            return response.Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            return response.Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)



class UpdatePasswordView(APIView):
    @extend_schema(
        description="New Password",
        request=UpdatePasswordSerializer,
        responses={200: {"message": "password successfully changed."}}
        )
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            username = serializer.validated_data['username']
            user = Register.objects.get(username=username)


            if password == confirm_password:
                user.password = make_password(password)
                user.save()
                return response.Response({'message': ' PASSWORD UPDATED.'}, status=status.HTTP_200_OK)
            else:
                return response.Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Change_photo(APIView):
    parser_classes = [MultiPartParser]
    @extend_schema(
        description="user's photo",
        request=PhotoChangeSerializer,
        responses={200: {"message": "user successfully got."}}
    )
    def put(self, request, username):
        serializer = PhotoChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(Register, username=username)
            photo = serializer.validated_data['photo']
            user.photo = photo
            user.save()
            return response.Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)