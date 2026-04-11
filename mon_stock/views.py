from django.shortcuts import render
from rest_framework import viewsets
from .models import Categorie, Fournisseur, Produit, Stock, Client, Commande, ArticleCommande
from .serializers import CategorieSerializer, FournisseurSerializer, ProduitSerializer, StockSerializer, ClientSerializer, CommandeSerializer, ArticleCommandeSerializer
from rest_framework.permissions import IsAuthenticated
from mon_stock.permissions import IsAdminAuthenticated

# Create your views here.

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAdminAuthenticated]

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    permission_classes = [IsAdminAuthenticated]

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAdminAuthenticated]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminAuthenticated]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]

class ArticleCommandeViewSet(viewsets.ModelViewSet):
    queryset = ArticleCommande.objects.all()
    serializer_class = ArticleCommandeSerializer
    permission_classes = [IsAuthenticated]