from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.html import format_html
from .models import Person, Category, Products, Review


class EmptyAdminAuthenticationForm(AuthenticationForm):
    """Keep the admin login fields empty instead of requesting saved values."""

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
    )


admin.site.login_form = EmptyAdminAuthenticationForm


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # NOTE: Эти поля позволяют быстро просматривать команду и редактировать
    # контакты сотрудника без открытия дополнительных разделов.
    list_display = ('photo_preview', 'full_name', 'position', 'age', 'email', 'phone')
    list_display_links = ('full_name',)
    fields = ('image', 'name', 'fam', 'oth', 'position', 'age', 'description', 'email', 'phone')
    search_fields = ('fam', 'name', 'oth', 'position', 'email', 'phone')
    list_filter = ('position', 'age')
    list_select_related = True
    ordering = ('fam', 'name')
    list_per_page = 25
    save_on_top = True
    empty_value_display = '—'

    @admin.display(description='Сотрудник', ordering='fam')
    def full_name(self, obj):
        return str(obj)

    @admin.display(description='Фото')
    def photo_preview(self, obj):
        if not obj.image:
            return format_html('<span class="admin-empty">Нет фото</span>')
        return format_html(
            '<img class="admin-thumb" src="{}" alt="{}">', obj.image.url, str(obj)
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'description_preview')
    list_display_links = ('name',)
    search_fields = ('name', 'coment')
    ordering = ('name',)
    list_per_page = 25
    save_on_top = True
    fieldsets = ((None, {'fields': ('name', 'coment')}),)

    @admin.display(description='Товаров', ordering='products__count')
    def product_count(self, obj):
        return obj.products_set.count()

    @admin.display(description='Описание')
    def description_preview(self, obj):
        return obj.coment if len(obj.coment) <= 80 else f'{obj.coment[:80]}…'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # NOTE: Описание и изображение доступны редактору прямо в форме товара.
    list_display = ('product_preview', 'name', 'category_name', 'price_display', 'material', 'stock_status', 'date_prod')
    list_display_links = ('name',)
    search_fields = ('name', 'material', 'cat_id__name')
    list_filter = ('cat_id', 'material', 'date_prod')
    ordering = ('name',)
    list_per_page = 25
    date_hierarchy = 'date_prod'
    list_select_related = ('cat_id',)
    save_on_top = True
    save_as = True
    autocomplete_fields = ('cat_id',)
    fieldsets = (
        ('Основная информация', {'fields': ('image', 'name', 'description', 'cat_id')}),
        ('Цена и наличие', {'fields': ('sale', 'conter', 'material', 'date_prod')}),
    )
    actions = ('mark_out_of_stock', 'add_ten_to_stock')

    @admin.action(description='Обнулить остаток выбранных товаров')
    def mark_out_of_stock(self, request, queryset):
        updated = queryset.update(conter=0)
        self.message_user(request, f'Остаток обнулён у товаров: {updated}.')

    @admin.action(description='Добавить 10 единиц к остатку')
    def add_ten_to_stock(self, request, queryset):
        updated = 0
        for product in queryset:
            product.conter += 10
            product.save(update_fields=('conter',))
            updated += 1
        self.message_user(request, f'Остаток увеличен у товаров: {updated}.')

    @admin.display(description='Фото')
    def product_preview(self, obj):
        if not obj.image:
            return format_html('<span class="admin-empty">Нет фото</span>')
        return format_html('<img class="admin-thumb" src="{}" alt="{}">', obj.image.url, obj.name)

    @admin.display(description='Категория', ordering='cat_id__name')
    def category_name(self, obj):
        return obj.cat_id.name

    @admin.display(description='Цена', ordering='sale')
    def price_display(self, obj):
        return format_html('<strong class="admin-price">{} ₽</strong>', f'{obj.sale:,}'.replace(',', ' '))

    @admin.display(description='Остаток', ordering='conter')
    def stock_status(self, obj):
        if obj.conter <= 0:
            return format_html('<span class="admin-badge admin-badge--danger">Нет в наличии</span>')
        if obj.conter <= 5:
            return format_html('<span class="admin-badge admin-badge--warning">Осталось {}</span>', obj.conter)
        return format_html('<span class="admin-badge admin-badge--success">В наличии: {}</span>', obj.conter)


# ==========================================
# Админка для отзывов
# ==========================================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # ! Перед публикацией сайта отзывы желательно модерировать в этой панели.
    # Поля, которые будут отображаться в таблице списка
    list_display = ('name', 'rating_display', 'text_preview', 'created_at')
    
    # Фильтры в правой колонке
    list_filter = ('rating', 'created_at')
    
    # Поля, по которым работает поиск (лупа сверху)
    search_fields = ('name', 'text')
    
    # Сортировка по умолчанию (новые сверху)
    ordering = ('-created_at',)
    
    # Поля, которые нельзя редактировать вручную
    readonly_fields = ('created_at',)
    
    list_per_page = 25
    save_on_top = True
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Отзыв клиента', {'fields': ('name', 'rating', 'text')}),
        ('Публикация', {'fields': ('created_at',)}),
    )
    actions = ('delete_low_rated_reviews',)

    @admin.action(description='Удалить выбранные отзывы с оценкой 1–2')
    def delete_low_rated_reviews(self, request, queryset):
        deleted, _ = queryset.filter(rating__lte=2).delete()
        self.message_user(request, f'Удалено отзывов: {deleted}.')

    # Метод для красивого отображения длинного текста в таблице
    @admin.display(description='Текст отзыва')
    def text_preview(self, obj):
        if len(obj.text) > 60:
            return obj.text[:60] + '...'
        return obj.text

    @admin.display(description='Оценка', ordering='rating')
    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span class="admin-rating">{}</span>', stars)
