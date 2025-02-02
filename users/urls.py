from django.urls import path, include
from rest_framework import routers

from users import views

app_name = 'users'
router = routers.DefaultRouter()
router.register(r'user', views.UserApi)

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),
    path('api/', include(router.urls)),
]