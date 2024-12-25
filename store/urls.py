# urls.py in store

from django.urls import path
from .views import products_view, shop_view, product_page_view
from logic.services import filtering_category

urlpatterns = [
    path('product/', products_view),
    path('', shop_view),
    path('product/<slug:page>.html', product_page_view ),
    path('product/<int:page>', product_page_view),

]