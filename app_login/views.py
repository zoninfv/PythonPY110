from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from logic.services import add_user_to_cart

def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data["username"], password=data["password"])
        if user:
            login(request, user)
            add_user_to_cart(request,user.username)
            return redirect("/")
        return render(request, "login/login.html", context={"error": "Неверные данные"})

from django.contrib.auth import logout

def logout_view(request):
    if request.method == "GET":
        logout(request)  # Функция разлогинивает пользователя
        return redirect("/") # TODO Верните редирект на главную страницу