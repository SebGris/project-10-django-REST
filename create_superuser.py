"""
Script pour créer un superutilisateur avec tous les champs requis
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

from issues.models import User

def create_superuser():
    """Créer un superutilisateur avec tous les champs requis"""
    
    # Vérifier si un superutilisateur existe déjà
    if User.objects.filter(is_superuser=True).exists():
        print("Un superutilisateur existe déjà.")
        return
    
    # Créer le superutilisateur
    user = User.objects.create_superuser(
        username='admin',
        email='admin@softdesk.local',
        password='SoftDesk2025!',
        age=25,  # Âge par défaut pour l'admin
        can_be_contacted=True,
        can_data_be_shared=False
    )
    
    print(f"Superutilisateur créé avec succès !")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Âge: {user.age}")

if __name__ == '__main__':
    create_superuser()
