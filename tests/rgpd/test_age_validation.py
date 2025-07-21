"""
Test de validation RGPD avec le champ age
"""
import os
import django

# Configuration Django (DOIT être fait AVANT d'importer les modèles)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

# MAINTENANT on peut importer les modèles Django
from users.models import User  # noqa: E402
from django.core.exceptions import ValidationError  # noqa: E402

def test_rgpd_age_validation():
    """Test de la validation d'âge RGPD"""
    print("🔒 Test de conformité RGPD - Validation d'âge")
    print("=" * 50)
    
    # Test 1: Utilisateur trop jeune (moins de 15 ans)
    print("\n❌ Test 1: Utilisateur de 14 ans (refusé)")
    try:
        user_young = User(
            username='user_14',
            email='young@test.com',
            password='testpass123',  # Ajout du password obligatoire
            age=14
        )
        user_young.full_clean()  # Déclenche la validation
        print("   ⚠️  PROBLÈME: L'utilisateur de 14 ans a été accepté!")
    except ValidationError as e:
        print("   ✅ Correct: Utilisateur de 14 ans refusé")
        print(f"   📝 Message d'erreur: {e}")
    
    # Test 2: Utilisateur âge limite (15 ans)
    print("\n✅ Test 2: Utilisateur de 15 ans (accepté)")
    try:
        user_limit = User(
            username='user_15',
            email='limit@test.com',
            password='testpass123',  # Ajout du password obligatoire
            age=15
        )
        user_limit.full_clean()  # Déclenche la validation
        print("   ✅ Correct: Utilisateur de 15 ans accepté")
    except ValidationError as e:
        print(f"   ❌ PROBLÈME: Utilisateur de 15 ans refusé: {e}")
    
    # Test 3: Utilisateur adulte (25 ans)
    print("\n✅ Test 3: Utilisateur de 25 ans (accepté)")
    try:
        user_adult = User(
            username='user_25',
            email='adult@test.com',
            password='testpass123',  # Ajout du password obligatoire
            age=25
        )
        user_adult.full_clean()  # Déclenche la validation
        print("   ✅ Correct: Utilisateur de 25 ans accepté")
    except ValidationError as e:
        print(f"   ❌ PROBLÈME: Utilisateur de 25 ans refusé: {e}")
    
    # Test 4: Âge non renseigné (maintenant obligatoire)
    print("\n❌ Test 4: Âge non renseigné (obligatoire pour RGPD)")
    try:
        user_no_age = User(
            username='user_no_age',
            email='noage@test.com',
            password='testpass123'
            # age non défini - cela devrait maintenant échouer
        )
        user_no_age.full_clean()  # Déclenche la validation
        print("   ⚠️  PROBLÈME: Utilisateur sans âge accepté!")
    except ValidationError as e:
        print("   ✅ Correct: Utilisateur sans âge refusé (champ obligatoire)")
        print(f"   📝 Message d'erreur: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Résumé des tests RGPD:")
    print("   - Les utilisateurs < 15 ans doivent être refusés")
    print("   - Les utilisateurs ≥ 15 ans doivent être acceptés") 
    print("   - L'âge est OBLIGATOIRE pour vérifier la conformité RGPD")
    print("=" * 50)

def test_user_creation_with_save():
    """Test de création d'utilisateur avec save()"""
    print("\n💾 Test de création d'utilisateur avec save()")
    print("-" * 40)
    
    # Nettoyage préalable
    User.objects.filter(username__in=['valid_user', 'invalid_user']).delete()
    
    # Test utilisateur valide
    try:
        valid_user = User.objects.create_user(
            username='valid_user',
            email='valid@test.com',
            password='testpass123',
            age=20
        )
        print("✅ Utilisateur valide créé avec succès")
        valid_user.delete()  # Nettoyage
    except Exception as e:
        print(f"❌ Erreur création utilisateur valide: {e}")
    
    # Test utilisateur invalide
    try:
        invalid_user = User(
            username='invalid_user',
            email='invalid@test.com',
            age=10  # Trop jeune
        )
        invalid_user.set_password('testpass123')  # Définir le password correctement
        invalid_user.save()  # Cela devrait maintenant déclencher la validation
        print("⚠️  PROBLÈME: Utilisateur invalide créé!")
        invalid_user.delete()  # Nettoyage si jamais
    except Exception as e:
        print("✅ Correct: Utilisateur invalide refusé")
        print(f"   📝 Erreur: {e}")

if __name__ == "__main__":
    test_rgpd_age_validation()
    test_user_creation_with_save()
