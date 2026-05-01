from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from django.contrib.auth.models import User
from .models import Categorie, Fournisseur, Produit, Stock, Client, Commande, ArticleCommande
from .serializers import CategorieSerializer, FournisseurSerializer, ProduitSerializer, StockSerializer, ClientSerializer, CommandeSerializer, ArticleCommandeSerializer
from mon_stock.permissions import IsAdminAuthenticated


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminAuthenticated()]


class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminAuthenticated()]


class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminAuthenticated()]


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminAuthenticated()]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class CommandeViewSet(viewsets.ModelViewSet):
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Commande.objects.all()

        return Commande.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleCommandeViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleCommandeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return ArticleCommande.objects.all()

        return ArticleCommande.objects.filter(commande__user=user)