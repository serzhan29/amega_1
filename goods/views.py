from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import viewsets
from django.contrib.postgres.search import TrigramSimilarity

from goods.models import Products, Categories, SubCategories
from goods.utils import q_search
from goods.serializers import CategoriesSerializer, ProductsSerializer



def q_search(query):
    query = query.lower()
    return Products.objects.filter(Q(name__icontains=query))


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 6)
    current_page = paginator.page(int(page))

    context = {
        "title": "Главная страница - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    context = {"product": product}
    return render(request, "goods/product.html", context=context)


def categories(request):
    # Получаем все категории и их подкатегории
    categories = Categories.objects.all()
    subcategories = SubCategories.objects.all()
    return render(request, 'goods/category.html', {
        'categories': categories,
        'subcategories': subcategories,
    })


def subcategories(request, category_slug):
    # Получаем категорию по slug
    category = get_object_or_404(Categories, slug=category_slug)
    subcategories = SubCategories.objects.filter(category=category)
    return render(request, 'goods/subcategory.html', {'category': category, 'subcategories': subcategories})


def products(request, category_slug, subcategory_slug=None):
    # Получаем категорию по slug
    category = get_object_or_404(Categories, slug=category_slug)
    if subcategory_slug:
        # Если указана подкатегория, получаем ее
        subcategory = get_object_or_404(SubCategories, slug=subcategory_slug)
        # Получаем товары для указанной подкатегории
        products = Products.objects.filter(category=category, sub_category=subcategory)
    else:
        # Если не указана подкатегория, получаем все товары для категории
        products = Products.objects.filter(category=category)
        subcategory = None
    return render(request, 'goods/product-2.html', {'category': category, 'subcategory': subcategory, 'products': products})


def products_by_subcategory(request, category_slug, subcategory_slug):
    # Получаем подкатегорию
    subcategory = SubCategories.objects.get(slug=subcategory_slug)

    # Получаем все товары для данной подкатегории, отсортированные по главной категории, а затем по подкатегории
    products = Products.objects.filter(category__slug=category_slug, sub_category__slug=subcategory_slug)

    context = {
        'subcategory': subcategory,
        'products': products
    }
    return render(request, 'goods/sub-products.html', context)

#======================categories============================

def categories_list(request):
    categories = Categories.objects.all()
    return render(request, 'goods/main-categories.html', {'categories': categories})


def subcategories_list(request, category_slug):
    category = Categories.objects.get(slug=category_slug)
    subcategories = SubCategories.objects.filter(category=category)
    products = Products.objects.filter(category=category)
    if subcategories:
        return render(request, 'goods/main-subcategories.html', {'category': category, 'subcategories': subcategories})
    else:
        # здесь предполагается логика вывода продуктов, связанных с основной категорией
        return render(request, 'goods/main-products.html', {
                                        'category': category,
                                        'products': products,

                                                            })

#====================mobile-api==============================


class MobileCategoryApi(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class ProductsCategoryApi(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer