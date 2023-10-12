from rest_framework import generics, viewsets
from rest_framework import generics, serializers
from django.db.models import Func
from rest_framework.decorators import action
from rest_framework import response, status, mixins, viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Avg
from .models import Pizza, Review, Order, OrderPizza, PizzaSize
from .serializers import (PizzaSerializers, ReviewSerializers, OrderSerializers, OrderPizzaSerializers)


class Round(Func):
  function = 'ROUND'
  arity = 2

class PizzaViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializers
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        try:
            pizza = Pizza.objects.get(pk=pk)
            serializer = PizzaSerializers(pizza)
            return response.Response(serializer.data)
        except Pizza.DoesNotExist:
            return response.Response({'error': 'Pizza not found'}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['POST', 'PUT', 'GET', 'DELETE'], detail=True, url_path='main-review')
    def review(self, request, pk=None):
        pizza = self.get_object()
        if request.method == 'GET':
            reviews = pizza.reviews.all()
            serializer = ReviewSerializers(reviews, many=True)
            return response.Response(serializer.data, 200)

        elif request.method == 'POST':
            serializer = ReviewSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(pizza=pizza, user=self.request.user)
                return response.Response(serializer.data, 201)
            return response.Response(serializer.errors, 400)

        elif request.method == 'DELETE':
            print(self.kwargs)
            pizza = get_object_or_404(Pizza, pk=self.kwargs['pk'])
            user = request.user
            review = Review.objects.filter(pizza_id=pizza, user=user).first()
            if review:
                review.delete()
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return response.Response(status=status.HTTP_404_NOT_FOUND)

        elif request.method == ['PUT', 'PATCH']:
            pizza = get_object_or_404(Pizza, pk=pk)
            if request.method == 'PATCH':
                serializer = ReviewSerializers(pizza=pizza, data=request.data, partial=True)
            else:
                serializer = ReviewSerializers(pizza=pizza, data=request.data)
            if serializer.is_valid():
                serializer.save()

    @action(detail=True, url_name='avg-rating', methods=['GET'])
    def avg_rating(self, request, pk=None):
        pizza = self.get_object()
        avg_rating = pizza.reviews.aggregate(Avg('rating'))['rating__avg']
        return response.Response({'avg_rating': avg_rating})


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [AllowAny]


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        order = Order.objects.create(customer=request.user, total_cost=0)
        serializer = OrderPizzaSerializers(
            data=request.data,
            many=True,
            context={
                'order_id': order.id,
            }
        )
        serializer.is_valid(raise_exception=True)
        order_pizza_list = []
        total_cost = 0
        for order_pizza_data in request.data:
            pizza_id = order_pizza_data['pizza_id']
            amount = order_pizza_data['amount']
            pizza_size_id = order_pizza_data.get('pizza_size', None)
            pizza = Pizza.objects.get(id=pizza_id)
            pizza_size = PizzaSize.objects.get(id=pizza_size_id) if pizza_size_id else None
            price = pizza_size.price if pizza_size else pizza.price
            obj = OrderPizza(pizza_id_id=pizza.id, order_id_id=order.id, amount=amount, pizza_size=pizza_size)
            order_pizza_list.append(obj)
            total_cost += price * amount

        OrderPizza.objects.bulk_create(objs=order_pizza_list)
        order.total_cost = total_cost
        order.save(update_fields=['total_cost'])
        return response.Response(serializer.data, 201)




