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
    path("attribut/<pk>/delete/",views.ProductAttributeDeleteView.as_view(), name="attribute-delete"),
    path("attributs/<pk>/update/",views.ProductAttributeUpdateView.as_view(), name="attribute-update"),
    path("attribut/add/",views.ProductAttributeCreateView.as_view(), name="attribut-add"),
    

    # Items : 
    path("items/",views.ProductItemListView.as_view(), name="item-list"),
    path("item/<pk>",views.ProductItemDetailView.as_view(), name="item-detail"),
    path("item/<pk>/delete/",views.ProductItemDeleteView.as_view(), name="item-delete"),
    path("item/<pk>/update/",views.ProductItemUpdateView.as_view(), name="item-update"),
    path("item/add/",views.ProductItemCreateView.as_view(), name="item-add"),

    # Support : 
    path("about",views.AboutView.as_view(), name='about-page'),
    path('contact/', views.ContactView, name='contact'),

    # Fournisseurs :
    path("providers",views.ProviderListView.as_view(), name="provider-list"),
    path("provider/<pk>",views.ProviderDetailView.as_view(), name="provider-detail"),
    path("provider/add/",views.ProviderCreateView.as_view(), name="provider-add"),
    path("provider/<pk>/update/",views.ProviderUpdateView.as_view(), name="provider-update"),
    path("provider/<pk>/delete/",views.ProviderDeleteView.as_view(), name="provider-delete"),

    # Prix fournisseurs :
    path("providerPrice/<pk>/update/",views.ProviderProductPriceUpdateView.as_view(), name="providerPrice-update"),
    path("providerPrice/<pk>/delete/",views.ProviderProductPriceDeleteView.as_view(), name="providerPrice-delete"),
    path("providerPrice/<int:provider_id>/add/",views.ProviderProductPriceCreateView.as_view(), name="providerPrice-add"),

    # Commandes :
    path("orders/<int:provider_id>/add",views.OrderCreateView.as_view(), name="order-add"),
    path("orders",views.OrderListView.as_view(), name="order-list"),
    path("order/<pk>",views.OrderDetailView.as_view(), name="order-detail"),
    path("order/<pk>/delete/",views.OrderDeleteView.as_view(), name="order-delete"),

]