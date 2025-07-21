#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test simple d'un script pour déboguer les problèmes
"""
import os
import sys
import django

def test_single_script():
    """Test d'un seul script pour déboguer"""
    print("=== TEST SIMPLE D'UN SCRIPT ===")
    
    try:
        # Configuration Django
        print("1. Configuration Django...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
        django.setup()
        print("   [OK] Django configuré")
        
        # Import des modèles
        print("2. Import des modèles...")
        from users.models import User
        from issues.models import Project, Contributor
        print("   [OK] Modèles importés")
        
        # Test de création basique
        print("3. Test de création d'utilisateur...")
        
        # Nettoyer d'abord (au cas où)
        User.objects.filter(username__startswith='test_').delete()
        Project.objects.filter(name__startswith='Test Project').delete()
        
        # Créer utilisateur test
        user = User.objects.create_user(
            username='test_user_simple',
            email='test@example.com',
            password='TestPass123!',
            age=25,
            can_be_contacted=True,
            can_data_be_shared=False
        )
        print(f"   [OK] Utilisateur créé: {user.username}")
        
        # Créer projet test
        project = Project.objects.create(
            name='Test Project Simple',
            description='Projet de test simple',
            type='back_end',
            author=user
        )
        print(f"   [OK] Projet créé: {project.name}")
        
        # Vérifier que l'auteur est automatiquement contributeur
        is_contributor = project.contributors.filter(user=user).exists()
        print(f"   [OK] Auteur est contributeur: {is_contributor}")
        
        # Nettoyer
        project.delete()
        user.delete()
        print("   [OK] Nettoyage effectué")
        
        print("\n=== TEST SIMPLE RÉUSSI ===")
        return True
        
    except Exception as e:
        print(f"   [ERREUR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_single_script()
    sys.exit(0 if success else 1)
