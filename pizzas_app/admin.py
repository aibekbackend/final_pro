from django.contrib import admin
from .models import Pizza, OrderPizza


admin.site.register(OrderPizza)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price" ]
