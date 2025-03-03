from django.urls import path
from .views import *


urlpatterns = [
    path('', index_page, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('detail/<int:id>/', book_detail, name='detail'),
    path('like/<int:book_id>/', select_books, name='like_book'),
]