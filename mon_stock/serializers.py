from rest_framework import serializers
from .models import Categorie, Fournisseur, Produit, Stock, Client, Commande, ArticleCommande

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    fournisseur = FournisseurSerializer(read_only=True)
    categorie_id = serializers.IntegerField(write_only=True)
    fournisseur_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Produit
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    produit_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ArticleCommandeSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    produit_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ArticleCommande
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True)
    articles = ArticleCommandeSerializer(source='articlecommande_set', many=True, read_only=True)

    class Meta:
        model = Commande
        fields = '__all__'