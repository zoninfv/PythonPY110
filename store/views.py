#from django.shortcuts import render
#from models import DATABASE
# Create your views here.

from django.http import HttpResponseNotFound
from django.http import JsonResponse
from .models import DATABASE
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