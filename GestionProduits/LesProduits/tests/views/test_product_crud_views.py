from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from LesProduits.models import Product

class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_create_view_get(self):
        """
        Tester que la vue de création renvoie le bon template et s'affiche correctement
        """
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'LesProduits/new_product.html')

    def test_create_view_post_valid(self):
        """
        Tester que la vue de création crée un nouvel objet lorsque les données sont valides
        """
        data = {
            'name': 'Booster Pokémon',
            'code': 'BP001',
            'price_ht': 5.00,
            'price_ttc': 6.00,
            'status': 1
        }
        response = self.client.post(reverse('product-add'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'Booster Pokémon')

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Booster Pokémon',
            code='BP001',
            price_ht=5.00,
            price_ttc=6.00,
            status=1
        )

    def test_detail_view(self):
        """
        Tester que la vue de détail renvoie le bon template et affiche les bonnes données
        """
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'LesProduits/detail_product.html')
        self.assertContains(response, 'Booster Pokémon')
        self.assertContains(response, 'BP001')

class ProductUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(
            name='Booster Pokémon',
            code='BP001',
            price_ht=5.00,
            price_ttc=6.00,
            status=1
        )

    def test_update_view_get(self):
        """
        Tester que la vue de mise à jour s'affiche correctement
        """
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'LesProduits/update_product.html')

    def test_update_view_post_valid(self):
        """
        Tester que la vue met à jour l'objet lorsque les données sont valides
        """
        data = {
            'name': 'ETB Pokémon',
            'code': 'EP001',
            'price_ht': 40.00,
            'price_ttc': 48.00,
            'status': 1
        }
        response = self.client.post(reverse('product-update', args=[self.product.id]), data)
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'ETB Pokémon')
        self.assertEqual(self.product.code, 'EP001')

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(
            name='Booster Pokémon',
            code='BP001',
            price_ht=5.00,
            price_ttc=6.00,
            status=1
        )

    def test_delete_view_get(self):
        """
        Tester que la vue de suppression s'affiche correctement
        """
        response = self.client.get(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'LesProduits/delete_product.html')

    def test_delete_view_post(self):
        """
        Tester que l'objet est supprimé lorsque le formulaire de suppression est soumis
        """
        response = self.client.post(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)