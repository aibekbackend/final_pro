from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from .models import Register


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Register
        fields = [
        'id', 'username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender',
        'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError("Error password.")

        return data

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)
        user = Register.objects.create(**validated_data)
        hashed_passw = make_password(user.password)
        user.password = hashed_passw
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)


class UsersProfileSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    role = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)


class PhotoChangeSerializer(serializers.Serializer):
    photo = serializers.ImageField()


class SendCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6, min_length=6, required=True)


