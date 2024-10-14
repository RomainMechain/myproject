from django import forms
from LesProduits.models import Product, ProductItem, ProductAttribute, Provider

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
