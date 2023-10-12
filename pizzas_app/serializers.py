from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pizza, Ingredient, Order, Review, OrderPizza, PizzaSize
from django.db import transaction


class PizzaSizeSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    percent_increase = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = PizzaSize
        fields = ['size', 'price', 'percent_increase']

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


