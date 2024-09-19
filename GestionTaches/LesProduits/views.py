from django.shortcuts import render

from django.http import HttpResponse

from LesProduits.models import Product

# Create your views here.

def index(request, name) :
    return HttpResponse("Bonjour, voici ma première vue, il est écrit : " + name)

def home(request) :
    print(request.__dict__)
    name_r = request.GET["name"]
    return HttpResponse("Bonjour, voici ma première vue, il n'y a aucun paramètres, vous êtes : "+name_r)

def listProducts(request) : 
    prdcts = Product.objects.all()
    return render(request, 'list_products.html', {'prdcts' : prdcts})

# def product(request, code) : 
#     prod = Product.objects.

