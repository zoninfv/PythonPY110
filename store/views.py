#from django.shortcuts import render
#from models import DATABASE
# Create your views here.

from django.http import HttpResponseNotFound
from django.http import JsonResponse
from .models import DATABASE
def products_view(request):
    if request.method == "GET":
        if request.GET.get('id'):
            ID = request.GET['id']
            if ID in DATABASE:
                return JsonResponse(DATABASE[ID],json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            else:
                return HttpResponseNotFound("Данного продукта нет в базе данных")
        else:
            return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})






from django.http import HttpResponse, HttpResponseNotFound

def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ