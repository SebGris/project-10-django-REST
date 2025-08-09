from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec gestion RGPD et âge
    """
    age = models.IntegerField(
        verbose_name="Âge",
        validators=[
            MinValueValidator(15, message="L'âge minimum requis est de 15 ans.")
        ],
        help_text="Doit avoir au moins 15 ans (RGPD)"
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

    def save(self, *args, **kwargs):
        """Override save pour déclencher la validation RGPD avant sauvegarde"""
        self.full_clean()  # Déclenche la validation des champs
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
