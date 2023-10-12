from django.urls import path, include
from rest_framework_nested import routers
from .views import PizzaViewSet, OrderListCreateAPIView
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register('pizza', PizzaViewSet, basename='pizza')


urlpatterns = [
    path('order/create', OrderListCreateAPIView.as_view(), name='order-create'),
    path('', include(router.urls)),
]
