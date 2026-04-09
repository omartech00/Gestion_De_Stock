from django.contrib import admin
from .models import Categorie, Fournisseur, Produit, Stock, Client, Commande, ArticleCommande

# Register your models here.

admin.site.register(Categorie)
admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(Stock)
admin.site.register(Client)
admin.site.register(Commande)
admin.site.register(ArticleCommande)
