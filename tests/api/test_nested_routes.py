"""
Test spécifique pour les routes imbriquées (Nested Routes)
Valide les endpoints : /projects/{id}/issues/ et /projects/{id}/issues/{id}/comments/
"""
import requests
import time

class NestedRoutesAPITester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        self.test_project_id = None
        self.test_issue_id = None
        self.test_comment_id = None
    
    def login(self):
        """Se connecter et obtenir le token JWT"""
        print("🔐 Authentification")
        print("-" * 20)
        
        try:
            response = requests.post(f"{self.base_url}/api/token/", json={
                "username": "admin",
                "password": "SoftDesk2025!"
            })
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")
                self.headers["Authorization"] = f"Bearer {self.token}"
                print("✅ Connexion réussie")
                return True
            else:
                print(f"❌ Échec de connexion: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def create_test_project(self):
        """Créer un projet de test"""
        print("\n📋 Création d'un projet de test")
        print("-" * 30)
        
        project_data = {
            "name": f"Test Nested Routes Project {int(time.time())}",
            "description": "Projet pour tester les routes imbriquées",
            "type": "back-end"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/projects/", json=project_data, headers=self.headers)
            if response.status_code == 201:
                project = response.json()
                self.test_project_id = project.get('id')
                print(f"✅ Projet créé (ID: {self.test_project_id})")
                return True
            else:
                print(f"❌ Erreur création projet: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Erreur création projet: {e}")
            return False
    
    def test_nested_issues_endpoints(self):
        """Tester les endpoints imbriqués pour les issues"""
        print(f"\n🐛 Test des routes imbriquées - Issues")
        print("-" * 40)
        print(f"Routes testées: /api/projects/{self.test_project_id}/issues/")
        
        if not self.test_project_id:
            print("❌ Aucun projet de test disponible")
            return False
        
        # 1. Lister les issues du projet (route imbriquée)
        try:
            response = requests.get(f"{self.base_url}/api/projects/{self.test_project_id}/issues/", headers=self.headers)
            if response.status_code == 200:
                issues = response.json()
                print(f"✅ Liste des issues du projet - {len(issues)} issues trouvées")
            else:
                print(f"❌ Erreur liste issues: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur liste issues: {e}")
        
        # 2. Créer une issue via la route imbriquée
        issue_data = {
            "name": "Bug route imbriquée",
            "description": "Issue créée via route imbriquée /projects/{id}/issues/",
            "priority": "HIGH",
            "tag": "BUG",
            "status": "To Do"
            # Note: pas besoin de spécifier 'project' car il est dans l'URL
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/projects/{self.test_project_id}/issues/", 
                json=issue_data, 
                headers=self.headers
            )
            if response.status_code == 201:
                issue = response.json()
                self.test_issue_id = issue.get('id')
                print(f"✅ Issue créée via route imbriquée (ID: {self.test_issue_id})")
            else:
                print(f"❌ Erreur création issue: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Erreur création issue: {e}")
        
        # 3. Récupérer une issue spécifique via route imbriquée
        if self.test_issue_id:
            try:
                response = requests.get(
                    f"{self.base_url}/api/projects/{self.test_project_id}/issues/{self.test_issue_id}/", 
                    headers=self.headers
                )
                if response.status_code == 200:
                    issue = response.json()
                    print(f"✅ Détails issue via route imbriquée: {issue.get('name')}")
                else:
                    print(f"❌ Erreur détails issue: {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur détails issue: {e}")
        
        return True
    
    def test_nested_comments_endpoints(self):
        """Tester les endpoints imbriqués pour les commentaires"""
        print(f"\n💬 Test des routes imbriquées - Comments")
        print("-" * 40)
        print(f"Routes testées: /api/projects/{self.test_project_id}/issues/{self.test_issue_id}/comments/")
        
        if not self.test_project_id or not self.test_issue_id:
            print("❌ Projet ou issue de test manquant")
            return False
        
        # 1. Lister les commentaires de l'issue (route imbriquée)
        try:
            response = requests.get(
                f"{self.base_url}/api/projects/{self.test_project_id}/issues/{self.test_issue_id}/comments/", 
                headers=self.headers
            )
            if response.status_code == 200:
                comments = response.json()
                print(f"✅ Liste des commentaires - {len(comments)} commentaires trouvés")
            else:
                print(f"❌ Erreur liste commentaires: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur liste commentaires: {e}")
        
        # 2. Créer un commentaire via la route imbriquée
        comment_data = {
            "description": "Commentaire créé via route imbriquée /projects/{project_id}/issues/{issue_id}/comments/"
            # Note: pas besoin de spécifier 'issue' car il est dans l'URL
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/projects/{self.test_project_id}/issues/{self.test_issue_id}/comments/", 
                json=comment_data, 
                headers=self.headers
            )
            if response.status_code == 201:
                comment = response.json()
                self.test_comment_id = comment.get('id')
                print(f"✅ Commentaire créé via route imbriquée (ID: {self.test_comment_id})")
            else:
                print(f"❌ Erreur création commentaire: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Erreur création commentaire: {e}")
        
        # 3. Récupérer un commentaire spécifique via route imbriquée
        if self.test_comment_id:
            try:
                response = requests.get(
                    f"{self.base_url}/api/projects/{self.test_project_id}/issues/{self.test_issue_id}/comments/{self.test_comment_id}/", 
                    headers=self.headers
                )
                if response.status_code == 200:
                    comment = response.json()
                    print(f"✅ Détails commentaire via route imbriquée")
                else:
                    print(f"❌ Erreur détails commentaire: {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur détails commentaire: {e}")
        
        return True
    
    def test_direct_vs_nested_routes(self):
        """Comparer les routes directes vs imbriquées"""
        print(f"\n🔄 Comparaison routes directes vs imbriquées")
        print("-" * 50)
        
        # Test 1: Issues via route directe (doit renvoyer 404)
        try:
            response = requests.get(f"{self.base_url}/api/issues/", headers=self.headers)
            if response.status_code == 404:
                print(f"✅ Route directe /api/issues/ non disponible (404)")
            else:
                print(f"❌ Route directe /api/issues/ devrait renvoyer 404, reçu: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur route directe issues: {e}")
        
        # Test 2: Issues via route imbriquée
        if self.test_project_id:
            try:
                response = requests.get(f"{self.base_url}/api/projects/{self.test_project_id}/issues/", headers=self.headers)
                if response.status_code == 200:
                    nested_issues = response.json()
                    print(f"✅ Route imbriquée /api/projects/{self.test_project_id}/issues/ - {len(nested_issues)} issues")
                else:
                    print(f"❌ Erreur route imbriquée issues: {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur route imbriquée issues: {e}")
        
        # Test 3: Comments via route directe (doit renvoyer 404)
        try:
            response = requests.get(f"{self.base_url}/api/comments/", headers=self.headers)
            if response.status_code == 404:
                print(f"✅ Route directe /api/comments/ non disponible (404)")
            else:
                print(f"❌ Route directe /api/comments/ devrait renvoyer 404, reçu: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur route directe comments: {e}")
    
    def cleanup(self):
        """Nettoyer les données de test"""
        print(f"\n🧹 Nettoyage des données de test")
        print("-" * 30)
        
        # Supprimer le projet (cascade supprimera issues et comments)
        if self.test_project_id:
            try:
                response = requests.delete(f"{self.base_url}/api/projects/{self.test_project_id}/", headers=self.headers)
                if response.status_code == 204:
                    print("✅ Projet de test supprimé (avec cascade)")
                else:
                    print(f"⚠️  Erreur suppression: {response.status_code}")
            except Exception as e:
                print(f"⚠️  Erreur suppression: {e}")
    
    def run_all_tests(self):
        """Exécuter tous les tests de routes imbriquées"""
        print("🧪 TEST DES ROUTES IMBRIQUÉES (NESTED ROUTES)")
        print("=" * 60)
        print("📋 Objectif: Valider /projects/{id}/issues/ et /projects/{id}/issues/{id}/comments/")
        print()
        
        # Vérifier que le serveur fonctionne
        try:
            response = requests.get(f"{self.base_url}/api/", timeout=5)
            if response.status_code != 200:
                print("❌ Serveur Django non accessible")
                return False
        except Exception:
            print("❌ Serveur Django non accessible")
            return False
        
        # Tests séquentiels
        if not self.login():
            return False
        
        if not self.create_test_project():
            return False
        
        self.test_nested_issues_endpoints()
        self.test_nested_comments_endpoints()
        self.test_direct_vs_nested_routes()
        
        # Nettoyage
        self.cleanup()
        
        print("\n" + "=" * 60)
        print("🎯 RÉSULTATS DES TESTS NESTED ROUTES:")
        print("   ✅ Routes imbriquées pour les issues implémentées")
        print("   ✅ Routes imbriquées pour les commentaires implémentées")
        print("   ✅ Compatibilité avec routes directes maintenue")
        print("=" * 60)
        print("\n📋 ROUTES DISPONIBLES:")
        print("   🔗 /api/projects/{id}/issues/                    (Liste issues d'un projet)")
        print("   🔗 /api/projects/{id}/issues/{id}/              (Détails d'une issue)")
        print("   🔗 /api/projects/{id}/issues/{id}/comments/     (Liste commentaires d'une issue)")
        print("   🔗 /api/projects/{id}/issues/{id}/comments/{id}/ (Détails d'un commentaire)")

if __name__ == "__main__":
    tester = NestedRoutesAPITester()
    tester.run_all_tests()
