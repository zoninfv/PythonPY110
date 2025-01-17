#from django.shortcuts import render
#from models import DATABASE
# Create your views here.

from django.http import HttpResponseNotFound
from django.http import JsonResponse
from store.models import DATABASE
from logic.services import view_in_cart, add_to_cart, remove_from_cart

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



def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ

from logic.services import filtering_category

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
         else:
               return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                                      'indent': 4})

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
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})

def cart_view(request):
    if request.method == "GET":
        data = ... # TODO Вызвать ответственную за это действие функцию
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = ... # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = ... # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})