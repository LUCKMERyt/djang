from django.contrib import admin
from .models import Person, Category, Products, RegisteredUser


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
    list_display = ('id', 'name', 'sale', 'material', 'date_prod', 'conter', 'cat_id')
    search_fields = ('name', 'material', 'cat_id__name')
    list_filter = ('cat_id', 'material', 'date_prod')
    ordering = ('name',)
    list_per_page = 25
    date_hierarchy = 'date_prod'


@admin.register(RegisteredUser)
class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)
    list_per_page = 25
    exclude = ('password',)