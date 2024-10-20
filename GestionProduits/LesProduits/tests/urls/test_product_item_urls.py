from django.test import SimpleTestCase
from django.urls import reverse, resolve
from LesProduits.views import ProductItemCreateView, ProductItemListView, ProductItemDetailView, ProductItemUpdateView, ProductItemDeleteView

class ProductItemTestUrls(SimpleTestCase):
    def test_create_view_url_is_resolved(self):
        """
        Tester que l'URL de la création de ProductItem renvoie la bonne vue
        """
        url = reverse('item-add')
        self.assertEqual(resolve(url).func.view_class, ProductItemCreateView)

    def test_list_view_url_is_resolved(self):
        """
        Tester que l'URL de la liste de ProductItem renvoie la bonne vue
        """
        url = reverse('item-list')
        self.assertEqual(resolve(url).func.view_class, ProductItemListView)

    def test_detail_view_url_is_resolved(self):
        """
        Tester que l'URL de détail de ProductItem renvoie la bonne vue
        """
        url = reverse('item-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductItemDetailView)

    def test_update_view_url_is_resolved(self):
        """
        Tester que l'URL de mise à jour de ProductItem renvoie la bonne vue
        """
        url = reverse('item-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductItemUpdateView)

    def test_delete_view_url_is_resolved(self):
        """
        Tester que l'URL de suppression de ProductItem renvoie la bonne vue
        """
        url = reverse('item-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductItemDeleteView)