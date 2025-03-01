from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexPage, name='index'),
    # path('featured/', FeaturedPage, name='featured-books'),
    # path('popular/', PopularPage, name='popular-books'),
    # path('offer/', OfferPage, name='special-offer'),
    # path('articles/', ArticlesPage, name='latest-blog'),
    # path('download-app/', DownloadAppPage, name='download-app'),
]