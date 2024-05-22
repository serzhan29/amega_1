from carts.models import Cart  # Импорт модели Cart из приложения carts


def get_user_carts(request):
    # Проверяем, аутентифицирован ли пользователь
    if request.user.is_authenticated:
        # Если пользователь аутентифицирован, возвращаем корзины, связанные с этим пользователем,
        # с учетом связанных объектов продуктов (product)
        return Cart.objects.filter(user=request.user).select_related('product')

    # Если пользователь не аутентифицирован, но у него есть сессия
    if not request.session.session_key:
        # Если сессия отсутствует, создаем новую сессию
        request.session.create()
    # Возвращаем корзины, связанные с сессией пользователя, с учетом связанных объектов продуктов (product)
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')
