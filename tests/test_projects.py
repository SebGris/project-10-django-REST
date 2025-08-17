"""
Tests pour la gestion des projets, issues et commentaires
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from issues.models import Project, Contributor, Comment

User = get_user_model()


@pytest.mark.django_db
class TestProjects:
    """Tests pour la gestion des projets"""
    
    def test_create_project(self, authenticated_client):
        """Test de création d'un projet"""
        url = reverse('project-list')
        data = {
            'name': 'New Project',
            'description': 'Project Description for testing',
            'type': 'front-end'
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Project'
        assert response.data['type'] == 'front-end'
        assert response.data['author']['id'] == authenticated_client.user.id
        
        # Vérifier que l'auteur est automatiquement contributeur
        project = Project.objects.get(id=response.data['id'])
        assert project.contributors.filter(user=authenticated_client.user).exists()
    
    def test_create_project_invalid_type(self, authenticated_client):
        """Test de création avec un type invalide"""
        url = reverse('project-list')
        data = {
            'name': 'Invalid Type Project',
            'description': 'Testing invalid type',
            'type': 'invalid-type'  # Type invalide
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'type' in response.data
    
    def test_list_only_contributor_projects(self, authenticated_client, create_project, create_user):
        """Test que l'utilisateur ne voit que ses projets"""
        # Créer un projet où l'utilisateur est auteur
        project1 = create_project(author=authenticated_client.user)
        
        # Créer un projet où l'utilisateur n'est pas contributeur
        other_user = create_user(username='otheruser')
        project2 = create_project(name='Other Project', author=other_user)
        
        url = reverse('project-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        project_ids = [p['id'] for p in response.data['results']]
        assert project1.id in project_ids
        assert project2.id not in project_ids
    
    def test_add_contributor(self, authenticated_client, create_project, create_user):
        """Test d'ajout d'un contributeur par l'auteur"""
        project = create_project(author=authenticated_client.user)
        new_user = create_user(username='contributor', age=20)
        
        url = reverse('project-add-contributor', kwargs={'pk': project.id})
        data = {'user_id': new_user.id}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'contributor' in response.data
        assert Contributor.objects.filter(project=project, user=new_user).exists()
    
    def test_add_contributor_twice(self, authenticated_client, create_project, create_user):
        """Test qu'on ne peut pas ajouter le même contributeur deux fois"""
        project = create_project(author=authenticated_client.user)
        user = create_user(username='contributor')
        
        url = reverse('project-add-contributor', kwargs={'pk': project.id})
        data = {'user_id': user.id}
        
        # Première addition
        response1 = authenticated_client.post(url, data, format='json')
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Deuxième tentative
        response2 = authenticated_client.post(url, data, format='json')
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert 'déjà contributeur' in str(response2.data)
    
    def test_non_author_cannot_add_contributor(self, authenticated_client, create_project, create_user):
        """Test que seul l'auteur peut ajouter des contributeurs"""
        other_user = create_user(username='otherauthor')
        project = create_project(author=other_user)
        new_contributor = create_user(username='newcontrib')
        
        url = reverse('project-add-contributor', kwargs={'pk': project.id})
        data = {'user_id': new_contributor.id}
        
        response = authenticated_client.post(url, data, format='json')
        # Un non-contributeur reçoit 404 (projet non trouvé pour lui)
        # car il n'a pas accès au projet
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_project_by_author(self, authenticated_client, create_project):
        """Test de modification par l'auteur"""
        project = create_project(author=authenticated_client.user)
        url = reverse('project-detail', kwargs={'pk': project.id})
        data = {
            'name': 'Updated Name',
            'description': 'Updated description',
            'type': 'iOS'
        }
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        project.refresh_from_db()
        assert project.name == 'Updated Name'
        assert project.type == 'iOS'
    
    def test_delete_project_by_author(self, authenticated_client, create_project):
        """Test de suppression par l'auteur"""
        project = create_project(author=authenticated_client.user)
        url = reverse('project-detail', kwargs={'pk': project.id})
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Project.objects.filter(id=project.id).exists()
    
    def test_contributor_cannot_update_project(self, authenticated_client, create_project, create_user):
        """Test qu'un contributeur non-auteur ne peut pas modifier"""
        author = create_user(username='projectauthor')
        project = create_project(author=author)
        
        # Ajouter l'utilisateur comme contributeur
        Contributor.objects.create(project=project, user=authenticated_client.user)
        
        url = reverse('project-detail', kwargs={'pk': project.id})
        data = {'name': 'Hacked Name'}
        
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestIssues:
    """Tests pour la gestion des issues"""
    
    def test_create_issue_as_contributor(self, authenticated_client, create_project):
        """Test de création d'une issue par un contributeur"""
        project = create_project(author=authenticated_client.user)
        url = reverse('project-issues-list', kwargs={'project_pk': project.id})
        data = {
            'name': 'Bug Fix',
            'description': 'Description of the bug',
            'priority': 'HIGH',
            'tag': 'BUG',
            'status': 'To Do'
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Bug Fix'
        assert response.data['priority'] == 'HIGH'
        assert response.data['tag'] == 'BUG'
        assert response.data['author']['id'] == authenticated_client.user.id
    
    def test_assign_issue_to_contributor(self, authenticated_client, create_project, create_user):
        """Test d'assignation d'une issue à un contributeur"""
        project = create_project(author=authenticated_client.user)
        assignee = create_user(username='assignee')
        Contributor.objects.create(project=project, user=assignee)
        
        url = reverse('project-issues-list', kwargs={'project_pk': project.id})
        data = {
            'name': 'Assigned Task',
            'description': 'Task description',
            'priority': 'MEDIUM',
            'tag': 'TASK',
            'assigned_to': assignee.id
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['assigned_to'] == assignee.id
    
    def test_cannot_assign_to_non_contributor(self, authenticated_client, create_project, create_user):
        """Test qu'on ne peut pas assigner à un non-contributeur"""
        project = create_project(author=authenticated_client.user)
        non_contributor = create_user(username='noncontrib')
        
        url = reverse('project-issues-list', kwargs={'project_pk': project.id})
        data = {
            'name': 'Task',
            'description': 'Description',
            'priority': 'LOW',
            'tag': 'TASK',
            'assigned_to': non_contributor.id
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_update_issue_by_author(self, authenticated_client, create_project, create_issue):
        """Test de modification d'une issue par son auteur"""
        project = create_project(author=authenticated_client.user)
        issue = create_issue(project=project, author=authenticated_client.user)
        
        url = reverse('project-issues-detail', kwargs={
            'project_pk': project.id,
            'pk': issue.id
        })
        data = {'status': 'In Progress'}
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'In Progress'
    
    def test_project_author_can_update_any_issue(self, authenticated_client, create_project, create_user, create_issue):
        """Test que l'auteur du projet peut modifier toute issue"""
        project = create_project(author=authenticated_client.user)
        other_user = create_user(username='issueauthor')
        Contributor.objects.create(project=project, user=other_user)
        
        # Issue créée par un autre utilisateur
        issue = create_issue(project=project, author=other_user)
        
        url = reverse('project-issues-detail', kwargs={
            'project_pk': project.id,
            'pk': issue.id
        })
        data = {'status': 'Finished'}
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'Finished'
    
    def test_contributor_cannot_update_others_issue(self, authenticated_client, create_project, create_user, create_issue):
        """Test qu'un contributeur ne peut pas modifier l'issue d'un autre"""
        author = create_user(username='projectauthor')
        project = create_project(author=author)
        
        # Ajouter l'utilisateur comme contributeur
        Contributor.objects.create(project=project, user=authenticated_client.user)
        
        # Issue créée par l'auteur du projet
        issue = create_issue(project=project, author=author)
        
        url = reverse('project-issues-detail', kwargs={
            'project_pk': project.id,
            'pk': issue.id
        })
        data = {'status': 'Finished'}
        
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_list_project_issues(self, authenticated_client, create_project, create_issue):
        """Test de listing des issues d'un projet"""
        project = create_project(author=authenticated_client.user)
        
        # Créer plusieurs issues
        for i in range(3):
            create_issue(
                name=f'Issue {i}',
                project=project,
                author=authenticated_client.user
            )
        
        url = reverse('project-issues-list', kwargs={'project_pk': project.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_non_contributor_cannot_see_issues(self, authenticated_client, create_project, create_user, create_issue):
        """Test qu'un non-contributeur ne peut pas voir les issues"""
        other_user = create_user(username='otheruser')
        project = create_project(author=other_user)
        _ = create_issue(project=project, author=other_user)
        
        url = reverse('project-issues-list', kwargs={'project_pk': project.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestComments:
    """Tests pour la gestion des commentaires"""
    
    def test_create_comment(self, authenticated_client, create_project, create_issue):
        """Test de création d'un commentaire"""
        project = create_project(author=authenticated_client.user)
        issue = create_issue(project=project, author=authenticated_client.user)
        
        url = reverse('issue-comments-list', kwargs={
            'project_pk': project.id,
            'issue_pk': issue.id
        })
        data = {'description': 'This is a comment on the issue'}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['description'] == 'This is a comment on the issue'
        assert response.data['author']['id'] == authenticated_client.user.id
    
    def test_update_comment_by_author(self, authenticated_client, create_project, create_issue):
        """Test de modification d'un commentaire par son auteur"""
        project = create_project(author=authenticated_client.user)
        issue = create_issue(project=project, author=authenticated_client.user)
        comment = Comment.objects.create(
            description='Original comment',
            issue=issue,
            author=authenticated_client.user
        )
        
        url = reverse('issue-comments-detail', kwargs={
            'project_pk': project.id,
            'issue_pk': issue.id,
            'pk': comment.id
        })
        data = {'description': 'Updated comment'}
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == 'Updated comment'
    
    def test_delete_comment_by_author(self, authenticated_client, create_project, create_issue):
        """Test de suppression d'un commentaire par son auteur"""
        project = create_project(author=authenticated_client.user)
        issue = create_issue(project=project, author=authenticated_client.user)
        comment = Comment.objects.create(
            description='Comment to delete',
            issue=issue,
            author=authenticated_client.user
        )
        
        url = reverse('issue-comments-detail', kwargs={
            'project_pk': project.id,
            'issue_pk': issue.id,
            'pk': comment.id
        })
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=comment.id).exists()
    
    def test_delete_comment_by_project_author(self, authenticated_client, create_project, create_user, create_issue):
        """Test que l'auteur du projet peut supprimer n'importe quel commentaire"""
        project = create_project(author=authenticated_client.user)
        other_user = create_user(username='commenter')
        Contributor.objects.create(project=project, user=other_user)
        
        issue = create_issue(project=project, author=authenticated_client.user)
        comment = Comment.objects.create(
            description='Comment by other user',
            issue=issue,
            author=other_user
        )
        
        url = reverse('issue-comments-detail', kwargs={
            'project_pk': project.id,
            'issue_pk': issue.id,
            'pk': comment.id
        })
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=comment.id).exists()
    
    def test_contributor_cannot_delete_others_comment(self, authenticated_client, create_project, create_user, create_issue):
        """Test qu'un contributeur ne peut pas supprimer le commentaire d'un autre"""
        author = create_user(username='projectauthor')
        project = create_project(author=author)
        
        # Ajouter l'utilisateur comme contributeur
        Contributor.objects.create(project=project, user=authenticated_client.user)
        
        issue = create_issue(project=project, author=author)
        comment = Comment.objects.create(
            description='Comment by project author',
            issue=issue,
            author=author
        )
        
        url = reverse('issue-comments-detail', kwargs={
            'project_pk': project.id,
            'issue_pk': issue.id,
            'pk': comment.id
        })
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Comment.objects.filter(id=comment.id).exists()
    
    def test_list_issue_comments(self, authenticated_client, create_project, create_issue):
        """Test de listing des commentaires d'une issue"""
        project = create_project(author=authenticated_client.user)
        issue = create_issue(project=project, author=authenticated_client.user)
        
        # Créer plusieurs commentaires
        for i in range(3):
            Comment.objects.create(
                description=f'Comment {i}',
                issue=issue,
                author=authenticated_client.user
            )
        
        url = reverse('issue-comments-list', kwargs={
            'project_pk': project.id,
            'issue_pk': issue.id
        })
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_non_contributor_cannot_comment(self, authenticated_client, create_project, create_user, create_issue):
        """Test qu'un non-contributeur ne peut pas commenter"""
        other_user = create_user(username='projectowner')
        project = create_project(author=other_user)
        issue = create_issue(project=project, author=other_user)
        
        url = reverse('issue-comments-list', kwargs={
            'project_pk': project.id,
            'issue_pk': issue.id
        })
        data = {'description': 'Unauthorized comment'}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestPermissions:
    """Tests spécifiques pour les permissions et cas limites"""
    
    def test_unauthenticated_cannot_access_anything(self, api_client):
        """Test qu'un utilisateur non authentifié ne peut rien faire"""
        urls = [
            reverse('project-list'),
            reverse('user-list'),
        ]
        
        for url in urls:
            response = api_client.get(url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_project_types_validation(self, authenticated_client):
        """Test de tous les types de projets valides"""
        valid_types = ['back-end', 'front-end', 'iOS', 'Android']
        
        for project_type in valid_types:
            url = reverse('project-list')
            data = {
                'name': f'Project {project_type}',
                'description': f'Testing {project_type} type',
                'type': project_type
            }
            
            response = authenticated_client.post(url, data, format='json')
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['type'] == project_type
    
    def test_issue_priorities_and_tags(self, authenticated_client, create_project):
        """Test de toutes les priorités et tags valides"""
        project = create_project(author=authenticated_client.user)
        url = reverse('project-issues-list', kwargs={'project_pk': project.id})
        
        priorities = ['LOW', 'MEDIUM', 'HIGH']
        tags = ['BUG', 'FEATURE', 'TASK']
        issue_statuses = ['To Do', 'In Progress', 'Finished']  # Renommé pour éviter confusion
        
        for i, (priority, tag, issue_status) in enumerate(zip(priorities, tags, issue_statuses)):
            data = {
                'name': f'Issue {i}',
                'description': f'Testing {priority} {tag}',
                'priority': priority,
                'tag': tag,
                'status': issue_status
            }
            
            response = authenticated_client.post(url, data, format='json')
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data['priority'] == priority
            assert response.data['tag'] == tag