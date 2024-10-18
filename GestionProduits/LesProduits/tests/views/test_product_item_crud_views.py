from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from LesProduits.models import Product, ProductItem, ProductAttribute, ProductAttributeValue

class ProductItemCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
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

    def test_create_view_get(self):
        """
        Tester que la vue de création renvoie le bon template et s'affiche correctement
        """
        response = self.client.get(reverse('item-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Items/new_item.html')


class ProductItemDetailViewTest(TestCase):
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
        self.attribute = ProductAttribute.objects.create(name="Color")
        self.attribute_value = ProductAttributeValue.objects.create(
            value="Red", product_attribute=self.attribute, position=1
        )
        self.product_item = ProductItem.objects.create(
            color='Red',
            code='PI001',
            product=self.product,
            quantity=10
        )
        self.product_item.attributes.add(self.attribute_value)

    def test_detail_view(self):
        """
        Tester que la vue de détail renvoie le bon template et affiche les bonnes données
        """
        response = self.client.get(reverse('item-detail', args=[self.product_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Items/item_detail.html')
        self.assertContains(response, 'Red')
        self.assertContains(response, 'PI001')

class ProductItemUpdateViewTest(TestCase):
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
        self.attribute = ProductAttribute.objects.create(name="Color")
        self.attribute_value = ProductAttributeValue.objects.create(
            value="Red", product_attribute=self.attribute, position=1
        )
        self.product_item = ProductItem.objects.create(
            color='Red',
            code='PI001',
            product=self.product,
            quantity=10
        )
        self.product_item.attributes.add(self.attribute_value)

    def test_update_view_get(self):
        """
        Tester que la vue de mise à jour s'affiche correctement
        """
        response = self.client.get(reverse('item-update', args=[self.product_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Items/update_product_item.html')

    def test_update_view_post_valid(self):
        """
        Tester que la vue met à jour l'objet lorsque les données sont valides
        """
        data = {
            'color': 'Blue',
            'code': 'PI001',
            'product': self.product.id,
            'quantity': 20,
            'attributes': [self.attribute_value.id]
        }
        response = self.client.post(reverse('item-update', args=[self.product_item.id]), data)
        self.assertEqual(response.status_code, 302)
        self.product_item.refresh_from_db()
        self.assertEqual(self.product_item.color, 'Blue')
        self.assertEqual(self.product_item.quantity, 20)

class ProductItemDeleteViewTest(TestCase):
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
        self.attribute = ProductAttribute.objects.create(name="Color")
        self.attribute_value = ProductAttributeValue.objects.create(
            value="Red", product_attribute=self.attribute, position=1
        )
        self.product_item = ProductItem.objects.create(
            color='Red',
            code='PI001',
            product=self.product,
            quantity=10
        )
        self.product_item.attributes.add(self.attribute_value)

    def test_delete_view_get(self):
        """
        Tester que la vue de suppression s'affiche correctement
        """
        response = self.client.get(reverse('item-delete', args=[self.product_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Items/delete_items.html')

    def test_delete_view_post(self):
        """
        Tester que l'objet est supprimé lorsque le formulaire de suppression est soumis
        """
        response = self.client.post(reverse('item-delete', args=[self.product_item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductItem.objects.count(), 0)