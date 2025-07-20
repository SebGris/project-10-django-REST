"""
Script de test pour valider les modèles Issue et Comment
"""
import os
import django

# Configuration Django (DOIT être fait AVANT d'importer les modèles)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

# MAINTENANT on peut importer les modèles Django
from users.models import User  # noqa: E402
from issues.models import Project, Contributor, Issue, Comment  # noqa: E402


def test_issue_comment_logic():
    """Test des modèles Issue et Comment"""
    print("🧪 Test des modèles Issue et Comment")
    print("=" * 50)
    
    # 1. Créer des utilisateurs de test
    print("\n1️⃣ Création des utilisateurs de test...")
    try:
        # Supprimer les utilisateurs existants pour un test propre
        User.objects.filter(username__in=['test_author', 'test_assignee', 'test_commenter']).delete()
        
        author = User.objects.create_user(
            username='test_author',
            email='author@test.com',
            password='testpass123',
            age=25
        )
        assignee = User.objects.create_user(
            username='test_assignee', 
            email='assignee@test.com',
            password='testpass123',
            age=30
        )
        commenter = User.objects.create_user(
            username='test_commenter', 
            email='commenter@test.com',
            password='testpass123',
            age=28
        )
        print("✅ Utilisateurs créés avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la création des utilisateurs: {e}")
        return
    
    # 2. Créer un projet
    print("\n2️⃣ Création d'un projet...")
    try:
        # Supprimer les projets existants pour un test propre
        Project.objects.filter(name='Test Project Issues').delete()
        
        project = Project.objects.create(
            name='Test Project Issues',
            description='Projet de test pour valider les issues et commentaires',
            type='back-end',
            author=author
        )
        print("✅ Projet créé avec succès")
        print(f"   Auteur: {project.author.username}")
        
        # Ajouter les autres utilisateurs comme contributeurs
        Contributor.objects.create(user=assignee, project=project)
        Contributor.objects.create(user=commenter, project=project)
        print(f"   Contributeurs ajoutés: {assignee.username}, {commenter.username}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du projet: {e}")
        return
    
    # 3. Créer des issues
    print("\n3️⃣ Création d'issues...")
    try:
        # Issue 1: Bug non assigné
        issue1 = Issue.objects.create(
            name='Bug de connexion',
            description='Les utilisateurs ne peuvent pas se connecter',
            priority='HIGH',
            tag='BUG',
            status='To Do',
            project=project,
            author=author
        )
        print(f"✅ Issue 1 créée: {issue1.name} (priorité: {issue1.priority}, statut: {issue1.status})")
        
        # Issue 2: Feature assignée
        issue2 = Issue.objects.create(
            name='Nouvelle fonctionnalité de recherche',
            description='Ajouter une barre de recherche avancée',
            priority='MEDIUM',
            tag='FEATURE',
            status='In Progress',
            project=project,
            author=author,
            assigned_to=assignee
        )
        print(f"✅ Issue 2 créée: {issue2.name} (assignée à: {issue2.assigned_to.username})")
        
        # Issue 3: Tâche créée par un contributeur
        issue3 = Issue.objects.create(
            name='Documentation API',
            description='Rédiger la documentation de l\'API',
            priority='LOW',
            tag='TASK',
            status='To Do',
            project=project,
            author=commenter
        )
        print(f"✅ Issue 3 créée: {issue3.name} (auteur: {issue3.author.username})")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des issues: {e}")
        return
    
    # 4. Créer des commentaires
    print("\n4️⃣ Création de commentaires...")
    try:
        # Commentaire 1: Sur l'issue 1
        comment1 = Comment.objects.create(
            description='J\'ai reproduit le bug, il semble lié au JWT',
            issue=issue1,
            author=assignee
        )
        print(f"✅ Commentaire 1 créé sur '{issue1.name}' par {comment1.author.username}")
        
        # Commentaire 2: Réponse de l'auteur
        comment2 = Comment.objects.create(
            description='Merci pour l\'info. Je vais investiguer le problème JWT.',
            issue=issue1,
            author=author
        )
        print(f"✅ Commentaire 2 créé sur '{issue1.name}' par {comment2.author.username}")
        
        # Commentaire 3: Sur l'issue 2
        comment3 = Comment.objects.create(
            description='J\'ai commencé le développement de la barre de recherche',
            issue=issue2,
            author=assignee
        )
        print(f"✅ Commentaire 3 créé sur '{issue2.name}' par {comment3.author.username}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des commentaires: {e}")
        return
    
    # 5. Tests des relations
    print("\n5️⃣ Test des relations...")
    
    # Issues du projet
    project_issues = project.issues.all()
    print(f"   Nombre d'issues dans le projet: {len(project_issues)}")
    for issue in project_issues:
        print(f"     - {issue.name} (auteur: {issue.author.username}, assigné: {issue.assigned_to.username if issue.assigned_to else 'Non assigné'})")
    
    # Commentaires de l'issue 1
    issue1_comments = issue1.comments.all()
    print(f"   Nombre de commentaires sur '{issue1.name}': {len(issue1_comments)}")
    for comment in issue1_comments:
        print(f"     - Par {comment.author.username}: {comment.description[:50]}...")
    
    # Issues assignées à assignee
    assigned_issues = assignee.assigned_issues.all()
    print(f"   Issues assignées à {assignee.username}: {len(assigned_issues)}")
    for issue in assigned_issues:
        print(f"     - {issue.name}")
    
    # Issues créées par chaque utilisateur
    print(f"   Issues créées par {author.username}: {author.authored_issues.count()}")
    print(f"   Issues créées par {commenter.username}: {commenter.authored_issues.count()}")
    
    # Commentaires créés par chaque utilisateur
    print(f"   Commentaires créés par {assignee.username}: {assignee.authored_comments.count()}")
    print(f"   Commentaires créés par {author.username}: {author.authored_comments.count()}")
    
    # 6. Test des méthodes __str__
    print("\n6️⃣ Test des méthodes __str__...")
    print(f"   Issue 1: {issue1}")
    print(f"   Comment 1: {comment1}")
    
    # 7. Test des IDs UUID pour les commentaires
    print("\n7️⃣ Test des IDs UUID...")
    print(f"   Comment 1 ID (UUID): {comment1.id}")
    print(f"   Comment 2 ID (UUID): {comment2.id}")
    print(f"   Type: {type(comment1.id)}")
    
    print("\n🎉 Tests terminés avec succès!")
    print("=" * 50)
    
    # Nettoyage
    print("\n🧹 Nettoyage des données de test...")
    Project.objects.filter(name='Test Project Issues').delete()
    User.objects.filter(username__in=['test_author', 'test_assignee', 'test_commenter']).delete()
    print("✅ Nettoyage terminé")


if __name__ == "__main__":
    test_issue_comment_logic()
