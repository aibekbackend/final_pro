from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pizza, Ingredient, Order, Review, OrderPizza, PizzaSize, Size
from django.db import transaction

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['title']


class PizzaSizeSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    def __init__(self, *args, **kwargs):
        self.pizza = kwargs.pop('pizza', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = PizzaSize
        fields = ['size', 'price']



class PizzaSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    pizza_sizes = PizzaSizeSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        fields = ['id', 'name', 'description', 'price', 'image', 'pizza_sizes']



class IngredientSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'cost']


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'pizzas', 'total_cost', 'timestamp']


class OrderPizzaSerializers(serializers.Serializer):
    pizza_id = serializers.PrimaryKeyRelatedField(queryset=Pizza.objects.all())
    amount = serializers.IntegerField(min_value=1)


class ReviewSerializers(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    pizza = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'pizza', 'user', 'rating', 'comment', 'timestamp', 'avg_rating']


