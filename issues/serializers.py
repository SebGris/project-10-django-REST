from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, UserMiniSerializer
from .models import Project, Contributor, Issue, Comment

User = get_user_model()


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les contributeurs d'un projet"""
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'user_id', 'project', 'created_time']
        read_only_fields = ['project', 'created_time']
    
    def validate(self, attrs):
        """Valide qu'un contributeur n'existe pas déjà pour ce projet"""
        user = attrs.get('user')
        project = self.context.get('project') or getattr(self.instance, 'project', None)
        
        if user and project:
            # Pour la création uniquement (pas la mise à jour)
            if not self.instance and Contributor.objects.filter(user=user, project=project).exists():
                raise serializers.ValidationError(
                    "Cet utilisateur est déjà contributeur de ce projet."
                )
        
        return attrs


class AddContributorSerializer(serializers.Serializer):
    """Serializer pour ajouter un contributeur à un projet"""
    user_id = serializers.IntegerField(required=True)
    
    def validate_user_id(self, value):
        """Valide que l'utilisateur existe"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f"L'utilisateur avec l'ID {value} n'existe pas."
            )
        return value
    
    def validate(self, attrs):
        """Validation : vérifier que l'utilisateur n'est pas déjà contributeur"""
        user_id = attrs.get('user_id')
        project = self.context.get('project')
        
        if project and Contributor.objects.filter(user_id=user_id, project=project).exists():
            raise serializers.ValidationError({
                'user_id': "Cet utilisateur est déjà contributeur de ce projet."
            })
        
        return attrs
    
    def create(self, validated_data):
        """Crée le contributeur"""
        project = self.context.get('project')
        user_id = validated_data.get('user_id')
        user = User.objects.get(id=user_id)
        
        return Contributor.objects.create(user=user, project=project)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer complet pour le détail d'un projet"""
    author = UserSerializer(read_only=True)
    contributors = serializers.SerializerMethodField()
    issues_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'type', 'author', 
            'contributors', 'created_time', 'issues_count'
        ]
        read_only_fields = ['id', 'created_time']
    
    def get_issues_count(self, obj):
        """Nombre d'issues du projet"""
        return obj.issues.count()
    
    def get_contributors(self, obj):
        """Retourne la liste des utilisateurs contributeurs"""
        # Récupérer les users via la relation Contributor
        users = User.objects.filter(contributor__project=obj)
        return UserSerializer(users, many=True).data


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des projets"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    contributors_count = serializers.SerializerMethodField()
    contributors_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'type', 'author_username',
            'contributors_count', 'contributors_names', 'created_time'
        ]
        read_only_fields = ['id', 'created_time']
    
    def get_contributors_count(self, obj):
        """Retourne le nombre de contributeurs"""
        return obj.contributors.count()
    
    def get_contributors_names(self, obj):
        """Retourne la liste des noms des contributeurs"""
        # Optimisation : utiliser values_list pour éviter de charger tout l'objet
        return list(obj.contributors.values_list('user__username', flat=True))
    

class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la création/modification de projets"""
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type']
        read_only_fields = ['id']
        
    def validate_name(self, value):
        """Validation du nom"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Le nom du projet doit contenir au moins 3 caractères."
            )
        return value.strip()
    
    def validate_description(self, value):
        """Validation de la description"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "La description doit contenir au moins 10 caractères."
            )
        return value.strip()
    
    def validate_type(self, value):
        """Valider le type de projet"""
        valid_types = ['back-end', 'front-end', 'iOS', 'Android']
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Type invalide. Choisir parmi: {valid_types}"
            )
        return value


class IssueListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des issues"""
    author = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Issue
        fields = ['id', 'name', 'priority', 'tag', 'status', 'author', 'created_time']


class IssueSerializer(serializers.ModelSerializer):
    """Serializer complet pour le détail d'une issue"""
    author = UserMiniSerializer(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    assigned_to_details = UserMiniSerializer(source='assigned_to', read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Issue
        fields = [
            'id', 'name', 'description', 'priority', 'tag', 'status', 
            'project', 'author', 'assigned_to', 'assigned_to_details', 'created_time'
        ]
        read_only_fields = ['id', 'author', 'project', 'created_time']

    def validate_assigned_to(self, value):
        """Valider que l'utilisateur assigné est contributeur du projet"""
        if value:
            request = self.context.get('request')
            view = self.context.get('view')
            
            if view and hasattr(view, 'kwargs'):
                project_id = view.kwargs.get('project_pk')
                if project_id:
                    # Vérifier que l'assigné est contributeur
                    if not Contributor.objects.filter(user=value, project_id=project_id).exists():
                        raise serializers.ValidationError(
                            "L'utilisateur assigné doit être contributeur du projet."
                        )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Comment"""
    author = UserMiniSerializer(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)
    issue_name = serializers.CharField(source='issue.name', read_only=True)
    project_id = serializers.IntegerField(source='issue.project.id', read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'project_id', 'issue', 
            'issue_name', 'author', 'created_time'
        ]
        read_only_fields = ['id', 'author', 'project_id', 'issue', 'issue_name', 'created_time']
    
    def validate_description(self, value):
        """Validation de la description"""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Le commentaire ne peut pas être vide."
            )
        if len(value.strip()) > 2000:
            raise serializers.ValidationError(
                "Le commentaire ne peut pas dépasser 2000 caractères."
            )
        return value.strip()