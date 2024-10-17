from django import forms
from LesProduits.models import Product, ProductItem, ProductAttribute, Provider, ProviderProductPrice, Order, OrderProductItem

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['status']

class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        #fields = '__all__'
        exclude = ['price_ttc', 'status']


class AttributsValuesForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        #fields = '__all__'
        exclude = ['price_ttc', 'status']

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        exclude = ['status']

class ProviderProductPriceUpdateForm(forms.ModelForm):
    class Meta:
        model = ProviderProductPrice
        exclude = ['provider', 'product']

class ProviderProductPriceCreateForm(forms.ModelForm):
    class Meta:
        model = ProviderProductPrice
        exclude = ['provider']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['status', 'date_creation', 'provider']

class OrderProductItemForm(forms.ModelForm):
    class Meta:
        model = OrderProductItem
        exclude = ['order']

    def __init__(self, *args, **kwargs):
        provider_id = kwargs.pop('provider_id', None)
        super(OrderProductItemForm, self).__init__(*args, **kwargs)  
        if provider_id:
            products = ProviderProductPrice.objects.filter(provider_id=provider_id).values_list('product_id', flat=True)
            self.fields['productItem'].queryset = ProductItem.objects.filter(product_id__in=products)
