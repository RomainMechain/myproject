from django.test import SimpleTestCase
from django.urls import reverse, resolve
from LesProduits.views import ProductCreateView, ProductListView

class ProductTestUrls(SimpleTestCase):
    def test_create_view_url_is_resolved(self):
        """
        Tester que l'URL de la création de Product renvoie la bonne vue
        """
        url = reverse('product-add')
        self.assertEqual(resolve(url).func.view_class, ProductCreateView)

    def test_list_view_url_is_resolved(self):
        """
        Tester que l'URL de la liste de Product renvoie la bonne vue
        """
        url = reverse('product-list')
        self.assertEqual(resolve(url).func.view_class, ProductListView)