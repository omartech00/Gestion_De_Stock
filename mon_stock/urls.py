from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# Utilisateurs
router.register(r'administrateurs',     views.AdministrateurViewSet,     basename='administrateur')
router.register(r'vendeurs',            views.VendeurViewSet,            basename='vendeur')

# Catalogue & stock
router.register(r'fournisseurs',        views.FournisseurViewSet,        basename='fournisseur')
router.register(r'produits',            views.ProduitViewSet,            basename='produit')

# Commandes
router.register(r'commandes',           views.CommandeViewSet,           basename='commande')
router.register(r'lignes-commande',     views.LigneCommandeViewSet,      basename='ligne-commande')

# Ventes
router.register(r'ventes',             views.VenteViewSet,              basename='vente')
router.register(r'lignes-vente',       views.LigneVenteViewSet,         basename='ligne-vente')

urlpatterns = [
    path('', include(router.urls)),
]