from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import *
from django.db.models import Sum


# Register your models here.
admin.site.unregister(Group)


@admin.register(Categorys)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Books)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'author', 'price', 'display_genres')
    list_filter = ('genre', 'author', 'price')
    search_fields = ('title', 'author')    

    def display_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
    
    display_genres.short_description = 'Janrlar'
    autocomplete_fields = ['genre']


@admin.register(CustomUser)
class UserAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_superuser', 'is_staff')


@admin.register(SelectedBooks)
class SelectedBookAdmin(ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    autocomplete_fields = ['user', 'book']


@admin.register(SellingBooks)
class SellingBooksAdmin(ModelAdmin):
    list_display = ('book', 'count', 'created_at', 'updated_at')
    list_filter = ('count',)
    autocomplete_fields = ['book']