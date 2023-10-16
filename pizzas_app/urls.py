from django.urls import path, include
from rest_framework_nested import routers
from .views import PizzaViewSet, OrderListCreateAPIView

# Создайте экземпляр DefaultRouter
router = routers.DefaultRouter()
# Зарегистрируйте ваше представление PizzaViewSet
router.register(r'pizzas', PizzaViewSet)

# Определите вложенные маршруты для OrderListCreateAPIView
order_router = routers.NestedDefaultRouter(router, r'pizzas', lookup='pizza')
order_router.register(r'orders', OrderListCreateAPIView, basename='order')

# Теперь добавьте маршруты из router и order_router к вашим общим маршрутам
urlpatterns = [
    # ... другие маршруты ...
    path('api/', include(router.urls)),
    path('api/', include(order_router.urls)),
]