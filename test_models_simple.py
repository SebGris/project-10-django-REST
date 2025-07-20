# -*- coding: utf-8 -*-
"""
Script de test simplifie pour valider les modeles Project et Contributor
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

from users.models import User
from issues.models import Project, Contributor


def test_models():
    """Test des modeles Project et Contributor - Version simplifiee"""
    print("Test des modeles Project et Contributor")
    print("=" * 50)
    
    try:
        # Nettoyage initial
        User.objects.filter(username__in=['author_test', 'contributor_test']).delete()
        
        # 1. Creation des utilisateurs
        print("\n1. Creation des utilisateurs de test...")
        author = User.objects.create_user(
            username='author_test',
            email='author@test.com',
            password='TestPass123!',
            age=25,
            can_be_contacted=True,
            can_data_be_shared=False
        )
        
        contributor = User.objects.create_user(
            username='contributor_test',
            email='contributor@test.com',
            password='TestPass123!',
            age=30,
            can_be_contacted=True,
            can_data_be_shared=True
        )
        print("   SUCCES - Utilisateurs crees")
        
        # 2. Creation d'un projet
        print("\n2. Creation d'un projet...")
        project = Project.objects.create(
            name="Test Project Model",
            description="Projet de test pour valider le modele",
            type="back-end",
            author=author
        )
        print(f"   SUCCES - Projet cree (ID: {project.id})")
        
        # 3. Test des methodes utilitaires
        print("\n3. Test des methodes utilitaires...")
        print(f"   - Auteur du projet: {project.author.username}")
        print(f"   - Type de projet: {project.type}")
        print(f"   - Date de creation: {project.created_time.strftime('%Y-%m-%d')}")
        
        # 4. Ajout d'un contributeur
        print("\n4. Ajout d'un contributeur...")
        contrib = Contributor.objects.create(
            user=contributor,
            project=project,
            role="contributor"
        )
        print(f"   SUCCES - Contributeur ajoute (Role: {contrib.role})")
        
        # 5. Liste des contributeurs
        print("\n5. Verification des contributeurs...")
        contributors = Contributor.objects.filter(project=project)
        print(f"   - Nombre de contributeurs: {contributors.count()}")
        for c in contributors:
            print(f"   - {c.user.username} ({c.role})")
        
        # 6. Nettoyage
        print("\n6. Nettoyage des donnees de test...")
        User.objects.filter(username__in=['author_test', 'contributor_test']).delete()
        print("   SUCCES - Nettoyage termine")
        
        print("\n" + "="*50)
        print("RESULTAT: TOUS LES TESTS REUSSIS")
        return True
        
    except Exception as e:
        print(f"\nERREUR: {e}")
        return False


if __name__ == "__main__":
    success = test_models()
    if success:
        print("EXIT CODE: 0 (Succes)")
    else:
        print("EXIT CODE: 1 (Echec)")
        exit(1)
