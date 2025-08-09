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
            if (
                not self.instance and
                Contributor.objects.filter(user=user, project=project).exists()
            ):
                raise serializers.ValidationError(
                    "Cet utilisateur est déjà contributeur de ce projet."
                )
        
        return attrs


class AddContributorSerializer(serializers.Serializer):
    """Serializer pour ajouter un contributeur à un projet"""
    user_id = serializers.IntegerField(required=True)
    
    def validate_user_id(self, value):
        """Valide que l'utilisateur existe"""
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("L'utilisateur avec cet ID n'existe pas.")
        return value
    
    def validate(self, attrs):
        """Validation additionnelle"""
        user_id = attrs.get('user_id')
        project = self.context.get('project')
        
        if (
            project
            and Contributor.objects.filter(
                user_id=user_id,
                project=project
            ).exists()
        ):
            raise serializers.ValidationError(
                "Cet utilisateur est déjà contributeur de ce projet."
            )
        
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
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors', 
                  'created_time', 'issues_count']
        read_only_fields = ['id', 'created_time']
    
    def get_issues_count(self, obj):
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
        return [contributor.user.username for contributor in obj.contributors.all()]
    

class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la création/modification de projets"""
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type']
        read_only_fields = ['id']
        
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
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'priority', 'tag', 'status', 
                 'project', 'author', 'assigned_to', 'created_time']
        read_only_fields = ['id', 'author', 'project', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Comment"""
    author = UserMiniSerializer(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'description', 'project', 'issue', 'author', 'created_time']
        read_only_fields = ['id', 'author', 'project', 'issue', 'created_time']
    
    def get_project(self, obj):
        """Retourne l'ID du projet associé à l'issue"""
        return obj.issue.project.id