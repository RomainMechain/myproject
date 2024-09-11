from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone

class Statut(models.Model) : 
    numStatut = models.IntegerField()
    libele = models.CharField(max_length=250)

    def __unicode__(self) :
        return "numStatut : {0} libele : {1}".format(self.numStatut, self.libele)
    
    def __str__(self) -> str:
        return "numStatut : {0} libele : {1}".format(self.numStatut, self.libele)

class Product(models.Model) : 
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=10, null=True, unique=True)
    prixHT = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dateFabrication = models.DateTimeField(blank=True, default=timezone.now)
    statut = models.ForeignKey("Statut",on_delete=models.CASCADE)

    def __unicode__(self) :
        return "name : {0} code : {1} prixHT : {2}euros dateFabrication {3} statut : {4}".format(self.name, self.code, self.prixHT, self.dateFabrication, self.statut.libele)
    
    def __str__(self) -> str:
        return "name : {0} code : {1} prixHT : {2}euros dateFabrication {3} statut : {4}".format(self.name, self.code, self.prixHT, self.dateFabrication, self.statut.libele)
    
class ProductItem(models.Model) : 
    codeItem = models.CharField(max_length=10, null=True, unique=True)
    color = models.CharField(max_length=100)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)

    def __unicode__(self) :
        return "codeItem : {0} color: {1} product name : {2}".format(self.codeItem, self.color, self.product.name)
    
    def __str__(self) -> str:
        return "codeItem : {0} color: {1} product name : {2}".format(self.codeItem, self.color, self.product.name)


#python3 manage.py makemigrations LesProduits
#python3 manage.py sqlmigrate LesProduits 0001
#python manage.py migrate