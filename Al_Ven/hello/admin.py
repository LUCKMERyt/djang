from django.contrib import admin

# Register your models here.

# admin.site.register(Genre)


# from myapp 


# admin.site.register(kladm)

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_display_links = ('id',)
    list_editable = ('title', 'author')

# admin.site.register(Book, BookAdmin)
# admin.site.register(Discussion)
# admin.site.register(Products)
# admin.site.register(Category)