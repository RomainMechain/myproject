from django.shortcuts import render, get_object_or_404
from LesProduits.models import Product, ProductAttribute, ProductAttributeValue, ProductItem, Provider, ProviderProductPrice, Order, OrderProductItem
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from LesProduits.forms import ContactUsForm, ProductForm, ProductItemForm , AttributsValuesForm, ProviderForm, ProviderProductPriceUpdateForm, ProviderProductPriceCreateForm, OrderForm, OrderProductItemForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required , user_passes_test
from django.utils.decorators import method_decorator
from functools import wraps
from django.utils import timezone

# Décorateurs :

def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap

# Home :

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
    
@method_decorator(admin_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class=ProductForm
    template_name = "LesProduits/new_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
   
@method_decorator(admin_required, name='dispatch')   
class ProductUpdateView(UpdateView):
    model = Product
    form_class=ProductForm
    template_name = "LesProduits/update_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)

@method_decorator(admin_required, name='dispatch')
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
    
@method_decorator(admin_required, name='dispatch')
class ProductAttributeCreateView(CreateView):
    model = ProductAttribute
    form_class=AttributsValuesForm
    template_name = "Attributs/new_attributs.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('attribut-list')
   
@method_decorator(admin_required, name='dispatch')   
class ProductAttributeUpdateView(UpdateView):
    model = ProductAttribute
    form_class=AttributsValuesForm
    template_name = "Attributs/update_attribut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return redirect('attribut-list')

@method_decorator(admin_required, name='dispatch')
class ProductAttributeDeleteView(DeleteView) : 
    model = ProductAttribute
    template_name = "Attributs/delete_attribute.html"
    success_url = reverse_lazy('attribut-list')
    
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
        # Ajouter la plage de quantités disponibles
        context['quantity_range'] = range(1, self.object.quantity + 1)
        #Calculer le prix total
        context['total_price'] = self.object.product.price_ttc * self.object.quantity
        return context
    
@method_decorator(admin_required, name='dispatch')   
class ProductItemDeleteView(DeleteView) : 
    model = ProductItem
    template_name = "Items/delete_items.html"
    success_url = reverse_lazy('item-list')

@method_decorator(admin_required, name='dispatch')   
class ProductItemUpdateView(UpdateView):
    model = ProductItem
    form_class=ProductItemForm
    template_name = "Items/update_product_item.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('item-detail', product.id)

@method_decorator(admin_required, name='dispatch')
class ProductItemCreateView(CreateView):
    model = ProductItem
    form_class=ProductItemForm
    template_name = "Items/new_item.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('item-list')
    
# Achat :

@method_decorator(login_required, name='dispatch')
class AchatView(TemplateView):
    template_name = "Achat/achat.html"

    def get_context_data(self, **kwargs):
        context = super(AchatView, self).get_context_data(**kwargs)
        context['titreh1'] = "Achat"
        return context
    
    def post(self, request, *args, **kwargs):
        productitem_id = kwargs.get('productitem_id')
        quantity = int(request.POST.get('quantity'))
        unit_price = request.POST.get('unit_price').replace(',', '.')
        unit_price = float(unit_price)
        total_price = unit_price * quantity
        return redirect(f"{reverse('achat_produit', args=[productitem_id])}?quantity={quantity}&price={total_price:.2f}")

    def get(self, request, *args, **kwargs):
        productitem_id = kwargs.get('productitem_id')
        quantity = int(request.GET.get('quantity', 0))
        if quantity > 0:
            try:
                productitem = ProductItem.objects.get(id=productitem_id)
            except ProductItem.DoesNotExist:
                raise Http404(f"ProductItem with id {productitem_id} does not exist")
            if productitem.quantity >= quantity:
                productitem.quantity -= quantity
                productitem.save()
            return redirect('item-list')
        return super().get(request, *args, **kwargs)
    
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

# Provider : 

@method_decorator(admin_required, name='dispatch')
class ProviderListView(ListView):
    model = Provider
    template_name = "Provider/list_providers.html"
    context_object_name = "providers"

    def get_context_data(self, **kwargs):
        context = super(ProviderListView, self).get_context_data(**kwargs)
        context['titreh1'] = "Liste des fournisseurs"
        context['providers'] = Provider.objects.all()
        return context
    
@method_decorator(admin_required, name='dispatch')
class ProviderDetailView(DetailView):
    model = Provider
    template_name = "Provider/detail_provider.html"
    context_object_name = "provider"

    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)
        context['titreh1'] = "Détail fournisseur"
        context['productsPrice'] = ProviderProductPrice.objects.filter(provider=self.object)
        return context
    
@method_decorator(admin_required, name='dispatch')
class ProviderCreateView(CreateView):
    model = Provider
    form_class = ProviderForm
    template_name = "Provider/new_provider.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        provider = form.save()
        return redirect('provider-list')
    
@method_decorator(admin_required, name='dispatch')
class ProviderUpdateView(UpdateView):
    model = Provider
    form_class = ProviderForm
    template_name = "Provider/update_provider.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        provider = form.save()
        return redirect('provider-detail', provider.id)
    
@method_decorator(admin_required, name='dispatch')
class ProviderDeleteView(DeleteView) : 
    model = Provider
    template_name = "Provider/delete_provider.html"
    success_url = reverse_lazy('provider-list')

# ProviderProductPrice :

@method_decorator(admin_required, name='dispatch')
class ProviderProductPriceUpdateView(UpdateView):
    model = ProviderProductPrice
    form_class = ProviderProductPriceUpdateForm
    template_name = "ProviderProductPrice/update_provider_product_price.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        providerProductPrice = form.save()
        return redirect('provider-detail', providerProductPrice.provider.id)

@method_decorator(admin_required, name='dispatch')
class ProviderProductPriceDeleteView(DeleteView):
    model = ProviderProductPrice
    template_name = "ProviderProductPrice/delete_provider_product_price.html"

    def get_success_url(self):
        provider_id = self.object.provider.id
        return reverse('provider-detail', kwargs={'pk': provider_id})

@method_decorator(admin_required, name='dispatch')
class ProviderProductPriceCreateView(CreateView):
    model = ProviderProductPrice
    form_class = ProviderProductPriceCreateForm
    template_name = "ProviderProductPrice/new_provider_product_price.html"

    # Permet de passer un instance de provider à la création du formulaire, pour filtrer les produits qui ont déjà un prix pour ce fournisseur
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        provider_id = self.kwargs.get('provider_id')
        provider = get_object_or_404(Provider, id=provider_id)
        kwargs['provider'] = provider
        return kwargs

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        provider_id = self.kwargs.get('provider_id')
        form.instance.provider = Provider.objects.get(id=provider_id)
        providerProductPrice = form.save()
        return redirect('provider-detail', providerProductPrice.provider.id)
    
# Orders :

@method_decorator(admin_required, name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "Orders/new_order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['order_product_item_form'] = OrderProductItemForm(self.request.POST, provider_id=self.kwargs.get('provider_id'))
        else:
            context['order_product_item_form'] = OrderProductItemForm(provider_id=self.kwargs.get('provider_id'))
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = self.get_context_data()
        provider_id = self.kwargs.get('provider_id')
        form.instance.provider = Provider.objects.get(id=provider_id)
        form.instance.date_creation = timezone.now()
        order = form.save()
        order_product_item_form = context['order_product_item_form']
        product_item_selected = order_product_item_form.data.get('productItem')
        if product_item_selected:
            order_product_item_form.instance.order = order
            order_product_item_form.save()
        else:
            # Supprime la commande si aucun item n'est sélectionné
            order.delete()
        return redirect('provider-detail', order.provider.id)

@method_decorator(admin_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = "Orders/list_orders.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['titreh1'] = "Liste des commandes"
        context['orders'] = Order.objects.all()
        return context
    
@method_decorator(admin_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = "Orders/detail_order.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['titreh1'] = "Détail commande"
        OrderProductItems = OrderProductItem.objects.filter(order=self.object)
        items = []
        total_order = 0
        for item in OrderProductItems:
            price_unitaire = ProviderProductPrice.objects.get(provider=self.object.provider, product=item.productItem.product)
            items.append({'item': item.productItem, 'price_unitaire': price_unitaire.price, 'quantity': item.quantity, 'total': item.quantity * price_unitaire.price})
            total_order += item.quantity * price_unitaire.price
        context['items'] = items
        context['total_order'] = total_order
        return context

@method_decorator(admin_required, name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    template_name = "Orders/delete_order.html"
    success_url = reverse_lazy('order-list')

@method_decorator(admin_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "Orders/update_order.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        order = form.save()
        return redirect('order-detail', order.id)

# OrderProductItem :

@method_decorator(admin_required, name='dispatch')
class OrderProductItemCreateView(CreateView):
    model = OrderProductItem
    form_class = OrderProductItemForm
    template_name = "Orders/new_order_product_item.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        order = Order.objects.get(id=self.kwargs.get('order_id'))
        provider_id = order.provider.id
        kwargs['provider_id'] = provider_id
        return kwargs

    def form_valid(self, form):
        order_id = self.kwargs.get('order_id')
        form.instance.order = Order.objects.get(id=order_id)
        order_product_item = form.save()
        return redirect('order-detail', order_product_item.order.id)

# Actions sur les commandes : 

@admin_required
def order_passed(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 1
    order.save()
    return redirect('order-detail', order_id)

@admin_required
def order_received(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 2
    order.save()
    items = OrderProductItem.objects.filter(order=order)
    for item in items:
        product_item = item.productItem
        product_item.quantity += item.quantity
        product_item.save()
    return redirect('order-detail', order_id)
