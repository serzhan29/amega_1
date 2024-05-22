"""" Корзина """
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from rest_framework import viewsets


from goods.models import Products
from carts.serializers import CartSerializer

# Функция cart_add обрабатывает запрос на добавление продукта в корзину.
def cart_add(request):
    # Получаем идентификатор продукта из POST-запроса.
    product_id = request.POST.get("product_id")
    # Получаем объект продукта по его идентификатору.
    product = Products.objects.get(id=product_id)
    # Проверяем, авторизован ли пользователь.
    if request.user.is_authenticated:
        # Если пользователь авторизован, ищем корзины, которые содержат данный продукт для данного пользователя.
        carts = Cart.objects.filter(user=request.user, product=product)
        # Если корзина уже существует, увеличиваем количество продукта в корзине.
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            # Если корзина не существует, создаем новую корзину с продуктом и устанавливаем количество в 1.
            Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        # Если пользователь не авторизован, ищем корзины по сессионному ключу.
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)

        # Если корзина уже существует, увеличиваем количество продукта в корзине.
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            # Если корзина не существует, создаем новую корзину с продуктом и устанавливаем количество в 1.
            Cart.objects.create(
                session_key=request.session.session_key, product=product, quantity=1)

    # Получаем информацию о корзинах пользователя после обновления.
    user_cart = get_user_carts(request)

    # Создаем HTML-код для отображения корзин в пользовательском интерфейсе.
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)
    # Формируем данные для отправки JSON-ответа.
    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }
    # Возвращаем JSON-ответ.
    return JsonResponse(response_data)


# Функция cart_change обрабатывает запрос на изменение количества продукта в корзине.
def cart_change(request):
    # Получаем идентификатор корзины и новое количество из POST-запроса.
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    # Получаем объект корзины по ее идентификатору.
    cart = Cart.objects.get(id=cart_id)

    # Обновляем количество продукта в корзине.
    cart.quantity = quantity
    cart.save()

    # Получаем обновленное количество продукта в корзине.
    updated_quantity = cart.quantity

    # Получаем информацию о корзинах пользователя после обновления.
    user_cart = get_user_carts(request)

    # Создаем HTML-код для отображения корзин в пользовательском интерфейсе.
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)
    # Формируем данные для отправки JSON-ответа.
    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,  # Замечание: опечатка в ключе "quaantity"
    }
    # Возвращаем JSON-ответ.
    return JsonResponse(response_data)


# Функция cart_remove обрабатывает запрос на удаление продукта из корзины.
def cart_remove(request):
    # Получаем идентификатор корзины из POST-запроса.
    cart_id = request.POST.get("cart_id")
    # Получаем объект корзины по ее идентификатору и сохраняем количество продукта.
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    # Удаляем корзину из базы данных.
    cart.delete()
    # Получаем информацию о корзинах пользователя после удаления.
    user_cart = get_user_carts(request)
    # Создаем HTML-код для отображения корзин в пользовательском интерфейсе.
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)
    # Формируем данные для отправки JSON-ответа.
    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }
    return JsonResponse(response_data)

#====================mobile-api==============================


class MobileCartsApi(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer