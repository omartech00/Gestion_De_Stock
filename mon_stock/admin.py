from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Administrateur, Vendeur,
    Fournisseur, Produit,
    Commande, LigneCommande,
    Vente, LigneVente
)


# ─── Utilisateurs ───────────────────────

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Administrateur)
class AdministrateurAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


@admin.register(Vendeur)
class VendeurAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


# ─── Fournisseur ────────────────────────

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display  = ('societe', 'contact')
    search_fields = ('societe',)


# ─── Produit ────────────────────────────

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display  = ('libelle', 'prix_unitaire', 'quantite', 'seuil_alert', 'fournisseur', 'administrateur')
    list_filter   = ('fournisseur', 'administrateur')
    search_fields = ('libelle',)


# ─── Commande ───────────────────────────

class LigneCommandeInline(admin.TabularInline):
    model  = LigneCommande
    extra  = 1


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display  = ('id', 'administrateur', 'fournisseur', 'date_commande', 'contact')
    list_filter   = ('fournisseur', 'administrateur')
    inlines       = [LigneCommandeInline]


@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display  = ('commande', 'produit', 'quantite', 'prix')


# ─── Vente ──────────────────────────────

class LigneVenteInline(admin.TabularInline):
    model  = LigneVente
    extra  = 1


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display  = ('id', 'vendeur', 'montant_total', 'data')
    list_filter   = ('vendeur', 'data')
    search_fields = ('vendeur__username',)
    inlines       = [LigneVenteInline]


@admin.register(LigneVente)
class LigneVenteAdmin(admin.ModelAdmin):
    list_display  = ('vente', 'produit', 'quantite', 'prix')
    