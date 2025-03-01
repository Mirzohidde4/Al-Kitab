from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.
admin.site.unregister(Group)


@admin.register(Categorys)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)


@admin.register(Books)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'author', 'price', 'genre')
    list_filter = ('genre', 'author', 'price')
    search_fields = ('title', 'author')    