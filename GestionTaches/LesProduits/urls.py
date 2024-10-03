from django.urls import path

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("home/<name>", views.HomeParamView.as_view(), name="index"),
    path("home/", views.home, name="home"),
    path("products", views.ProductListView.as_view(), name="product-list"),
    path("home2",TemplateView.as_view(template_name="home.html")),
    path("home3",views.HomeView.as_view()),
    path("about",views.AboutView.as_view()),
    path("product/<pk>",views.ProductDetailView.as_view(), name="product-detail"),
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path('contact/', views.ContactView, name='contact'),
    path("products/add/",views.ProductCreateView.as_view(), name="product-add"),
    path("products/<pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<pk>/delete/",views.ProductDeleteView.as_view(), name="product-delete"),
    path("attributs/",views.ProductAttributeListView.as_view(), name="attribut-list"),
    path("attribut/<pk>",views.ProductAttributeDetailView.as_view(), name="attribute-detail"),
    path("items/",views.ProductItemListView.as_view(), name="item-list"),
]