from django.shortcuts import render
from django.http import HttpResponse
from LesProduits.models import Product, ProductAttribute, ProductAttributeValue, ProductItem
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from LesProduits.forms import ContactUsForm, ProductForm, ProductItemForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required , user_passes_test
from django.utils.decorators import method_decorator

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

# les Produits :

# def listProducts(request) : 
#     prdcts = Product.objects.all()
#     return render(request, 'LesProduits/list_products.html', {'prdcts' : prdcts})

class ProductListView(ListView):
    model = Product
    template_name = "LesProduits/list_products.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['titreh1'] = "Liste des produits"
        context['prdcts'] = Product.objects.all()
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "LesProduits/detail_product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['items'] = ProductItem.objects.filter(product=self.object)
        context['titreh1'] = "Détail produit"
        return context
    
@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class=ProductForm
    template_name = "LesProduits/new_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
   
@method_decorator(login_required, name='dispatch')   
class ProductUpdateView(UpdateView):
    model = Product
    form_class=ProductForm
    template_name = "LesProduits/update_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)

@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView) : 
    model = Product
    template_name = "LesProduits/delete_product.html"
    success_url = reverse_lazy('product-list')

# Authentification :

class ConnectView(LoginView):
    template_name = 'Authentification/login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'home.html', {'titreh1': "hello " + username + ", you're connected"})
        else:
            return render(request, 'Authentification/register.html')

class RegisterView(TemplateView):
    template_name = 'Authentification/register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'Authentification/login.html')
        else:
            return render(request, 'Authentification/register.html')
        
class DisconnectView(TemplateView):
    template_name = 'Authentification/logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
# Attributes :

@method_decorator(login_required, name='dispatch')
class ProductAttributeListView(ListView):
    model = ProductAttribute
    template_name = "Attributs/list_ProductAttribute.html"
    context_object_name = "productattributes"

    def get_queryset(self ):
        return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')
    
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context
    
@method_decorator(login_required, name='dispatch')
class ProductAttributeDetailView(DetailView):
    model = ProductAttribute
    template_name = "Attributs/detail_attribute.html"
    context_object_name = "productattribute"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values']=ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
        return context
    
# Items :

class ProductItemListView(ListView):
    model = ProductItem
    template_name = "Items/list_items.html"
    context_object_name = "productitems"

    def get_queryset(self ):
        return ProductItem.objects.select_related('product').prefetch_related('attributes')
    
    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des déclinaisons"
        return context
    
@method_decorator(login_required, name='dispatch')
class ProductItemDetailView(DetailView):
    model = ProductItem
    template_name = "Items/item_detail.html"
    context_object_name = "productitem"
    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail déclinaison"
        # Récupérer les attributs associés à cette déclinaison
        context['attributes'] = self.object.attributes.all()
        return context
    
@method_decorator(login_required, name='dispatch')   
class ProductItemDeleteView(DeleteView) : 
    model = ProductItem
    template_name = "Items/delete_items.html"
    success_url = reverse_lazy('item-list')

@method_decorator(login_required, name='dispatch')   
class ProductItemUpdateView(UpdateView):
    model = ProductItem
    form_class=ProductItemForm
    template_name = "Items/update_product_item.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('item-detail', product.id)
    

@method_decorator(login_required, name='dispatch')
class ProductItemCreateView(CreateView):
    model = ProductItem
    form_class=ProductItemForm
    template_name = "Items/new_item.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('item-list')
    
# Support :
    
class AboutView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
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
    return render(request, "Support/contact.html", {'titreh1': titreh1, 'form': form})