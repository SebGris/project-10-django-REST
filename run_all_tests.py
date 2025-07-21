#!/usr/bin/env python
"""
Script pour exécuter tous les tests SoftDesk dans l'ordre optimal
"""
import subprocess
import sys
import os

# Changer vers le répertoire du projet
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

def run_command(cmd, description):
    """Exécuter une commande et afficher le résultat"""
    print(f"\n🧪 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SUCCÈS")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ ÉCHEC")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

def main():
    print("🌟 EXÉCUTION COMPLÈTE DES TESTS SOFTDESK")
    print("=" * 60)
    
    success_count = 0
    total_tests = 0
    
    # Tests de modèles
    tests_models = [
        ("poetry run python tests/models/test_project_contributor.py", "Tests Project/Contributor détaillés"),
        ("poetry run python tests/models/test_project_contributor_simple.py", "Tests Project/Contributor simplifiés"),
        ("poetry run python tests/models/test_issue_comment.py", "Tests Issue/Comment détaillés"),
        ("poetry run python tests/models/test_issue_comment_simple.py", "Tests Issue/Comment simplifiés"),
    ]
    
    # Tests d'API
    tests_api = [
        ("poetry run python tests/api/test_basic_api.py", "Tests API de base"),
        ("poetry run python tests/api/test_complete_api.py", "Tests API complets"),
        ("poetry run python tests/api/test_issue_comment_api.py", "Tests API Issue/Comment"),
        ("poetry run python tests/api/test_nested_routes.py", "Tests routes imbriquées"),
    ]
    
    # Tests RGPD
    tests_rgpd = [
        ("poetry run python tests/rgpd/test_compliance.py", "Tests conformité RGPD"),
        ("poetry run python tests/rgpd/test_api.py", "Tests API RGPD"),
    ]
    
    # Tests de performance
    tests_performance = [
        ("poetry run python tests/performance/test_performance.py", "Tests de performance"),
    ]
    
    all_tests = [
        ("🏗️  TESTS DES MODÈLES", tests_models),
        ("🌐 TESTS DES API", tests_api), 
        ("🔒 TESTS RGPD", tests_rgpd),
        ("⚡ TESTS DE PERFORMANCE", tests_performance)
    ]
    
    for category, tests in all_tests:
        print(f"\n{category}")
        print("=" * 60)
        
        for cmd, description in tests:
            total_tests += 1
            if run_command(cmd, description):
                success_count += 1
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 60)
    print(f"✅ Tests réussis: {success_count}/{total_tests}")
    print(f"📈 Taux de réussite: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 TOUS LES TESTS SONT PASSÉS ! Votre API SoftDesk est robuste.")
        return 0
    else:
        print("⚠️  Certains tests ont échoué. Consultez les détails ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
