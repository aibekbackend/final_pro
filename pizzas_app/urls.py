from django.urls import path, include
from rest_framework_nested import routers
from .views import PizzaViewSet, OrderListCreateAPIView

router = routers.DefaultRouter()
router.register(r'pizzas', PizzaViewSet)

order_router = routers.NestedDefaultRouter(router, r'pizzas', lookup='pizza')
order_router.register(r'orders', OrderListCreateAPIView, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(order_router.urls)),
]