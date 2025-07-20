# -*- coding: utf-8 -*-
"""
Script de test simplifie pour les modeles Issue et Comment
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

from users.models import User
from issues.models import Project, Contributor, Issue, Comment


def test_issue_comment_models():
    """Test des modeles Issue et Comment - Version simplifiee"""
    print("Test des modeles Issue et Comment")
    print("=" * 40)
    
    try:
        # Nettoyage initial
        User.objects.filter(username__startswith='test_issue').delete()
        
        # 1. Creation des utilisateurs de test
        print("\n1. Creation des utilisateurs...")
        author = User.objects.create_user(
            username='test_issue_author',
            email='author@issue.com',
            password='TestPass123!',
            age=25,
            can_be_contacted=True,
            can_data_be_shared=False
        )
        print("   SUCCES - Utilisateur auteur cree")
        
        # 2. Creation d'un projet
        print("\n2. Creation du projet...")
        project = Project.objects.create(
            name="Test Project Issues",
            description="Projet de test pour les issues",
            type="back-end",
            author=author
        )
        print(f"   SUCCES - Projet cree (ID: {project.id})")
        
        # 3. Creation d'une issue
        print("\n3. Creation d'une issue...")
        issue = Issue.objects.create(
            name="Bug de test",
            description="Description du bug de test",
            priority="HIGH",
            tag="BUG",
            status="To Do",
            project=project,
            author=author,
            assigned_to=author
        )
        print(f"   SUCCES - Issue creee (ID: {issue.id})")
        
        # 4. Creation d'un commentaire
        print("\n4. Creation d'un commentaire...")
        comment = Comment.objects.create(
            description="Commentaire de test pour l'issue",
            author=author,
            issue=issue
        )
        print(f"   SUCCES - Commentaire cree (ID: {comment.id})")
        
        # 5. Verification des relations
        print("\n5. Verification des relations...")
        print(f"   - Issue appartient au projet: {issue.project.name}")
        print(f"   - Issue assignee a: {issue.assigned_to.username}")
        print(f"   - Commentaire lie a l'issue: {comment.issue.name}")
        print(f"   - Auteur du commentaire: {comment.author.username}")
        
        # 6. Test des choix
        print("\n6. Verification des choix...")
        print(f"   - Priorite: {issue.priority}")
        print(f"   - Tag: {issue.tag}")
        print(f"   - Status: {issue.status}")
        
        # 7. Nettoyage
        print("\n7. Nettoyage...")
        User.objects.filter(username__startswith='test_issue').delete()
        print("   SUCCES - Nettoyage termine")
        
        print("\n" + "="*40)
        print("RESULTAT: TOUS LES TESTS ISSUE/COMMENT REUSSIS")
        return True
        
    except Exception as e:
        print(f"\nERREUR: {e}")
        return False


if __name__ == "__main__":
    success = test_issue_comment_models()
    if success:
        print("EXIT CODE: 0 (Succes)")
    else:
        print("EXIT CODE: 1 (Echec)")
        exit(1)
