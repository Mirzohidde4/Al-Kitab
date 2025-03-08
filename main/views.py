from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector


# Create your views here.
def index_page(request): 
    #! kitoblar 
    object_list = Books.objects.all()
    books = list(object_list)[::-1] 
    
    #! Asosiy qism
    paginator = Paginator(books, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    #! tanlangan kitoblar
    selected_book = SelectedBooks.objects.filter(user=request.user) if request.user.is_authenticated else []
   
    #! eng kop sotilgan kitob
    cache.clear()
    top_books = (
        SellingBooks.objects.values('book', 'book__id', 'book__title')  # Kitobni guruhlash
        .annotate(total_count=Sum('count'))  # sum count
        .order_by('-total_count', '-book__id')  # max count
    ).first()
    if top_books: book_id = top_books['book__id']  
    book_object = Books.objects.get(id=book_id)

    #! kategoriya kitoblar
    book_categorys = Categorys.objects.all()
    paginate = Paginator(books, 4)
    pages_number = request.GET.get("page")
    all_books = paginate.get_page(pages_number)

    #! chegirma kitoblar
    offer_books = OfferBooks.objects.all()

    #! maqollar
    articles = Articles.objects.all()
    
    return render(request, "index.html", {'page_obj': page_obj, 'selected_book': selected_book, 
        'book_object': book_object, 'categorys': book_categorys, 'all_books': all_books, 
        'offer_books': offer_books, 'articles': articles})


def book_detail(request, id):
    book = get_object_or_404(Books, id=id)
    user = request.user
    if request.user.is_authenticated:
        liked = SelectedBooks.objects.filter(user=user, book=book).exists()
    else: liked = False    

    return render(request, 'detail.html', {'book': book, 'liked': liked})


def select_books(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    user = request.user
    liked, created = SelectedBooks.objects.get_or_create(user=user, book=book)

    if not created:  #mavjud bo'lsa o'chirib tashlash
        liked.delete()
        return JsonResponse({'liked': False})
    return JsonResponse({'liked': True})


def search_view(request): #! bitmagan
    name = request.GET.get('search', '')
    search_filter = Books.objects.filter(title__icontains=name).order_by('id') if name else None
    paginator = Paginator(search_filter, 1)
    page_number = request.GET.get("page")
    results = paginator.get_page(page_number)
    return render(request, 'search_results.html', {'results': results, 'name': name}) 


def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")
        else:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect("signup")
            else:
                user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                login(request, user)
                return redirect("index")
    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")  
        else:
            messages.error(request, "Invalid email or password!")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("index")
