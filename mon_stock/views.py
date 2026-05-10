from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from .models import (
    Administrateur, Vendeur,
    Fournisseur, Produit,
    Commande, LigneCommande,
    Vente
)
from .serializers import (
    AdministrateurSerializer, VendeurSerializer,
    FournisseurSerializer, ProduitSerializer,
    CommandeSerializer, LigneCommandeSerializer,
    VenteSerializer
)
from .permissions import IsAdminAuthenticated, IsVendeurAuthenticated, IsAdminOrVendeur


# ─────────────────────────────────────────
#  Administrateur
# ─────────────────────────────────────────

class AdministrateurViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les administrateurs.
    Réservé aux administrateurs authentifiés.
    """
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurSerializer
    permission_classes = [IsAdminAuthenticated]


# ─────────────────────────────────────────
#  Vendeur
# ─────────────────────────────────────────

class VendeurViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les vendeurs.
    Réservé aux administrateurs.
    """
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer
    permission_classes = [IsAdminAuthenticated]


# ─────────────────────────────────────────
#  Fournisseur
# ─────────────────────────────────────────

class FournisseurViewSet(viewsets.ModelViewSet):
    """
    Lecture : Admin + Vendeur
    Écriture : Admin uniquement
    """
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAdminOrVendeur()]
        return [IsAdminAuthenticated()]


# ─────────────────────────────────────────
#  Produit
# ─────────────────────────────────────────

class ProduitViewSet(viewsets.ModelViewSet):
    """
    Lecture : Admin + Vendeur
    Écriture : Admin uniquement

    Actions custom :
      - GET /produits/alertes/  → produits sous le seuil d'alerte
    """
    queryset = Produit.objects.select_related('fournisseur', 'administrateur')
    serializer_class = ProduitSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAdminOrVendeur()]
        return [IsAdminAuthenticated()]

    @action(detail=False, methods=['get'], url_path='alertes',
            permission_classes=[IsAdminOrVendeur])
    def alertes(self, request):
        """Retourne les produits dont la quantité est <= seuil_alert."""
        produits = [p for p in self.get_queryset() if p.verifier_seuil()]
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # L'administrateur connecté est automatiquement assigné
        admin = Administrateur.objects.get(pk=self.request.user.pk)
        serializer.save(administrateur=admin)


# ─────────────────────────────────────────
#  Commande
# ─────────────────────────────────────────

class CommandeViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les commandes.
    Réservé aux administrateurs.
    """
    queryset = Commande.objects.select_related('administrateur', 'fournisseur')
    serializer_class = CommandeSerializer
    permission_classes = [IsAdminAuthenticated]

    def perform_create(self, serializer):
        admin = Administrateur.objects.get(pk=self.request.user.pk)
        serializer.save(administrateur=admin)


class LigneCommandeViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les lignes de commande.
    Réservé aux administrateurs.
    """
    queryset = LigneCommande.objects.select_related('commande', 'produit')
    serializer_class = LigneCommandeSerializer
    permission_classes = [IsAdminAuthenticated]


# ─────────────────────────────────────────
#  Vente
# ─────────────────────────────────────────

class VenteViewSet(viewsets.ModelViewSet):
    """
    Lecture : Admin + Vendeur
    Écriture : Vendeur (valide le paiement) + Admin

    Un vendeur ne voit que ses propres ventes.
    Un administrateur voit toutes les ventes.
    """
    serializer_class = VenteSerializer

    def get_permissions(self):
        return [IsAdminOrVendeur()]

    def get_queryset(self):
        user = self.request.user

        if Administrateur.objects.filter(pk=user.pk).exists():
            return Vente.objects.select_related('vendeur', 'produit').all()

        # Le vendeur ne voit que ses ventes
        return Vente.objects.select_related('vendeur', 'produit').filter(vendeur__pk=user.pk)

    def perform_create(self, serializer):
        """Assigne automatiquement le vendeur connecté et calcule le montant total."""
        produit_id      = serializer.validated_data.get('produit_id')
        quantite_vendue = serializer.validated_data.get('quantite_vendue', 1)

        produit = Produit.objects.get(pk=produit_id)
        montant_total = produit.prix_unitaire * quantite_vendue

        # Mise à jour du stock
        produit.update_stock(-quantite_vendue)

        try:
            vendeur = Vendeur.objects.get(pk=self.request.user.pk)
        except Vendeur.DoesNotExist:
            vendeur = None

        serializer.save(vendeur=vendeur, montant_total=montant_total)