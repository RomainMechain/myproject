from django.shortcuts import render

from django.http import HttpResponse

from LesProduits.models import Product

# Create your views here.

def index(request, name) :
    return HttpResponse("Bonjour, voici ma première vue, il est écrit : " + name)

def home(request) :
    return HttpResponse("Bonjour, voici ma première vue, il n'y a aucun paramètres")

def listProducts(request) : 
    prdts = Product.objects.all()
    res = "<h1> Liste de mes produits </h1><ul>"
    for prod in prdts : 
        res += f"<li>{prod.name}</li>"
    res += "</ul>"
    return HttpResponse(res)

