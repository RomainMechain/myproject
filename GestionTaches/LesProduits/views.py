from django.shortcuts import render

from django.http import HttpResponse

from LesProduits.models import Product
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from LesProduits.forms import ContactUsForm
from django.core.mail import send_mail

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

def ContactView(request):
    titreh1 = "Contact us !"
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monprojet.com'],
            )
    else:
        form = ContactUsForm()
    return render(request, "contact.html", {'titreh1': titreh1, 'form': form})

class HomeView(TemplateView) :
    template_name = "home.html"

    def post(self, request, **kwargs) :
        return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        return context
    
class HomeParamView(TemplateView) :
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeParamView, self).get_context_data(**kwargs)
        context['titreh1'] = self.kwargs.get("name")
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)

class AboutView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class ProductListView(ListView):
    model = Product
    template_name = "list_products.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['titreh1'] = "Liste des produits"
        context['prdcts'] = Product.objects.all()
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "detail_product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titreh1'] = "Détail produit"
        return context
    
class ConnectView(LoginView):
    template_name = 'login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'home.html', {'titreh1': "hello " + username + ", you're connected"})
        else:
            return render(request, 'register.html')

class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'login.html')
        else:
            return render(request, 'register.html')
        
class DisconnectView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
