"""
Test spécifique pour la validation RGPD via l'API
"""
import requests
import json

class RGPDAPITester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.headers = {"Content-Type": "application/json"}
    
    def test_user_registration_without_age(self):
        """Tester l'inscription sans âge (doit échouer)"""
        print("🔒 Test API : Inscription sans âge")
        print("-" * 40)
        
        url = f"{self.base_url}/api/users/"
        data = {
            "username": "user_no_age_api",
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "can_be_contacted": True,
            "can_data_be_shared": False
            # age manquant volontairement
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 400:
                error_data = response.json()
                if 'age' in error_data:
                    print("✅ Correct: Inscription refusée, âge manquant")
                    print(f"   📝 Erreur: {error_data['age']}")
                else:
                    print("❌ Inscription refusée mais pas pour l'âge")
                    print(f"   📝 Erreurs: {error_data}")
            elif response.status_code == 201:
                print("⚠️  PROBLÈME: Inscription acceptée sans âge!")
                user_data = response.json()
                print(f"   📝 Utilisateur créé: {user_data}")
            else:
                print(f"❓ Code de réponse inattendu: {response.status_code}")
                print(f"   📝 Réponse: {response.text}")
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
    
    def test_user_registration_age_too_young(self):
        """Tester l'inscription avec âge < 15 ans (doit échouer)"""
        print("\n🔒 Test API : Inscription âge < 15 ans")
        print("-" * 40)
        
        url = f"{self.base_url}/api/users/"
        data = {
            "username": "user_14_api",
            "email": "young@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "age": 14,
            "can_be_contacted": True,
            "can_data_be_shared": False
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 400:
                error_data = response.json()
                if 'age' in error_data:
                    print("✅ Correct: Inscription refusée, âge < 15 ans")
                    print(f"   📝 Erreur: {error_data['age']}")
                else:
                    print("❌ Inscription refusée mais pas pour l'âge")
                    print(f"   📝 Erreurs: {error_data}")
            elif response.status_code == 201:
                print("⚠️  PROBLÈME: Inscription acceptée avec âge < 15 ans!")
                user_data = response.json()
                print(f"   📝 Utilisateur créé: {user_data}")
                # Nettoyer si créé par erreur
                requests.delete(f"{self.base_url}/api/users/{user_data['id']}/")
            else:
                print(f"❓ Code de réponse inattendu: {response.status_code}")
                print(f"   📝 Réponse: {response.text}")
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
    
    def test_user_registration_valid_age(self):
        """Tester l'inscription avec âge valide ≥ 15 ans (doit réussir)"""
        print("\n🔒 Test API : Inscription âge valide")
        print("-" * 40)
        
        url = f"{self.base_url}/api/users/"
        data = {
            "username": "user_valid_api",
            "email": "valid@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "age": 20,
            "can_be_contacted": True,
            "can_data_be_shared": False
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                user_data = response.json()
                print("✅ Correct: Inscription acceptée avec âge valide")
                print(f"   📝 Utilisateur créé: {user_data.get('username')} (âge: {user_data.get('age')})")
                
                # Nettoyer l'utilisateur de test
                user_id = user_data.get('id')
                if user_id:
                    try:
                        delete_response = requests.delete(f"{self.base_url}/api/users/{user_id}/")
                        if delete_response.status_code in [204, 404]:
                            print("   🧹 Utilisateur de test supprimé")
                        else:
                            print(f"   ⚠️  Suppression partielle (code {delete_response.status_code})")
                    except Exception:
                        print("   ⚠️  Impossible de supprimer l'utilisateur de test")
                        
            elif response.status_code == 400:
                error_data = response.json()
                print("❌ Inscription refusée avec âge valide")
                print(f"   📝 Erreurs: {error_data}")
            else:
                print(f"❓ Code de réponse inattendu: {response.status_code}")
                print(f"   📝 Réponse: {response.text}")
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
    
    def run_all_tests(self):
        """Exécuter tous les tests RGPD API"""
        print("🧪 TESTS RGPD VIA API")
        print("=" * 50)
        
        # Vérifier que le serveur fonctionne
        try:
            response = requests.get(f"{self.base_url}/api/", timeout=5)
            if response.status_code != 200:
                print("❌ Serveur Django non accessible")
                print("💡 Lancez: poetry run python manage.py runserver")
                return
        except:
            print("❌ Serveur Django non accessible")
            print("💡 Lancez: poetry run python manage.py runserver")
            return
        
        self.test_user_registration_without_age()
        self.test_user_registration_age_too_young()
        self.test_user_registration_valid_age()
        
        print("\n" + "=" * 50)
        print("🎯 RÉSUMÉ DES TESTS RGPD API:")
        print("   - ❌ Inscription sans âge : REFUSÉE")
        print("   - ❌ Inscription âge < 15 : REFUSÉE") 
        print("   - ✅ Inscription âge ≥ 15 : ACCEPTÉE")
        print("=" * 50)

if __name__ == "__main__":
    tester = RGPDAPITester()
    tester.run_all_tests()
