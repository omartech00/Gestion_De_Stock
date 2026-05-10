from rest_framework.permissions import BasePermission
from .models import Administrateur, Vendeur


class IsAdminAuthenticated(BasePermission):
    """Accès réservé aux Administrateurs authentifiés."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return Administrateur.objects.filter(pk=request.user.pk).exists()


class IsVendeurAuthenticated(BasePermission):
    """Accès réservé aux Vendeurs authentifiés."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return Vendeur.objects.filter(pk=request.user.pk).exists()


class IsAdminOrVendeur(BasePermission):
    """Accès aux Administrateurs ET aux Vendeurs authentifiés."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        user_pk = request.user.pk
        return (
            Administrateur.objects.filter(pk=user_pk).exists()
            or Vendeur.objects.filter(pk=user_pk).exists()
        )