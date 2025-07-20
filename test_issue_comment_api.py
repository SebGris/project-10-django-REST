"""
Script de test API pour valider les endpoints Issue et Comment
"""
import requests
import json


class IssueCommentAPITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {}
        self.test_user_id = None
        self.test_project_id = None
        self.test_issue_id = None
        self.test_comment_id = None
        
        # Compteurs pour les tests
        self.tests_passed = 0
        self.tests_failed = 0
    
    def log(self, message, success=True):
        """Logger les résultats des tests"""
        status = "✅" if success else "❌"
        print(f"{status} {message}")
        if success:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
    
    def login(self, username="admin", password="SoftDesk2025!"):
        """Se connecter et obtenir le token JWT"""
        print("\n🔐 Authentification")
        print("-" * 20)
        
        try:
            response = requests.post(f"{self.base_url}/api/token/", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")
                self.headers = {"Authorization": f"Bearer {self.token}"}
                self.log(f"Connexion réussie pour {username}")
                return True
            else:
                self.log(f"Échec de connexion: {response.status_code} - {response.text}", False)
                return False
        except Exception as e:
            self.log(f"Erreur de connexion: {e}", False)
            return False
    
    def create_test_user(self):
        """Créer un utilisateur de test"""
        print("\n👤 Création d'un utilisateur de test")
        print("-" * 30)
        
        test_user_data = {
            "username": "test_issue_user",
            "email": "test.issue@example.com",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "age": 25,
            "can_be_contacted": True,
            "can_data_be_shared": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/users/", json=test_user_data)
            if response.status_code == 201:
                user_data = response.json()
                self.test_user_id = user_data.get('id')
                self.log(f"Utilisateur de test créé (ID: {self.test_user_id})")
                return True
            else:
                self.log(f"Erreur création utilisateur: {response.status_code} - {response.text}", False)
                return False
        except Exception as e:
            self.log(f"Erreur création utilisateur: {e}", False)
            return False
    
    def create_test_project(self):
        """Créer un projet de test"""
        print("\n📋 Création d'un projet de test")
        print("-" * 30)
        
        project_data = {
            "name": "Test Project Issues API",
            "description": "Projet de test pour valider les APIs Issue et Comment",
            "type": "back-end"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/projects/", json=project_data, headers=self.headers)
            if response.status_code == 201:
                project_data = response.json()
                self.test_project_id = project_data.get('id')
                self.log(f"Projet de test créé (ID: {self.test_project_id})")
                return True
            else:
                self.log(f"Erreur création projet: {response.status_code} - {response.text}", False)
                return False
        except Exception as e:
            self.log(f"Erreur création projet: {e}", False)
            return False
    
    def test_issues_crud(self):
        """Tester les opérations CRUD pour les issues"""
        print("\n🐛 Test des opérations CRUD pour les Issues")
        print("-" * 40)
        
        if not self.test_project_id:
            self.log("Aucun projet de test disponible", False)
            return False
        
        # 1. Créer une issue
        issue_data = {
            "name": "Bug de test",
            "description": "Ceci est un bug de test pour valider l'API",
            "priority": "HIGH",
            "tag": "BUG",
            "status": "To Do",
            "project": self.test_project_id
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/issues/", json=issue_data, headers=self.headers)
            if response.status_code == 201:
                issue_response = response.json()
                self.test_issue_id = issue_response.get('id')
                self.log(f"Issue créée (ID: {self.test_issue_id})")
            else:
                self.log(f"Erreur création issue: {response.status_code} - {response.text}", False)
                return False
        except Exception as e:
            self.log(f"Erreur création issue: {e}", False)
            return False
        
        # 2. Lire les issues
        try:
            response = requests.get(f"{self.base_url}/api/issues/", headers=self.headers)
            if response.status_code == 200:
                issues = response.json()
                self.log(f"Issues listées ({len(issues.get('results', issues))} trouvées)")
            else:
                self.log(f"Erreur lecture issues: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur lecture issues: {e}", False)
        
        # 3. Lire une issue spécifique
        try:
            response = requests.get(f"{self.base_url}/api/issues/{self.test_issue_id}/", headers=self.headers)
            if response.status_code == 200:
                issue = response.json()
                self.log(f"Issue détaillée récupérée: {issue.get('name')}")
            else:
                self.log(f"Erreur lecture issue détaillée: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur lecture issue détaillée: {e}", False)
        
        # 4. Modifier l'issue
        update_data = {
            "name": "Bug de test - MODIFIÉ",
            "status": "In Progress",
            "priority": "MEDIUM"
        }
        
        try:
            response = requests.patch(f"{self.base_url}/api/issues/{self.test_issue_id}/", json=update_data, headers=self.headers)
            if response.status_code == 200:
                self.log("Issue modifiée avec succès")
            else:
                self.log(f"Erreur modification issue: {response.status_code} - {response.text}", False)
        except Exception as e:
            self.log(f"Erreur modification issue: {e}", False)
        
        return True
    
    def test_comments_crud(self):
        """Tester les opérations CRUD pour les commentaires"""
        print("\n💬 Test des opérations CRUD pour les Comments")
        print("-" * 40)
        
        if not self.test_issue_id:
            self.log("Aucune issue de test disponible", False)
            return False
        
        # 1. Créer un commentaire
        comment_data = {
            "description": "Ceci est un commentaire de test pour valider l'API",
            "issue": self.test_issue_id
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/comments/", json=comment_data, headers=self.headers)
            if response.status_code == 201:
                comment_response = response.json()
                self.test_comment_id = comment_response.get('id')
                self.log(f"Commentaire créé (ID: {self.test_comment_id})")
            else:
                self.log(f"Erreur création commentaire: {response.status_code} - {response.text}", False)
                return False
        except Exception as e:
            self.log(f"Erreur création commentaire: {e}", False)
            return False
        
        # 2. Lire les commentaires
        try:
            response = requests.get(f"{self.base_url}/api/comments/", headers=self.headers)
            if response.status_code == 200:
                comments = response.json()
                self.log(f"Commentaires listés ({len(comments.get('results', comments))} trouvés)")
            else:
                self.log(f"Erreur lecture commentaires: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur lecture commentaires: {e}", False)
        
        # 3. Lire un commentaire spécifique
        try:
            response = requests.get(f"{self.base_url}/api/comments/{self.test_comment_id}/", headers=self.headers)
            if response.status_code == 200:
                comment = response.json()
                self.log(f"Commentaire détaillé récupéré")
            else:
                self.log(f"Erreur lecture commentaire détaillé: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur lecture commentaire détaillé: {e}", False)
        
        # 4. Modifier le commentaire
        update_data = {
            "description": "Commentaire de test MODIFIÉ - API validation"
        }
        
        try:
            response = requests.patch(f"{self.base_url}/api/comments/{self.test_comment_id}/", json=update_data, headers=self.headers)
            if response.status_code == 200:
                self.log("Commentaire modifié avec succès")
            else:
                self.log(f"Erreur modification commentaire: {response.status_code} - {response.text}", False)
        except Exception as e:
            self.log(f"Erreur modification commentaire: {e}", False)
        
        return True
    
    def test_permissions(self):
        """Tester les permissions"""
        print("\n🔒 Test des permissions")
        print("-" * 20)
        
        # Créer un deuxième utilisateur pour tester les permissions
        test_user_data = {
            "username": "test_permission_user",
            "email": "test.permission@example.com",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "age": 28,
            "can_be_contacted": True,
            "can_data_be_shared": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/users/", json=test_user_data)
            if response.status_code == 201:
                self.log("Utilisateur pour test de permissions créé")
                
                # Se connecter avec ce nouvel utilisateur
                login_response = requests.post(f"{self.base_url}/api/token/", json={
                    "username": "test_permission_user",
                    "password": "TestPass123!"
                })
                
                if login_response.status_code == 200:
                    new_token = login_response.json().get("access")
                    new_headers = {"Authorization": f"Bearer {new_token}"}
                    
                    # Essayer de modifier l'issue créée par l'autre utilisateur
                    update_data = {"name": "Tentative de modification non autorisée"}
                    
                    response = requests.patch(f"{self.base_url}/api/issues/{self.test_issue_id}/", 
                                            json=update_data, headers=new_headers)
                    
                    if response.status_code == 403:
                        self.log("Permission correctement refusée pour modification d'issue")
                    else:
                        self.log(f"Permission incorrecte: {response.status_code}", False)
                        
                else:
                    self.log("Erreur connexion utilisateur permission", False)
            else:
                self.log("Erreur création utilisateur permission", False)
        except Exception as e:
            self.log(f"Erreur test permissions: {e}", False)
    
    def cleanup(self):
        """Nettoyer les données de test"""
        print("\n🧹 Nettoyage des données de test")
        print("-" * 30)
        
        # Supprimer le commentaire
        if self.test_comment_id:
            try:
                response = requests.delete(f"{self.base_url}/api/comments/{self.test_comment_id}/", headers=self.headers)
                if response.status_code == 204:
                    self.log("Commentaire de test supprimé")
                else:
                    self.log(f"Erreur suppression commentaire: {response.status_code}", False)
            except Exception as e:
                self.log(f"Erreur suppression commentaire: {e}", False)
        
        # Supprimer l'issue
        if self.test_issue_id:
            try:
                response = requests.delete(f"{self.base_url}/api/issues/{self.test_issue_id}/", headers=self.headers)
                if response.status_code == 204:
                    self.log("Issue de test supprimée")
                else:
                    self.log(f"Erreur suppression issue: {response.status_code}", False)
            except Exception as e:
                self.log(f"Erreur suppression issue: {e}", False)
        
        # Supprimer le projet
        if self.test_project_id:
            try:
                response = requests.delete(f"{self.base_url}/api/projects/{self.test_project_id}/", headers=self.headers)
                if response.status_code == 204:
                    self.log("Projet de test supprimé")
                else:
                    self.log(f"Erreur suppression projet: {response.status_code}", False)
            except Exception as e:
                self.log(f"Erreur suppression projet: {e}", False)
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🧪 Test API complet des modèles Issue et Comment")
        print("=" * 60)
        
        # Authentification
        if not self.login():
            print("❌ Impossible de se connecter, arrêt des tests")
            return
        
        # Tests principaux
        self.create_test_user()
        self.create_test_project()
        self.test_issues_crud()
        self.test_comments_crud()
        self.test_permissions()
        
        # Nettoyage
        self.cleanup()
        
        # Résumé
        print(f"\n📊 Résumé des tests")
        print("-" * 20)
        print(f"✅ Tests réussis: {self.tests_passed}")
        print(f"❌ Tests échoués: {self.tests_failed}")
        total = self.tests_passed + self.tests_failed
        if total > 0:
            success_rate = (self.tests_passed / total) * 100
            print(f"📈 Taux de réussite: {success_rate:.1f}%")


if __name__ == "__main__":
    tester = IssueCommentAPITester()
    tester.run_all_tests()
