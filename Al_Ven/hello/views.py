from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import time
from .models import Person, Category, Products

# def index(request):
#     host = request.META["HTTP_HOST"] # получаем адрес сервера
#     user_agent = request.META["HTTP_USER_AGENT"]    # получаем данные бразера
#     path = request.path     # получаем запрошенный путь

#     return HttpResponse(f"""
#         <h2>Hello</h2>
#         <p>Host: {host}</p>
#         <p>Path: {path}</p>
#         <p>User-agent: {user_agent}</p>
#         <img src="https://avatars.mds.yandex.net/i?id=6d3e505aa14911c3f6f7b1184358c6f8dc18168a-4055226-images-thumbs&n=13">
#     """)

def index(request):
    return render(request, "index.html")

def products(request):
    categories = Category.objects.all()
    products = Products.objects.select_related('cat_id').all()

    return render(request, 'products.html', {
        'category': categories,
        'product': products,
    })


def blog(request):
    return render(request, "blog.html")

def weo(request):
    return render(request, "weo.html")



def news(request):
    name = request.GET.get("", "").strip()
    people = Person.objects.all()

    if name:
        people = people.filter(name__icontains=name)

    people = people.values_list("id", "name", "fam", "oth", "age")

    return render(request, "news.html", {"people": people})



def reg(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        password = request.POST.get("pass", "")
        pass_confirm = request.POST.get("pass_confirm", "")
        email = request.POST.get("email", "")

        if not name or not password or not email:
            messages.error(request, "Все поля должны быть заполнены!")
            return redirect("reg")

        if password != pass_confirm:
            messages.error(request, "Пароли не совпадают!")
            return redirect("reg")
        
        if password == pass_confirm:
            messages.success(request, f"Регистрация успешна! Имя: {name}, Email: {email}")
            return redirect("vhod")
    else:
        return render(request, "reg.html")
    
def vhod(request):
    return render(request, "vhod.html")

