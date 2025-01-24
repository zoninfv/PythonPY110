#from django.shortcuts import render
#from models import DATABASE
# Create your views here.

from django.http import HttpResponseNotFound
from django.http import JsonResponse
from store.models import DATABASE
from logic.services import filtering_category
from logic.services import add_to_cart,view_in_cart,remove_from_cart
from django.shortcuts import redirect

def products_view(request):
    if request.method == "GET":
        ID = request.GET.get('id')
        if ID:
            if ID in DATABASE:
                return JsonResponse(DATABASE[ID],json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            else:
                return HttpResponseNotFound("Данного продукта нет в базе данных")
        else:
            return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})

def product_page_view(request,page):
        if request.method == "GET":
            if isinstance(page, str):
                for data in DATABASE.values():
                    if data['html'] == page:
                        with open(f'store/products/{page}.html', encoding="utf-8") as f1:
                            data1 = f1.read()
                        return HttpResponse(data1)
            elif isinstance(page, int):
                data = DATABASE.get(str(page))
                if data:
                    with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f2:
                        data2=f2.read()
                    return HttpResponse(data2)
            return HttpResponse(status=404)
from django.http import HttpResponse, HttpResponseNotFound



from django.shortcuts import render

def shop_view(request):
    if request.method == "GET":
        return render(request,
                      'store/shop.html',
                      context={"products": DATABASE.values()})



def products_view(request):
    if request.method == "GET":
        # Обработка id из параметров запроса (уже было реализовано ранее)
        if request.method == "GET":
         ID = request.GET.get('id')
         if ID:
            if ID in DATABASE:
                return JsonResponse(DATABASE[ID],json_dumps_params={'ensure_ascii': False,
                                                                      'indent': 4})
            else:
                 return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        data = None
        if ordering_key := request.GET.get("ordering"): # Если в параметрах есть 'ordering'
            if request.GET.get("reverse") and request.GET.get("reverse").lower() == 'true': # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE,category_key,ordering_key,reverse=True) #  TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=True
            else:  # Если не обнаружили в адресно строке ...&reverse=true , значит reverse=False
                data = filtering_category(DATABASE,category_key,ordering_key,reverse=False) #  TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=False
        else:
            data = filtering_category(DATABASE,category_key) #  TODO Использовать filtering_category и провести фильтрацию с параметрами category
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4},safe=False)
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})

def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            product['quantity'] = quantity # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product[
                "price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            products.append(product)# 3. добавьте product в список products

        return render(request, "store/cart.html", context={"products": products})

def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        if name_coupon in DATA_COUPON.keys():
            return JsonResponse(
                {"discount": DATA_COUPON[name_coupon]["value"], "is_valid": DATA_COUPON[name_coupon]["is_valid"]},
                json_dumps_params={'ensure_ascii': False})
        else:
            return HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 80},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country in DATA_PRICE.keys() and city in DATA_PRICE.values():
            return JsonResponse(
                {"price": DATA_PRICE[country][city]},
                json_dumps_params={'ensure_ascii': False})
        elif country in DATA_PRICE.keys() and city not in DATA_PRICE.values():
            return JsonResponse({"price": DATA_PRICE[country]["fix_price"]},
                                json_dumps_params={'ensure_ascii': False})
    else:
        return HttpResponseNotFound("Неверные данные")

def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("store:cart_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")