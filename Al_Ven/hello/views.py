from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# ИМПОРТ МОДЕЛЕЙ (добавлен Review)
from .models import Person, Category, Products, Review

# ИМПОРТ ФОРМ (все в одной строке, без дублирования)
from .forms import UserForm, ReviewForm, EmailAuthenticationForm
from .authentication import username_for_email


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

    category_id = request.GET.get('category_id')
    selected_category = None

    if category_id:
        products = products.filter(cat_id_id=category_id)
        selected_category = Category.objects.filter(id=category_id).first()

    return render(request, 'products.html', {
        'category': categories,
        'product': products,
        'selected_category': selected_category,
    })

def blog(request):
    return render(request, "blog.html")

def weo(request):
    return render(request, "weo.html")

def news(request):
    name = request.GET.get("name", "").strip()
    people = Person.objects.all()

    if name:
        people = people.filter(name__icontains=name)

    people = people.values_list("id", "name", "fam", "oth", "age")

    return render(request, "news.html", {"people": people})

def reg(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_model = get_user_model()
            email = form.cleaned_data["email"]
            user = user_model.objects.create_user(
                username=username_for_email(email),
                email=email,
                first_name=form.cleaned_data["name"],
                password=form.cleaned_data["password"],
            )
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("index")
    else:
        form = UserForm()

    return render(request, "reg.html", {"form": form})

def vhod(request):
    if request.user.is_authenticated:
        return redirect("index")
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Вы вошли в аккаунт.")
        return redirect("index")
    return render(request, "vhod.html", {"form": form})


@login_required
def vyhod(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Вы вышли из аккаунта.")
    return redirect("index")
    
def reviews_page(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо! Ваш отзыв успешно добавлен.')
            return redirect('reviews') # Перенаправляем, чтобы избежать повторной отправки
    else:
        form = ReviewForm()

    # Получаем все отзывы, отсортированные по дате (новые первые)
    reviews_list = Review.objects.all()

    context = {
        'form': form,
        'reviews_list': reviews_list
    }
    return render(request, 'reviews.html', context)
