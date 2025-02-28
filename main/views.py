from django.shortcuts import render

# Create your views here.
def IndexPage(request): 
    return render(request, "index.html")