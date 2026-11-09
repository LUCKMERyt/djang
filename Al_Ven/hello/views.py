from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

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
    # NOTE: На главной показываем короткую витрину, чтобы пользователь сразу
    # видел товары, категории и отзывы, а не только приветственный текст.
    featured_categories = Category.objects.order_by('name')[:6]
    latest_reviews = Review.objects.all()[:3]
    return render(request, "index.html", {
        'featured_categories': featured_categories,
        'latest_reviews': latest_reviews,
    })


def robots_txt(request):
    # NOTE: В production замените домен на фактический адрес сайта.
    return HttpResponse(
        'User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: /sitemap.xml\n',
        content_type='text/plain',
    )


def sitemap_xml(request):
    # TODO: Добавить динамические URL товаров после появления отдельных страниц товаров.
    return HttpResponse(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        '<url><loc>/</loc></url><url><loc>/products/</loc></url>'
        '<url><loc>/news/</loc></url><url><loc>/reviews/</loc></url>'
        '<url><loc>/blog/</loc></url><url><loc>/weo/</loc></url>'
        '</urlset>',
        content_type='application/xml',
    )

def products(request):
    # NOTE: select_related уменьшает количество запросов к таблице категорий.
    categories = Category.objects.all()
    products = Products.objects.select_related('cat_id').all()

    category_id = request.GET.get('category_id')
    query = request.GET.get('q', '').strip()
    material = request.GET.get('material', '').strip()
    sort = request.GET.get('sort', 'name')
    stock = request.GET.get('stock', '')
    selected_category = None

    if category_id:
        products = products.filter(cat_id_id=category_id)
        selected_category = Category.objects.filter(id=category_id).first()

    # ! Фильтры используют ORM и не собирают SQL из пользовательской строки.
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if material:
        products = products.filter(material__icontains=material)
    if stock == 'available':
        products = products.filter(conter__gt=0)
    if sort in {'name', 'sale', '-sale', 'date_prod', '-date_prod'}:
        products = products.order_by(sort)

    return render(request, 'products.html', {
        'category': categories,
        'product': products,
            'selected_category': selected_category,
            'query': query, 'material': material, 'sort': sort, 'stock': stock,
    })

def blog(request):
    return render(request, "blog.html")

def weo(request):
    return render(request, "weo.html")

def news(request):
    # NOTE: Страница персонала показывает всю команду карточками без фильтра.
    people = Person.objects.all()

    return render(request, "news.html", {"people": people})

def reg(request):
    # ! Пароль передаётся в create_user, поэтому Django сохраняет его хеш.
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
            return redirect("account")
    else:
        form = UserForm()

    return render(request, "reg.html", {"form": form})

def vhod(request):
    if request.user.is_authenticated:
        return redirect("account")
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Вы вошли в аккаунт.")
        return redirect("account")
    return render(request, "vhod.html", {"form": form})


@login_required(login_url="vhod")
def account(request):
    return render(request, "account.html", {"account_user": request.user})


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
