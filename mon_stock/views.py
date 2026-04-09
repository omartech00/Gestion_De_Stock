from django.shortcuts import render
from rest_framework import viewsets
from .models import Categorie, Fournisseur, Produit, Stock, Client, Commande, ArticleCommande
from .serializers import CategorieSerializer, FournisseurSerializer, ProduitSerializer, StockSerializer, ClientSerializer, CommandeSerializer, ArticleCommandeSerializer

# Create your views here.

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

class ArticleCommandeViewSet(viewsets.ModelViewSet):
    queryset = ArticleCommande.objects.all()
    serializer_class = ArticleCommandeSerializer
