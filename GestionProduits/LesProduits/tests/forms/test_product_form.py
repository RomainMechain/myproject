from django.test import TestCase
from LesProduits.forms import ProductForm
from LesProduits.models import Product

class ProductFormTest(TestCase):
    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        form = ProductForm(data={
            'name': 'Booster Pokémon',
            'code': 'BP001',
            'price_ht': 5.00,
            'price_ttc': 6.00,
            'status': 1
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'name' est manquant
        """
        form = ProductForm(data={
            'code': 'BP001',
            'price_ht': 5.00,
            'price_ttc': 6.00,
            'status': 1
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_save(self):
        """
        Tester que le formulaire peut être enregistré avec des données valides
        """
        form = ProductForm(data={
            'name': 'Booster Pokémon',
            'code': 'BP001',
            'price_ht': 5.00,
            'price_ttc': 6.00,
            'status': 1
        })
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.name, 'Booster Pokémon')
        self.assertEqual(product.code, 'BP001')
        self.assertEqual(product.price_ht, 5.00)
        self.assertEqual(product.price_ttc, 6.00)
        self.assertEqual(product.status, 1)