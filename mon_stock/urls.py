from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategorieViewSet)
router.register(r'fournisseurs', views.FournisseurViewSet)
router.register(r'produits', views.ProduitViewSet)
router.register(r'stocks', views.StockViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'commandes', views.CommandeViewSet)
router.register(r'articles-commande', views.ArticleCommandeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
