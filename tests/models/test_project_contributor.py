"""
Script de test pour valider notre modèle Project et Contributor amélioré
"""
import os
import django

# Configuration Django (DOIT être fait AVANT d'importer les modèles)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

# MAINTENANT on peut importer les modèles Django
from users.models import User  # noqa: E402
from issues.models import Project, Contributor  # noqa: E402


def test_project_contributor_logic():
    """Test des nouvelles fonctionnalités du modèle Project et Contributor"""
    print("🧪 Test des modèles Project et Contributor")
    print("=" * 50)
    
    # 1. Créer des utilisateurs de test
    print("\n1️⃣ Création des utilisateurs de test...")
    try:
        # Supprimer les utilisateurs existants pour un test propre
        User.objects.filter(username__in=['author_test', 'contributor_test']).delete()
        
        author = User.objects.create_user(
            username='author_test',
            email='author@test.com',
            password='testpass123',
            age=25
        )
        contributor = User.objects.create_user(
            username='contributor_test', 
            email='contributor@test.com',
            password='testpass123',
            age=30
        )
        print("✅ Utilisateurs créés avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la création des utilisateurs: {e}")
        return
    
    # 2. Créer un projet
    print("\n2️⃣ Création d'un projet...")
    try:
        # Supprimer les projets existants pour un test propre
        Project.objects.filter(name='Test Project').delete()
        
        project = Project.objects.create(
            name='Test Project',
            description='Projet de test pour valider nos modèles',
            type='back-end',
            author=author
        )
        print("✅ Projet créé avec succès")
        print(f"   Auteur: {project.author.username}")
        
        # Vérifier que l'auteur est automatiquement contributeur
        contributors_count = project.contributors.count()
        print(f"   Nombre de contributeurs après création: {contributors_count}")
        
        author_is_contributor = project.is_user_contributor(author)
        print(f"   L'auteur est-il contributeur? {author_is_contributor}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du projet: {e}")
        return
    
    # 3. Tester les méthodes utilitaires
    print("\n3️⃣ Test des méthodes utilitaires...")
    
    # Test can_user_modify
    can_author_modify = project.can_user_modify(author)
    can_contributor_modify = project.can_user_modify(contributor)
    print(f"   L'auteur peut-il modifier? {can_author_modify}")
    print(f"   Un autre utilisateur peut-il modifier? {can_contributor_modify}")
    
    # Test can_user_access
    can_author_access = project.can_user_access(author)
    can_contributor_access = project.can_user_access(contributor)
    print(f"   L'auteur peut-il accéder? {can_author_access}")
    print(f"   Un autre utilisateur peut-il accéder? {can_contributor_access}")
    
    # 4. Ajouter un contributeur
    print("\n4️⃣ Ajout d'un contributeur...")
    try:
        new_contributor = Contributor.objects.create(
            user=contributor,
            project=project
        )
        print("✅ Contributeur ajouté avec succès")
        print(f"   Contributeur: {new_contributor.user.username}")
        print(f"   Est-ce l'auteur? {new_contributor.is_author}")
        
        # Test après ajout du contributeur
        can_contributor_access_now = project.can_user_access(contributor)
        print(f"   Le contributeur peut-il maintenant accéder? {can_contributor_access_now}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout du contributeur: {e}")
    
    # 5. Lister tous les contributeurs
    print("\n5️⃣ Liste des contributeurs...")
    all_contributors = project.get_all_contributors()
    non_author_contributors = project.get_non_author_contributors()
    
    print(f"   Tous les contributeurs ({len(all_contributors)}):")
    for contrib in all_contributors:
        role = " (Auteur)" if contrib.is_author else ""
        print(f"     - {contrib.user.username}{role}")
    
    print(f"   Contributeurs non-auteurs ({len(non_author_contributors)}):")
    for contrib in non_author_contributors:
        print(f"     - {contrib.user.username}")
    
    print("\n🎉 Tests terminés avec succès!")
    print("=" * 50)
    
    # Nettoyage
    print("\n🧹 Nettoyage des données de test...")
    Project.objects.filter(name='Test Project').delete()
    User.objects.filter(username__in=['author_test', 'contributor_test']).delete()
    print("✅ Nettoyage terminé")

if __name__ == "__main__":
    test_project_contributor_logic()
