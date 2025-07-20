#!/usr/bin/env python3
"""
Script pour créer un superutilisateur avec tous les champs requis
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """Créer un superutilisateur avec les champs obligatoires"""
    print("🔐 Création d'un superutilisateur SoftDesk")
    print("=" * 50)
    
    # Vérifier si l'utilisateur admin existe déjà
    if User.objects.filter(username='admin').exists():
        print("⚠️  Un utilisateur 'admin' existe déjà.")
        response = input("Voulez-vous le supprimer et en créer un nouveau ? [y/N]: ")
        if response.lower() == 'y':
            User.objects.filter(username='admin').delete()
            print("✅ Ancien utilisateur 'admin' supprimé")
        else:
            print("❌ Annulation de la création")
            return
    
    try:
        # Créer le superutilisateur avec tous les champs requis
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@softdesk.local',
            password='SoftDesk2025!',
            first_name='Admin',
            last_name='SoftDesk',
            age=30,  # Âge obligatoire conforme RGPD
            can_be_contacted=False,
            can_data_be_shared=False
        )
        
        print("✅ Superutilisateur créé avec succès !")
        print(f"   👤 Username: {superuser.username}")
        print(f"   📧 Email: {superuser.email}")
        print(f"   🎂 Âge: {superuser.age} ans")
        print(f"   🔑 Password: SoftDesk2025!")
        print(f"   🛡️  Superuser: {superuser.is_superuser}")
        print(f"   📊 Staff: {superuser.is_staff}")
        
        print("\n🎯 Vous pouvez maintenant :")
        print("   1. Démarrer le serveur : poetry run python manage.py runserver")
        print("   2. Accéder à l'admin : http://127.0.0.1:8000/admin/")
        print("   3. Tester l'API : http://127.0.0.1:8000/api/")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création : {e}")

if __name__ == "__main__":
    create_superuser()
