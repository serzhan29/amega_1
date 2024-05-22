from django.core import paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from goods.models import Categories, Products


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    products = Products.objects.all()
    paginator = Paginator(products, 9)
    page = request.GET.get('page', 1)

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        'title': 'Home - Главная',
        'content': "Магазин A-mega",
        'goods_2': current_page,
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Home - О нас',
        'content': "О нас",
        'text_on_page': "Текст о том почему этот магазин такой классный, и какой хороший товар."
    }

    return render(request, 'main/about.html', context)


def contact(request):
    return render(request, "main/contact.html")
