"""
Script de test complet pour valider toutes les URLs de l'API SoftDesk
"""
import requests
import json
import time

class CompleteTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        self.created_project_id = None
        self.created_user_id = None
    
    def log(self, message, success=True):
        """Afficher un message avec formatage"""
        icon = "✅" if success else "❌"
        print(f"{icon} {message}")
    
    def test_server_running(self):
        """Vérifier que le serveur Django fonctionne"""
        print("\n🔧 Test du serveur Django")
        print("-" * 30)
        
        try:
            response = requests.get(f"{self.base_url}/api/", timeout=5)
            if response.status_code == 200:
                self.log("Serveur Django accessible")
                return True
            else:
                self.log(f"Serveur répond avec le code {response.status_code}", False)
                return False
        except requests.exceptions.ConnectionError:
            self.log("❗ Serveur Django non accessible. Assurez-vous qu'il fonctionne avec: poetry run python manage.py runserver", False)
            return False
        except Exception as e:
            self.log(f"Erreur de connexion: {e}", False)
            return False
    
    def test_user_registration(self):
        """Tester l'inscription d'un utilisateur"""
        print("\n👤 Test d'inscription utilisateur")
        print("-" * 30)
        
        url = f"{self.base_url}/api/users/"
        data = {
            "username": f"testuser_{int(time.time())}",
            "email": "test@example.com",
            "password": "testpassword123",
            "age": 25,
            "can_be_contacted": True,
            "can_data_be_shared": False
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                user_data = response.json()
                self.created_user_id = user_data.get('id')
                self.log(f"Utilisateur créé: {user_data.get('username')}")
                return True
            else:
                self.log(f"Erreur inscription (Code {response.status_code}): {response.text}", False)
                return False
        except Exception as e:
            self.log(f"Erreur lors de l'inscription: {e}", False)
            return False
    
    def test_authentication(self):
        """Tester l'authentification JWT"""
        print("\n🔐 Test d'authentification JWT")
        print("-" * 30)
        
        # Essayer avec le superutilisateur
        url = f"{self.base_url}/api/token/"
        data = {
            "username": "admin",
            "password": "SoftDesk2025!"
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data["access"]
                self.headers["Authorization"] = f"Bearer {self.token}"
                self.log("Token JWT obtenu avec succès")
                return True
            else:
                self.log(f"Erreur authentification (Code {response.status_code}): {response.text}", False)
                self.log("💡 Créez d'abord un superutilisateur avec: poetry run python manage.py createsuperuser", False)
                return False
        except Exception as e:
            self.log(f"Erreur lors de l'authentification: {e}", False)
            return False
    
    def test_projects_crud(self):
        """Tester les opérations CRUD sur les projets"""
        print("\n📋 Test CRUD des projets")
        print("-" * 30)
        
        # 1. Lister les projets
        try:
            response = requests.get(f"{self.base_url}/api/projects/", headers=self.headers)
            if response.status_code == 200:
                self.log("Liste des projets accessible")
            else:
                self.log(f"Erreur liste projets: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur liste projets: {e}", False)
        
        # 2. Créer un projet
        project_data = {
            "name": f"Projet Test {int(time.time())}",
            "description": "Projet créé pour tester l'API",
            "type": "back-end"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/projects/", json=project_data, headers=self.headers)
            if response.status_code == 201:
                project = response.json()
                self.created_project_id = project.get('id')
                self.log(f"Projet créé: {project.get('name')}")
            else:
                self.log(f"Erreur création projet: {response.status_code} - {response.text}", False)
                return False
        except Exception as e:
            self.log(f"Erreur création projet: {e}", False)
            return False
        
        # 3. Récupérer le projet créé
        if self.created_project_id:
            try:
                response = requests.get(f"{self.base_url}/api/projects/{self.created_project_id}/", headers=self.headers)
                if response.status_code == 200:
                    self.log("Détails du projet accessibles")
                else:
                    self.log(f"Erreur détails projet: {response.status_code}", False)
            except Exception as e:
                self.log(f"Erreur détails projet: {e}", False)
        
        return True
    
    def test_contributors(self):
        """Tester la gestion des contributeurs"""
        print("\n👥 Test de gestion des contributeurs")
        print("-" * 30)
        
        if not self.created_project_id:
            self.log("Aucun projet disponible pour tester les contributeurs", False)
            return False
        
        # 1. Lister les contributeurs du projet
        try:
            response = requests.get(f"{self.base_url}/api/projects/{self.created_project_id}/contributors/", headers=self.headers)
            if response.status_code == 200:
                contributors = response.json()
                self.log(f"Contributeurs listés ({len(contributors)} trouvés)")
            else:
                self.log(f"Erreur liste contributeurs: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur liste contributeurs: {e}", False)
        
        # 2. Tenter d'ajouter un contributeur (nécessite un autre utilisateur)
        if self.created_user_id:
            try:
                # Récupérer le username du nouvel utilisateur
                user_response = requests.get(f"{self.base_url}/api/users/{self.created_user_id}/", headers=self.headers)
                if user_response.status_code == 200:
                    username = user_response.json().get('username')
                    
                    add_data = {"username": username}
                    response = requests.post(
                        f"{self.base_url}/api/projects/{self.created_project_id}/add-contributor/", 
                        json=add_data, 
                        headers=self.headers
                    )
                    if response.status_code == 201:
                        self.log(f"Contributeur {username} ajouté avec succès")
                    else:
                        self.log(f"Erreur ajout contributeur: {response.status_code} - {response.text}", False)
            except Exception as e:
                self.log(f"Erreur ajout contributeur: {e}", False)
        
        return True
    
    def test_users_endpoints(self):
        """Tester les endpoints utilisateurs"""
        print("\n🧑‍💼 Test des endpoints utilisateurs")
        print("-" * 30)
        
        # 1. Lister les utilisateurs
        try:
            response = requests.get(f"{self.base_url}/api/users/", headers=self.headers)
            if response.status_code == 200:
                users = response.json()
                total_users = len(users.get('results', []))
                self.log(f"Liste utilisateurs accessible ({total_users} utilisateurs)")
            else:
                self.log(f"Erreur liste utilisateurs: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur liste utilisateurs: {e}", False)
        
        # 2. Profil personnel
        try:
            response = requests.get(f"{self.base_url}/api/users/profile/", headers=self.headers)
            if response.status_code == 200:
                profile = response.json()
                self.log(f"Profil personnel accessible: {profile.get('username')}")
            else:
                self.log(f"Erreur profil personnel: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur profil personnel: {e}", False)
        
        return True
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🧪 TESTS COMPLETS DE L'API SOFTDESK")
        print("=" * 50)
        
        # Test préliminaire du serveur
        if not self.test_server_running():
            print("\n❌ Impossible de continuer: serveur Django non accessible")
            return False
        
        # Tests d'inscription (sans auth)
        self.test_user_registration()
        
        # Tests d'authentification
        if not self.test_authentication():
            print("\n❌ Impossible de continuer: échec de l'authentification")
            return False
        
        # Tests avec authentification
        self.test_projects_crud()
        self.test_contributors()
        self.test_users_endpoints()
        
        print("\n" + "=" * 50)
        print("🎉 TESTS TERMINÉS")
        print("=" * 50)
        
        if self.created_project_id:
            print(f"💡 Projet de test créé avec l'ID: {self.created_project_id}")
        
        print("\n📖 Pour des tests plus approfondis:")
        print("   - Importez la collection Postman: SoftDesk_API_Postman_Collection.json")
        print("   - Consultez l'interface web: http://127.0.0.1:8000/api/")
        print("   - Lisez les guides: API_TESTING_COMPLETE_GUIDE.md")

if __name__ == "__main__":
    tester = CompleteTester()
    tester.run_all_tests()
