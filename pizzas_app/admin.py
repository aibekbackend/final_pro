from django.contrib import admin
from .models import Pizza, OrderPizza, PizzaSize, Size


admin.site.register(OrderPizza)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price" ]

admin.site.register(PizzaSize)
admin.site.register(Size)