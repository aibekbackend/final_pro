from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Register(models.Model):
    GENDER = [
        ('Мужчина', 'Мужчина'),
        ('Женщина', 'Женщина')
    ]
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    photo = models.ImageField(upload_to='profile', default='profile/avatarka.jpg', null=True, blank=True)
    phone_number = PhoneNumberField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_join = models.DateTimeField(auto_now_add=True)
    country = models.CharField(null=True, blank=True, max_length=255)
    email_token = models.IntegerField(null=True, blank=True)
    recover_token = models.IntegerField(null=True, blank=True)
    is_email = models.BooleanField(default=False)
    def __str__(self):
        return self.username

