#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour identifier les problèmes de configuration
"""
import os
import sys
import subprocess

def check_project_structure():
    """Vérifier la structure du projet"""
    print("🔍 DIAGNOSTIC DE LA STRUCTURE DU PROJET")
    print("=" * 50)
    
    required_files = [
        'manage.py',
        'pyproject.toml', 
        'softdesk_support/__init__.py',
        'softdesk_support/settings.py',
        'users/__init__.py',
        'users/models.py',
        'issues/__init__.py', 
        'issues/models.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_python_path():
    """Vérifier le PYTHONPATH et les modules"""
    print("\n🐍 DIAGNOSTIC PYTHON")
    print("=" * 50)
    
    print(f"Répertoire courant: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Tester l'import de Django
    try:
        import django
        print(f"✅ Django version: {django.get_version()}")
    except ImportError as e:
        print(f"❌ Django non trouvé: {e}")
        return False
    
    return True

def check_django_settings():
    """Vérifier la configuration Django"""
    print("\n⚙️  DIAGNOSTIC DJANGO")
    print("=" * 50)
    
    try:
        # Tester l'import des settings
        sys.path.insert(0, os.getcwd())
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        print(f"✅ Settings module: {settings.SETTINGS_MODULE}")
        print(f"✅ Debug mode: {settings.DEBUG}")
        print(f"✅ Installed apps: {len(settings.INSTALLED_APPS)} apps")
        
        # Tester l'import des models
        from users.models import User
        print("✅ users.models.User importé")
        
        from issues.models import Project, Contributor, Issue, Comment
        print("✅ issues.models importés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        print(f"Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def check_database():
    """Vérifier la base de données"""
    print("\n💾 DIAGNOSTIC BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        result = subprocess.run(
            'poetry run python manage.py check',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Vérification Django réussie")
            return True
        else:
            print(f"❌ Erreur Django check: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur subprocess: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🚨 DIAGNOSTIC COMPLET DU PROJET SOFTDESK")
    print("=" * 60)
    
    checks = [
        ("Structure du projet", check_project_structure),
        ("Configuration Python", check_python_path),
        ("Configuration Django", check_django_settings),
        ("Base de données", check_database)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erreur lors du check {name}: {e}")
            results.append((name, False))
    
    # Résumé
    print("\n📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    for name, success in results:
        status = "✅ OK" if success else "❌ ÉCHEC"
        print(f"{status} {name}")
    
    successful_checks = sum(1 for _, success in results if success)
    total_checks = len(results)
    
    print(f"\nRésultat: {successful_checks}/{total_checks} vérifications réussies")
    
    if successful_checks == total_checks:
        print("🎉 Tous les diagnostics sont OK ! Le projet devrait fonctionner.")
    else:
        print("⚠️  Des problèmes ont été détectés. Consultez les détails ci-dessus.")
        
        # Suggestions de résolution
        print("\n💡 SUGGESTIONS DE RÉSOLUTION:")
        if not results[0][1]:  # Structure
            print("- Vérifiez que vous êtes dans le bon répertoire du projet")
        if not results[1][1]:  # Python
            print("- Installez les dépendances: poetry install")
        if not results[2][1]:  # Django
            print("- Vérifiez le fichier settings.py")
            print("- Exécutez: poetry run python manage.py check")
        if not results[3][1]:  # DB
            print("- Appliquez les migrations: poetry run python manage.py migrate")

if __name__ == "__main__":
    main()
