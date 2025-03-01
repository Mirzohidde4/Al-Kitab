from django.shortcuts import render

# Create your views here.
def IndexPage(request): 
    return render(request, "index.html")


def FeaturedPage(request): 
    return render(request, "featured-books.html")


def PopularPage(request): 
    return render(request, "popular-books.html")


def OfferPage(request): 
    return render(request, "special-offer.html")


def ArticlesPage(request): 
    return render(request, "latest-blog.html")


def DownloadAppPage(request): 
    return render(request, "download-app.html")