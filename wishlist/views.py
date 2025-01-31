from django.shortcuts import render

def wishlist_view(request):
        if request.method == "GET":
        #         return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
        #                                                      'indent': 4})
        # products = []  # Список продуктов
        # for product_id in data['products']:
        #     products.append(DATABASE[str(product_id)])
            return render(request, 'wishlist/wishlist.html')
