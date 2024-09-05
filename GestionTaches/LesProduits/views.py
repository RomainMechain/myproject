from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request, name) :
    return HttpResponse("Bonjour, voici ma première vue, il est écrit : " + name)

def home(request) :
    return HttpResponse("Bonjour, voici ma première vue, il n'y a aucun paramètres")
