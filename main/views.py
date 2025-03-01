from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator

# Create your views here.
def IndexPage(request): 
    object_list = Books.objects.all()
    books = []
    for book in object_list:
        books.insert(0, book) 
    paginator = Paginator(books, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {'page_obj': page_obj})
