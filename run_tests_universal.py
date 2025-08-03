#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script universel pour exécuter tous les tests SoftDesk
Version qui fonctionne avec Poetry et gère les problèmes Windows
"""
import subprocess
import sys
import os

def run_test_with_poetry(script_path, description):
    """Exécuter un script de test via Poetry avec gestion d'erreurs améliorée"""
    print(f"\n[TEST] {description}")
    print("=" * 60)
    
    try:
        # Commande Poetry avec le bon environnement
        cmd = f'poetry run python "{script_path}"'
        
        # Variables d'environnement pour éviter les problèmes d'encodage
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONPATH'] = os.getcwd()
        
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            env=env,
            cwd=os.getcwd(),
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("[OK] SUCCÈS")
            if result.stdout:
                # Nettoyer la sortie des emojis problématiques
                clean_output = clean_unicode_output(result.stdout)
                print(clean_output)
            return True
        else:
            print("[FAIL] ÉCHEC")
            if result.stderr:
                clean_error = clean_unicode_output(result.stderr)
                print("ERREURS:")
                print(clean_error)
            if result.stdout:
                clean_output = clean_unicode_output(result.stdout)
                print("SORTIE:")
                print(clean_output)
            return False
            
    except Exception as e:
        print(f"[ERROR] Erreur d'exécution: {e}")
        return False

def clean_unicode_output(text):
    """Nettoyer la sortie des caractères Unicode problématiques"""
    replacements = {
        '🧪': '[TEST]',
        '🚀': '[RUN]',
        '✅': '[OK]',
        '❌': '[FAIL]',
        '🔒': '[SECURITY]',
        '⚡': '[PERF]',
        '🌐': '[API]',
        '🏗️': '[BUILD]',
        '📊': '[STATS]',
        '🎉': '[SUCCESS]',
        '⚠️': '[WARNING]',
        '🔍': '[CHECK]',
        '📝': '[INFO]',
        '💾': '[DB]'
    }
    
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    
    return text

def check_poetry_env():
    """Vérifier que Poetry fonctionne correctement"""
    print("[INFO] Vérification de l'environnement Poetry...")
    
    try:
        result = subprocess.run(
            'poetry --version',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[OK] Poetry disponible: {result.stdout.strip()}")
            return True
        else:
            print("[FAIL] Poetry non disponible")
            return False
            
    except Exception as e:
        print(f"[ERROR] Erreur Poetry: {e}")
        return False

def check_django_via_poetry():
    """Vérifier Django via Poetry"""
    print("[INFO] Vérification de Django via Poetry...")
    
    try:
        result = subprocess.run(
            'poetry run python -c "import django; print(f\'Django {django.get_version()} OK\')"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[OK] {result.stdout.strip()}")
            return True
        else:
            print(f"[FAIL] Django non accessible: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Erreur Django: {e}")
        return False

def main():
    """Fonction principale"""
    print("EXECUTION COMPLETE DES TESTS SOFTDESK")
    print("Version corrigée pour Poetry + Windows")
    print("=" * 60)
    
    # 1. Vérifications préliminaires
    if not check_poetry_env():
        print("\n[ERROR] Poetry n'est pas disponible. Installez Poetry d'abord.")
        return 1
    
    if not check_django_via_poetry():
        print("\n[ERROR] Django n'est pas accessible via Poetry.")
        print("Solutions possibles:")
        print("1. poetry install")
        print("2. poetry add django djangorestframework")
        return 1
    
    print("\n[SUCCESS] Environnement Poetry + Django OK")
    
    # 2. Exécuter les tests
    success_count = 0
    total_tests = 0
    
    # Tests organisés par priorité
    test_files = [
        # Tests des modèles
        ("tests/models/test_issue_comment.py", "Tests Issue/Comment détaillés"),
        ("tests/models/test_issue_comment_simple.py", "Tests Issue/Comment simplifiés"),
        
        # Tests des API
        ("tests/api/test_basic_api.py", "Tests API de base"),
        ("tests/api/test_complete_api.py", "Tests API complets"),
        ("tests/api/test_issue_comment_api.py", "Tests API Issue/Comment"),
        ("tests/api/test_nested_routes.py", "Tests routes imbriquées"),
        
        # Tests RGPD
        ("tests/rgpd/test_compliance.py", "Tests conformité RGPD"),
        ("tests/rgpd/test_api.py", "Tests API RGPD"),
        
        # Tests de performance
        ("tests/performance/test_performance.py", "Tests de performance"),
    ]
    
    print(f"\n[INFO] Exécution de {len(test_files)} suites de tests...")
    
    for script_path, description in test_files:
        total_tests += 1
        
        # Vérifier que le fichier existe
        if not os.path.exists(script_path):
            print(f"\n[WARNING] Fichier manquant: {script_path}")
            continue
            
        if run_test_with_poetry(script_path, description):
            success_count += 1
    
    # 3. Résumé final
    print("\n" + "=" * 60)
    print("RÉSUMÉ FINAL")
    print("=" * 60)
    print(f"[STATS] Tests réussis: {success_count}/{total_tests}")
    
    if total_tests > 0:
        success_rate = (success_count / total_tests) * 100
        print(f"[STATS] Taux de réussite: {success_rate:.1f}%")
    else:
        success_rate = 0
        print("[WARNING] Aucun test n'a pu être exécuté")
    
    if success_count == total_tests and total_tests > 0:
        print("[SUCCESS] TOUS LES TESTS SONT PASSÉS!")
        return 0
    else:
        print("[WARNING] Certains tests ont échoué ou sont manquants.")
        print("\nDébogage recommandé:")
        print("1. Vérifiez les logs d'erreur ci-dessus")
        print("2. Vérifiez la configuration Django:")
        print("   poetry run python manage.py check")
        return 1

if __name__ == "__main__":
    # S'assurer qu'on est dans le bon répertoire
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    sys.exit(main())
