from rest_framework import serializers
from .models import (
    User, Administrateur, Vendeur,
    Fournisseur, Produit,
    Commande, LigneCommande,
    Vente, LigneVente
)


# ─────────────────────────────────────────
#  Utilisateurs
# ─────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class AdministrateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        admin = Administrateur(**validated_data)
        admin.set_password(password)
        admin.is_staff = True
        admin.save()
        return admin


class VendeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendeur
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        vendeur = Vendeur(**validated_data)
        vendeur.set_password(password)
        vendeur.save()
        return vendeur


# ─────────────────────────────────────────
#  Fournisseur
# ─────────────────────────────────────────

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'


# ─────────────────────────────────────────
#  Produit
# ─────────────────────────────────────────

class ProduitSerializer(serializers.ModelSerializer):
    # Lecture : objets imbriqués
    fournisseur         = FournisseurSerializer(read_only=True)
    administrateur      = AdministrateurSerializer(read_only=True)
    en_alerte           = serializers.SerializerMethodField()

    # Écriture : IDs uniquement
    fournisseur_id      = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    administrateur_id   = serializers.IntegerField(write_only=True)

    class Meta:
        model = Produit
        fields = [
            'id', 'libelle', 'prix_unitaire', 'quantite', 'seuil_alert',
            'fournisseur', 'fournisseur_id',
            'administrateur', 'administrateur_id',
            'en_alerte',
        ]

    def get_en_alerte(self, obj):
        return obj.verifier_seuil()


# ─────────────────────────────────────────
#  Commande
# ─────────────────────────────────────────

class LigneCommandeSerializer(serializers.ModelSerializer):
    produit     = ProduitSerializer(read_only=True)
    produit_id  = serializers.IntegerField(write_only=True)

    class Meta:
        model = LigneCommande
        fields = ['id', 'produit', 'produit_id', 'quantite', 'prix']


class CommandeSerializer(serializers.ModelSerializer):
    # Lecture
    administrateur  = AdministrateurSerializer(read_only=True)
    fournisseur     = FournisseurSerializer(read_only=True)
    lignes          = LigneCommandeSerializer(
                        source='lignecommande_set', many=True, read_only=True
                      )

    # Écriture
    administrateur_id   = serializers.IntegerField(write_only=True)
    fournisseur_id      = serializers.IntegerField(write_only=True)

    class Meta:
        model = Commande
        fields = [
            'id', 'contact', 'date_commande',
            'administrateur', 'administrateur_id',
            'fournisseur', 'fournisseur_id',
            'lignes',
        ]


# ─────────────────────────────────────────
#  Vente
# ─────────────────────────────────────────

class LigneVenteSerializer(serializers.ModelSerializer):
    produit     = ProduitSerializer(read_only=True)
    produit_id  = serializers.IntegerField(write_only=True)

    class Meta:
        model = LigneVente
        fields = ['id', 'produit', 'produit_id', 'quantite', 'prix']


class VenteSerializer(serializers.ModelSerializer):
    # Lecture
    vendeur     = VendeurSerializer(read_only=True)
    lignes      = LigneVenteSerializer(
                    source='lignevente_set', many=True, read_only=True
                  )

    # Écriture
    vendeur_id  = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    lignes_write = LigneVenteSerializer(many=True, write_only=True)

    class Meta:
        model = Vente
        fields = [
            'id', 'data', 'montant_total',
            'vendeur', 'vendeur_id',
            'lignes',
            'lignes_write',
        ]

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes_write')
        vente = Vente.objects.create(**validated_data)
        for ligne in lignes_data:
            LigneVente.objects.create(
                vente=vente,
                produit_id=ligne['produit_id'],
                quantite=ligne['quantite'],
                prix=ligne['prix']
            )
        return vente