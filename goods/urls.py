from django.urls import path, include
from rest_framework import routers

from goods import views

app_name = 'goods'
router = routers.DefaultRouter()
router.register(r'cat', views.MobileCategoryApi)
router.register(r'products', views.ProductsCategoryApi)

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),

    path('categories/', views.categories, name='categories'),
    path('categories/<slug:category_slug>/', views.subcategories, name='subcategories'),

    path('main/categories-main/', views.categories_list, name='categories-main'),  # Updated view function name
    path('main/categories-main/<slug:category_slug>/', views.subcategories_list, name='subcategories-main'),
    path('main/categories-main/<slug:category_slug>/<slug:subcategory_slug>/', views.products_by_subcategory, name='products_by_subcategory'),

    # Updated view function name

    path('api/', include(router.urls)),
]




