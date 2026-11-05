from django.contrib import admin
from .models import Person, Category, Products, Review


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'fam', 'name', 'oth', 'age')
    search_fields = ('fam', 'name', 'oth')
    list_filter = ('age',)
    ordering = ('fam', 'name')
    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coment')
    search_fields = ('name', 'coment')
    ordering = ('name',)
    list_per_page = 25


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_preview', 'sale', 'material', 'date_prod', 'conter', 'cat_id')
    fields = ('name', 'description', 'image', 'sale', 'material', 'date_prod', 'conter', 'cat_id')
    search_fields = ('name', 'material', 'cat_id__name')
    list_filter = ('cat_id', 'material', 'date_prod')
    ordering = ('name',)
    list_per_page = 25
    date_hierarchy = 'date_prod'

    @admin.display(description='Фото')
    def image_preview(self, obj):
        if not obj.image:
            return '—'
        return f'Есть: {obj.image.name}'


# ==========================================
# НОВОЕ: Админка для отзывов
# ==========================================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в таблице списка
    list_display = ('name', 'rating', 'text_preview', 'created_at')
    
    # Фильтры в правой колонке
    list_filter = ('rating', 'created_at')
    
    # Поля, по которым работает поиск (лупа сверху)
    search_fields = ('name', 'text')
    
    # Сортировка по умолчанию (новые сверху)
    ordering = ('-created_at',)
    
    # Поля, которые нельзя редактировать вручную
    readonly_fields = ('created_at',)
    
    list_per_page = 25

    # Метод для красивого отображения длинного текста в таблице
    @admin.display(description='Текст отзыва')
    def text_preview(self, obj):
        if len(obj.text) > 60:
            return obj.text[:60] + '...'
        return obj.text
