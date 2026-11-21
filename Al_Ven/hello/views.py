from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

# ИМПОРТ МОДЕЛЕЙ (добавлен Review)
from .models import Person, Category, Products, Review

# ИМПОРТ ФОРМ (все в одной строке, без дублирования)
from .forms import (
    UserForm,
    ReviewForm,
    EmailAuthenticationForm,
    AccountNameForm,
    AccountUsernameForm,
    AccountPasswordForm,
    ProductInquiryForm,
)
from .models import ProductInquiry
from .authentication import username_for_email


def index(request):
    # NOTE: На главной показываем короткую витрину, чтобы пользователь сразу
    # видел товары, категории и отзывы, а не только приветственный текст.
    featured_categories = Category.objects.order_by('name')[:6]
    latest_reviews = Review.objects.all()[:3]
    # NOTE: Панель остатков: 4 случайных товара в наличии, при каждом заходе разные.
    # Ширина полосы ограничена 100 (шкала до 100 шт.).
    stock_products = list(Products.objects.filter(conter__gt=0).order_by('?')[:4])
    for product in stock_products:
        product.bar = min(product.conter, 100)
    return render(request, "index.html", {
        'featured_categories': featured_categories,
        'latest_reviews': latest_reviews,
        'stock_products': stock_products,
    })


def robots_txt(request):
    # NOTE: В production замените домен на фактический адрес сайта.
    return HttpResponse(
        'User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: /sitemap.xml\n',
        content_type='text/plain',
    )


def sitemap_xml(request):
    # NOTE: Статические URL плюс детальные страницы товаров (/products/<slug>/).
    products = Products.objects.all().order_by('-date_prod')
    urls = [
        '/',
        '/products/',
        '/news/',
        '/reviews/',
        '/blog/',
        '/weo/',
    ] + [f'/products/{p.slug}/' for p in products]
    entries = ''.join(f'<url><loc>{u}</loc></url>' for u in urls)
    return HttpResponse(
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>',
        content_type='application/xml',
    )

def product_inquiry_form(request, slug):
    """Страница заявки на товар — B2B: отправка заявки на почту админов."""
    product = get_object_or_404(Products, slug=slug)
    if request.method == 'POST':
        form = ProductInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.save()
            admins_emails = [a[1] for a in settings.ADMINS if a[1]]
            if admins_emails:
                subject = f'Заявка на товар: {product.name}'
                body = (
                    f'Товар: {product.name}\n'
                    f'Ссылка: {request.build_absolute_uri()}\n\n'
                    f'Заявитель: {form.cleaned_data["name"]} — {form.cleaned_data["email"]}\n\n'
                    f'Сообщение:\n{form.cleaned_data["message"]}\n\n'
                    f'Заявка #{inquiry.pk}'
                )
                send_mail(subject, body, settings.SITE_EMAIL, admins_emails)
            messages.success(request, f'Заявка на «{product.name}» отправлена.')
            return redirect('product_detail', slug=slug)
    else:
        form = ProductInquiryForm()
    return render(request, 'product_inquiry.html', {'product': product, 'form': form})


def product_detail(request, slug):
    # NOTE: select_related для категории — один запрос к базе вместо двух.
    product = get_object_or_404(
        Products.objects.select_related('cat_id'),
        slug=slug,
    )
    # NOTE: Похожие товары из той же категории — для виртуальной витрины и SEO.
    related = (
        Products.objects.select_related('cat_id')
        .filter(cat_id=product.cat_id)
        .exclude(pk=product.pk)
        .order_by('-id')[:6]
    )
    return render(request, 'product_detail.html', {
        'product': product,
        'related': related,
    })


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
    name_form = AccountNameForm(initial={"name": request.user.first_name})
    username_form = AccountUsernameForm(
        request.user,
        initial={"username": request.user.username},
    )
    password_form = AccountPasswordForm(request.user)

    if request.method == "POST":
        if request.POST.get("action") == "name":
            name_form = AccountNameForm(request.POST)
            if name_form.is_valid():
                request.user.first_name = name_form.cleaned_data["name"].strip()
                request.user.save(update_fields=["first_name"])
                messages.success(request, "Имя аккаунта успешно изменено.")
                return redirect("account")
        elif request.POST.get("action") == "username":
            username_form = AccountUsernameForm(request.user, request.POST)
            if username_form.is_valid():
                request.user.username = username_form.cleaned_data["username"]
                request.user.save(update_fields=["username"])
                messages.success(request, "Логин успешно изменён.")
                return redirect("account")
        elif request.POST.get("action") == "password":
            password_form = AccountPasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Пароль успешно изменён.")
                return redirect("account")

    return render(request, "account.html", {
        "account_user": request.user,
        "name_form": name_form,
        "username_form": username_form,
        "password_form": password_form,
    })


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
