from django.test import TestCase
from LesProduits.forms import ProductItemForm
from LesProduits.models import Product, ProductItem, ProductAttribute, ProductAttributeValue

class ProductItemFormTest(TestCase):
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

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        form = ProductItemForm(data={
            'color': 'Red',
            'code': 'PI001',
            'product': self.product.id,
            'quantity': 10,
            'attributes': [self.attribute_value.id]
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'color' est manquant
        """
        form = ProductItemForm(data={
            'code': 'PI001',
            'product': self.product.id,
            'quantity': 10,
            'attributes': [self.attribute_value.id]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('color', form.errors)

    def test_form_save(self):
        """
        Tester que le formulaire peut être enregistré avec des données valides
        """
        form = ProductItemForm(data={
            'color': 'Red',
            'code': 'PI001',
            'product': self.product.id,
            'quantity': 10,
            'attributes': [self.attribute_value.id]
        })
        self.assertTrue(form.is_valid())
        product_item = form.save()
        self.assertEqual(product_item.color, 'Red')
        self.assertEqual(product_item.code, 'PI001')
        self.assertEqual(product_item.product, self.product)
        self.assertEqual(product_item.quantity, 10)
        self.assertIn(self.attribute_value, product_item.attributes.all())