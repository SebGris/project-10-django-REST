from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec gestion RGPD et âge
    """
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(15)],
        null=True,
        blank=True,
        help_text="L'utilisateur doit avoir au moins 15 ans (RGPD)"
    )
    can_be_contacted = models.BooleanField(
        default=False,
        help_text="L'utilisateur peut-il être contacté ?"
    )
    can_data_be_shared = models.BooleanField(
        default=False,
        help_text="Les données de l'utilisateur peuvent-elles être partagées ?"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
