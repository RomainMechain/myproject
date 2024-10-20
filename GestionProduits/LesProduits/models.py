
from django.db import models
from django.utils import timezone

PRODUCT_STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'Out of stock')              
)

COMMANDE_STATUS = (
    (0, 'En preparation'),
    (1, 'Passée'),
    (2, 'Reçue'),              
)

# Create your models here.
"""
    Status : numero, libelle
"""
class Status(models.Model):
    numero  = models.IntegerField()
    libelle = models.CharField(max_length=100)
          
    def __str__(self):
        return "{0} {1}".format(self.numero, self.libelle)
    
"""
Produit : nom, code, etc.
"""
class Product(models.Model):

    class Meta:
        verbose_name = "Produit"

    name          = models.CharField(max_length=100)
    code          = models.CharField(max_length=10, null=True, blank=True, unique=True)
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    price_ttc     = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation =  models.DateTimeField(blank=True, verbose_name="Date création", default=timezone.now) 
    
    def __str__(self):
        return "{0} {1}".format(self.name, self.code)

"""
    Déclinaison de produit déterminée par des attributs comme la couleur, etc.
"""
class ProductItem(models.Model):
    
    class Meta:
        verbose_name = "Déclinaison Produit"

    color   = models.CharField(max_length=100)
    code    = models.CharField(max_length=10, null=True, blank=True, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attributes  = models.ManyToManyField("ProductAttributeValue", related_name="product_item", blank=True)
    quantity = models.PositiveIntegerField("Quantité", default=0, null=True, blank=True)
       
    def __str__(self):
        attributes_str = ", ".join([attr.value for attr in self.attributes.all()])
        return "{0} {1}".format(self.product.name, attributes_str)
    
class ProductAttribute(models.Model):
    """
    Attributs produit
    """
    
    class Meta:
        verbose_name = "Attribut"
        
    name =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class ProductAttributeValue(models.Model):
    """
    Valeurs des attributs
    """
    
    class Meta:
        verbose_name = "Valeur attribut"
        ordering = ['position']
        
    value              = models.CharField(max_length=100)
    product_attribute  = models.ForeignKey('ProductAttribute', verbose_name="Unité", on_delete=models.CASCADE)
    position           = models.PositiveSmallIntegerField("Position", null=True, blank=True)
     
    def __str__(self):
        return "{0} [{1}]".format(self.value, self.product_attribute)
    
class Provider(models.Model):
    """
    Fournisseur
    """
    
    class Meta:
        verbose_name = "Fournisseur"
        
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return "{0} [{1}]".format(self.name, self.address)
    
class ProviderProductPrice(models.Model):
    """
    Prix d'achat d'un produit chez un fournisseur
    """
    
    class Meta:
        verbose_name = "Prix d'achat"
        
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    
    def __str__(self):
        return "{0} [{1}]".format(self.product, self.provider)
    
class Order(models.Model):
    """
    Commande
    """
    
    class Meta:
        verbose_name = "Commande"
        
    date_creation =  models.DateTimeField(blank=True, verbose_name="Date création", default=timezone.now) 
    status = models.SmallIntegerField(choices=COMMANDE_STATUS, default=0)
    name = models.CharField(max_length=100)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)
    
    def __str__(self):
        return "{0} [{1}]".format(self.name, self.date_creation)

    def get_status_display(self):
        return dict(COMMANDE_STATUS).get(self.status)
    
class OrderProductItem(models.Model):
    """
    Produit commandé
    """
    
    class Meta:
        verbose_name = "Produit commandé"
        
    productItem = models.ForeignKey('ProductItem', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Quantité", default=0, null=True, blank=True)

    def __str__(self):
        return "{0} [{1}]".format(self.productItem, self.order)
    
    
    


#python3 manage.py makemigrations LesProduits
#python3 manage.py sqlmigrate LesProduits 0001
#python manage.py migrate