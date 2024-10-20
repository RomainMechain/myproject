from django.test import TestCase
from LesProduits.models import Product, ProductItem, ProductAttribute, ProductAttributeValue

class ProductItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Booster Pokémon",
            code="BP001",
            price_ht=5.00,
            price_ttc=6.00,
            status=1
        )
        self.attribute = ProductAttribute.objects.create(name="Color")
        self.attribute_value = ProductAttributeValue.objects.create(
            value="Red", product_attribute=self.attribute, position=1
        )
        self.product_item = ProductItem.objects.create(
            color="Red",
            code="PI001",
            product=self.product,
            quantity=10
        )
        self.product_item.attributes.add(self.attribute_value)

    def test_product_item_creation(self):
        """
        Tester si un ProductItem est bien créé
        """
        self.assertEqual(self.product_item.color, "Red")
        self.assertEqual(self.product_item.code, "PI001")
        self.assertEqual(self.product_item.product, self.product)
        self.assertEqual(self.product_item.quantity, 10)
        self.assertIn(self.attribute_value, self.product_item.attributes.all())

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle ProductItem
        """
        self.assertEqual(str(self.product_item), "Booster Pokémon Red")

    def test_update_product_item(self):
        """
        Tester la mise à jour d'un ProductItem
        """
        self.product_item.color = "Blue"
        self.product_item.save()
        updated_product_item = ProductItem.objects.get(id=self.product_item.id)
        self.assertEqual(updated_product_item.color, "Blue")

    def test_delete_product_item(self):
        """
        Tester la suppression d'un ProductItem
        """
        self.product_item.delete()
        self.assertEqual(ProductItem.objects.count(), 0)