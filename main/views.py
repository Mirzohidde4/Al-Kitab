from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def index_page(request): 
    object_list = Books.objects.all()
    selected_book = SelectedBooks.objects.filter(user=request.user) if request.user.is_authenticated else []
    books = list(object_list)[::-1] 
    paginator = Paginator(books, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {'page_obj': page_obj, 'selected_book': selected_book})


def book_detail(request, id):
    book = get_object_or_404(Books, id=id)
    return render(request, 'detail.html', {'book': book})


def select_books(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    user = request.user
    liked, created = SelectedBooks.objects.get_or_create(user=user, book=book)

    if not created:  #mavjud bo'lsa o'chirib tashlash
        liked.delete()
        return JsonResponse({'liked': False})
    return JsonResponse({'liked': True})


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
            return redirect("index")  # Bosh sahifaga yo‘naltirish
        else:
            messages.error(request, "Invalid email or password!")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("index")
