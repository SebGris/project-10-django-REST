"""
Script de test pour l'API SoftDesk Support
"""
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "SoftDesk2025!"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def get_token(self):
        """Obtenir un token JWT"""
        url = f"{self.base_url}/api/token/"
        data = {
            "username": USERNAME,
            "password": PASSWORD
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access"]
            self.headers["Authorization"] = f"Bearer {self.token}"
            print("✅ Token obtenu avec succès")
            return True
        else:
            print(f"❌ Erreur lors de l'obtention du token: {response.status_code}")
            return False
    
    def test_projects_list(self):
        """Tester la liste des projets"""
        url = f"{self.base_url}/api/projects/"
        response = requests.get(url, headers=self.headers)
        
        print(f"\n📋 Liste des projets - Status: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            print(f"Nombre de projets: {len(projects.get('results', []))}")
        else:
            print(f"Erreur: {response.text}")
    
    def test_create_project(self):
        """Tester la création d'un projet"""
        url = f"{self.base_url}/api/projects/"
        data = {
            "name": "Projet Test API",
            "description": "Projet créé via le script de test",
            "type": "back-end"
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        print(f"\n🆕 Création de projet - Status: {response.status_code}")
        
        if response.status_code == 201:
            project = response.json()
            print(f"Projet créé: {project['name']} (ID: {project['id']})")
            return project['id']
        else:
            print(f"Erreur: {response.text}")
            return None
    
    def test_project_detail(self, project_id):
        """Tester les détails d'un projet"""
        url = f"{self.base_url}/api/projects/{project_id}/"
        response = requests.get(url, headers=self.headers)
        
        print(f"\n🔍 Détails du projet {project_id} - Status: {response.status_code}")
        if response.status_code == 200:
            project = response.json()
            print(f"Nom: {project['name']}")
            print(f"Type: {project['type']}")
            print(f"Auteur: {project['author']['username']}")
        else:
            print(f"Erreur: {response.text}")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 Début des tests de l'API SoftDesk")
        
        # 1. Obtenir le token
        if not self.get_token():
            return
        
        # 2. Lister les projets
        self.test_projects_list()
        
        # 3. Créer un projet
        project_id = self.test_create_project()
        
        # 4. Voir les détails du projet créé
        if project_id:
            self.test_project_detail(project_id)
        
        print("\n✅ Tests terminés")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
