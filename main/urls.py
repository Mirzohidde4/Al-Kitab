from django.urls import path
from .views import IndexPage


urlpatterns = [
    path('', IndexPage, name='index'),
]