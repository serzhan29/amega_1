from django.urls import path, include
from rest_framework import routers

from carts import views

app_name = 'carts'
router = routers.DefaultRouter()
router.register(r'carts', views.MobileCartsApi)


urlpatterns = [
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart_change/', views.cart_change, name='cart_change'),
    path('cart_remove/', views.cart_remove, name='cart_remove'),
    path('api/', include(router.urls)),
]