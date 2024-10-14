from django.urls import path

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    #path("home/<name>", views.HomeParamView.as_view(), name="index"),
    #path("home/", views.home, name="home"),
    path("home",views.HomeView.as_view(), name="home"),

    # Les produits : 
    path("products", views.ProductListView.as_view(), name="product-list"),
    path("product/<pk>",views.ProductDetailView.as_view(), name="product-detail"),
    path("products/<pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<pk>/delete/",views.ProductDeleteView.as_view(), name="product-delete"),
    path("products/add/",views.ProductCreateView.as_view(), name="product-add"),

    # Authentification : 
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),

    # Attributs :
    path("attributs/",views.ProductAttributeListView.as_view(), name="attribut-list"),
    path("attribut/<pk>",views.ProductAttributeDetailView.as_view(), name="attribute-detail"),

    # Items : 
    path("items/",views.ProductItemListView.as_view(), name="item-list"),
    path("item/<pk>",views.ProductItemDetailView.as_view(), name="item-detail"),
    path("item/<pk>/delete/",views.ProductItemDeleteView.as_view(), name="item-delete"),
    path("item/<pk>/update/",views.ProductItemUpdateView.as_view(), name="item-update"),
    path("item/add/",views.ProductItemCreateView.as_view(), name="item-add"),

    # Support : 
    path("about",views.AboutView.as_view(), name='about-page'),
    path('contact/', views.ContactView, name='contact'),

]