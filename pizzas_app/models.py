from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Size(models.Model):
    size_small = "25"
    size_average = "35"
    size_large = "45"
    size_list = (
        (size_small, "25"),
        (size_average, "35cm"),
        (size_large, "45cm"),
    )
    title = models.TextField(choices=size_list, default=size_small)

    def __str__(self):
        return self.title


class Pizza(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True)
    pizza_size = models.ManyToManyField(Size, through='PizzaSize')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, through='OrderPizza')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer} at {self.timestamp}"


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Review(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                     MaxValueValidator(5)])
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.pizza}"

class PizzaSize(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='pizza_sizes')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def price_for_size(self):
        if self.size:
            if self.size.title == "25":
                return self.price
            elif self.size.title == "35cm":
                return self.price * 1.4  # Увеличиваем цену на 40%
            elif self.size.title == "45cm":
                return self.price * 1.6  # Увеличиваем цену на 60%
        return self.price

class OrderPizza(models.Model):
    pizza_id = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    pizza_size = models.ForeignKey(PizzaSize, on_delete=models.SET_NULL, null=True)



