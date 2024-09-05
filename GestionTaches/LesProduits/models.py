from django.db import models

# Create your models here.

from django.db import models

class Product(models.Model) : 
    name = models.CharField(max_length=250)
    code = models.IntegerField()

    def __unicode__(self) :
        return "{0} [{1}]".format(self.name, self.code)
    
class ProductItem(models.Model) : 
    color = models.CharField(max_length=100)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)

    def __unicode__(self) :
        return "{0} [{1}] [{2}]".format(self.product.name, self.product.code, self.color)


#python3 manage.py makemigrations LesProduits
#python3 manage.py sqlmigrate LesProduits 0001
#python manage.py migrate