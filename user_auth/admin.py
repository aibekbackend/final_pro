from django.contrib import admin
from django.contrib.auth.models import User



@admin.register(User)
class EmployeesUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'password', 'is_staff']


