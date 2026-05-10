from django.contrib.auth.models import AbstractUser
from django.db import models


# ─────────────────────────────────────────
#  Utilisateurs (AbstractUser → héritage)
# ─────────────────────────────────────────

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='mon_stock_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='mon_stock_users',
        blank=True
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Administrateur(User):
    """
    Hérite de User.
    Peut ajouter des produits, gérer les utilisateurs, consulter le dashboard.
    """
    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"

    def __str__(self):
        return f"Admin : {self.username}"


class Vendeur(User):
    """
    Hérite de User.
    Peut valider des paiements/ventes.
    """
    class Meta:
        verbose_name = "Vendeur"
        verbose_name_plural = "Vendeurs"

    def __str__(self):
        return f"Vendeur : {self.username}"


# ─────────────────────────────────────────
#  Fournisseur
# ─────────────────────────────────────────

class Fournisseur(models.Model):
    societe  = models.CharField(max_length=200)
    contact  = models.CharField(max_length=200)

    def __str__(self):
        return self.societe

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"


# ─────────────────────────────────────────
#  Produit  (stock intégré dans le modèle)
# ─────────────────────────────────────────

class Produit(models.Model):
    libelle        = models.CharField(max_length=200)
    prix_unitaire  = models.FloatField()
    quantite       = models.IntegerField(default=0)
    seuil_alert    = models.IntegerField(default=0)

    # Géré par un Administrateur (1.1 → 1.n)
    administrateur = models.ForeignKey(
        Administrateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name="produits_geres"
    )

    # Livré par un Fournisseur via une Commande — relation directe optionnelle
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="produits"
    )

    def update_stock(self, quantite: int):
        """Ajoute ou retire de la quantité en stock."""
        self.quantite += quantite
        self.save()

    def verifier_seuil(self) -> bool:
        """Retourne True si le stock est en dessous du seuil d'alerte."""
        return self.quantite <= self.seuil_alert

    def get_infos(self) -> dict:
        return {
            "id": self.id,
            "libelle": self.libelle,
            "prix_unitaire": self.prix_unitaire,
            "quantite": self.quantite,
            "seuil_alert": self.seuil_alert,
        }

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


# ─────────────────────────────────────────
#  Commande  (effectuée par Administrateur,
#             concerne des Produits,
#             livrée par Fournisseur)
# ─────────────────────────────────────────

class Commande(models.Model):
    # Champs visibles sur le diagramme
    contact = models.CharField(max_length=200, blank=True)

    # Effectuée par un Administrateur (1 → 1.n)
    administrateur = models.ForeignKey(
        Administrateur,
        on_delete=models.CASCADE,
        related_name="commandes"
    )

    # Livrée par un Fournisseur (1 → 1.n)
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.CASCADE,
        related_name="commandes"
    )

    # Concerne plusieurs Produits (relation M2M avec quantité → table intermédiaire)
    produits = models.ManyToManyField(
        Produit,
        through="LigneCommande",
        related_name="commandes"
    )

    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.id} — {self.administrateur}"

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"


class LigneCommande(models.Model):
    """Table intermédiaire Commande ↔ Produit (quantité commandée, prix)."""
    commande  = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit   = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite  = models.IntegerField(default=1)
    prix      = models.FloatField()

    def __str__(self):
        return f"{self.quantite} × {self.produit.libelle}"

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"


# ─────────────────────────────────────────
#  Vente  (réalisée par un Vendeur,
#          porte sur un Produit)
# ─────────────────────────────────────────

class Vente(models.Model):
    data          = models.DateTimeField(auto_now_add=True)
    montant_total = models.FloatField(default=0)

    # Validée par un Vendeur (1 → 0..1)
    vendeur = models.ForeignKey(
        Vendeur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventes"
    )

    # Porte sur un Produit (0..1 → 1)
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name="ventes"
    )

    quantite_vendue = models.IntegerField(default=1)

    def generer_facture(self) -> str:
        """Retourne une représentation simple de la facture."""
        return (
            f"Facture Vente #{self.id}\n"
            f"Produit : {self.produit.libelle}\n"
            f"Quantité : {self.quantite_vendue}\n"
            f"Total : {self.montant_total} FCFA\n"
            f"Vendeur : {self.vendeur}\n"
            f"Date : {self.data}"
        )

    def __str__(self):
        return f"Vente #{self.id} — {self.produit.libelle}"

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"