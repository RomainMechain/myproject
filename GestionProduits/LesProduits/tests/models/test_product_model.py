from django.test import TestCase
from LesProduits.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Booster Pokémon",
            code="BP001",
            price_ht=5.00,
            price_ttc=6.00,
            status=1
        )

    def test_product_creation(self):
        """
        Tester si un Product est bien créé
        """
        self.assertEqual(self.product.name, "Booster Pokémon")
        self.assertEqual(self.product.code, "BP001")
        self.assertEqual(self.product.price_ht, 5.00)
        self.assertEqual(self.product.price_ttc, 6.00)
        self.assertEqual(self.product.status, 1)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Product
        """
        self.assertEqual(str(self.product), "Booster Pokémon BP001")

    def test_update_product(self):
        """
        Tester la mise à jour d'un Product
        """
        self.product.name = "ETB Pokémon"
        self.product.save()
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, "ETB Pokémon")

    def test_delete_product(self):
        """
        Tester la suppression d'un Product
        """
        self.product.delete()
        self.assertEqual(Product.objects.count(), 0)