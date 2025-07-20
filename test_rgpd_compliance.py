#!/usr/bin/env python3
"""
Test de conformité RGPD - Validation de l'âge minimum
"""

import urllib.request
import urllib.parse
import json
import urllib.error

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(url, method='GET', data=None, headers=None):
    """Faire une requête HTTP avec urllib"""
    if headers is None:
        headers = {}
    
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return {
                'status_code': response.getcode(),
                'data': json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_data)
        except:
            error_json = error_data
        return {
            'status_code': e.code,
            'data': error_json
        }
    except Exception as e:
        return {
            'status_code': 0,
            'data': str(e)
        }

def test_rgpd_age_validation():
    """Test de la validation RGPD pour l'âge minimum"""
    
    print("🔒 Test de conformité RGPD - Validation âge minimum\n")
    
    # Test 1 : Tentative d'inscription avec âge < 15 ans
    print("1. 🚫 Test inscription utilisateur de 12 ans (doit être rejetée)...")
    
    user_data_under_15 = {
        "username": "enfant_12ans",
        "email": "enfant@example.com",
        "first_name": "Enfant",
        "last_name": "Trop Jeune",
        "age": 12,  # < 15 ans ❌
        "can_be_contacted": True,
        "can_data_be_shared": False,
        "password": "TestPass123!",
        "password_confirm": "TestPass123!"
    }
    
    response = make_request(f"{BASE_URL}/users/", method='POST', data=user_data_under_15)
    
    if response['status_code'] == 400:
        print("   ✅ CONFORME RGPD : Inscription rejetée")
        print(f"   📝 Message d'erreur : {response['data']}")
        
        # Vérifier que l'erreur mentionne l'âge
        error_message = str(response['data']).lower()
        if 'âge' in error_message or 'age' in error_message or 'rgpd' in error_message:
            print("   ✅ Message d'erreur approprié mentionnant l'âge/RGPD")
        else:
            print("   ⚠️  Message d'erreur ne mentionne pas explicitement l'âge/RGPD")
    else:
        print(f"   ❌ PROBLÈME RGPD : Inscription acceptée (statut {response['status_code']})")
        print(f"   📝 Réponse : {response['data']}")
    
    print("\n" + "="*60)
    
    # Test 2 : Tentative d'inscription avec âge = 15 ans (limite)
    print("\n2. ✅ Test inscription utilisateur de 15 ans (doit être acceptée)...")
    
    user_data_15 = {
        "username": "ado_15ans",
        "email": "ado15@example.com",
        "first_name": "Ado",
        "last_name": "Quinze Ans",
        "age": 15,  # = 15 ans ✅
        "can_be_contacted": True,
        "can_data_be_shared": False,
        "password": "TestPass123!",
        "password_confirm": "TestPass123!"
    }
    
    response = make_request(f"{BASE_URL}/users/", method='POST', data=user_data_15)
    
    if response['status_code'] == 201:
        print("   ✅ CONFORME RGPD : Inscription acceptée pour 15 ans")
        print(f"   📝 Utilisateur créé : ID {response['data'].get('id')}")
    else:
        print(f"   ❌ PROBLÈME : Inscription rejetée (statut {response['status_code']})")
        print(f"   📝 Erreur : {response['data']}")
    
    print("\n" + "="*60)
    
    # Test 3 : Tentative d'inscription avec âge > 15 ans
    print("\n3. ✅ Test inscription utilisateur de 25 ans (doit être acceptée)...")
    
    user_data_25 = {
        "username": "adulte_25ans",
        "email": "adulte25@example.com",
        "first_name": "Adulte",
        "last_name": "Vingt Cinq",
        "age": 25,  # > 15 ans ✅
        "can_be_contacted": True,
        "can_data_be_shared": True,
        "password": "TestPass123!",
        "password_confirm": "TestPass123!"
    }
    
    response = make_request(f"{BASE_URL}/users/", method='POST', data=user_data_25)
    
    if response['status_code'] == 201:
        print("   ✅ CONFORME RGPD : Inscription acceptée pour 25 ans")
        print(f"   📝 Utilisateur créé : ID {response['data'].get('id')}")
    else:
        print(f"   ❌ PROBLÈME : Inscription rejetée (statut {response['status_code']})")
        print(f"   📝 Erreur : {response['data']}")
    
    print("\n" + "="*60)
    
    # Test 4 : Inscription sans âge (optionnel)
    print("\n4. ⚠️  Test inscription sans âge spécifié...")
    
    user_data_no_age = {
        "username": "sans_age",
        "email": "sansage@example.com", 
        "first_name": "Sans",
        "last_name": "Age",
        # age non spécifié
        "can_be_contacted": False,
        "can_data_be_shared": False,
        "password": "TestPass123!",
        "password_confirm": "TestPass123!"
    }
    
    response = make_request(f"{BASE_URL}/users/", method='POST', data=user_data_no_age)
    
    if response['status_code'] == 201:
        print("   ✅ Inscription acceptée sans âge spécifié")
        print("   📝 Note : L'âge n'est pas obligatoire")
    else:
        print(f"   ❌ Inscription rejetée (statut {response['status_code']})")
        print(f"   📝 Erreur : {response['data']}")
    
    print("\n" + "="*60)
    print("\n📋 RÉSUMÉ DE LA CONFORMITÉ RGPD :")
    print("✅ Les utilisateurs de moins de 15 ans doivent être rejetés")
    print("✅ Les utilisateurs de 15 ans et plus doivent être acceptés")
    print("✅ Le message d'erreur doit mentionner le RGPD/âge minimum")
    print("⚠️  Considérer rendre l'âge obligatoire pour une meilleure conformité")

if __name__ == "__main__":
    print("🚀 Démarrage des tests de conformité RGPD...")
    print("⚠️  Assurez-vous que le serveur Django est démarré !")
    print()
    test_rgpd_age_validation()
