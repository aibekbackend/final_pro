# Generated by Django 4.2.5 on 2023-10-13 09:37

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Женщина')], max_length=50)),
                ('photo', models.ImageField(blank=True, default='profile/avatarka.jpg', null=True, upload_to='profile')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_join', models.DateTimeField(auto_now_add=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('email_token', models.IntegerField(blank=True, null=True)),
                ('recover_token', models.IntegerField(blank=True, null=True)),
                ('is_email', models.BooleanField(default=False)),
            ],
        ),
    ]
