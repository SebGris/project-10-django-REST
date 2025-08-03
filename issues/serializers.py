from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Contributor, Issue, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared']
        read_only_fields = ['id']


class UserSummarySerializer(serializers.ModelSerializer):
    """Serializer minimal pour afficher un résumé utilisateur"""
    class Meta:
        model = User
        fields = ['id', 'username']


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les contributeurs d'un projet"""
    user = UserSummarySerializer(read_only=True)  # Utiliser UserSummarySerializer au lieu de UserSerializer
    
    class Meta:
        model = Contributor
        fields = ['user', 'created_time']
        read_only_fields = ['id', 'created_time']


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des projets"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    contributors_count = serializers.SerializerMethodField()
    contributors_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'author_username', 'contributors_count', 'contributors_names', 'created_time']
        read_only_fields = ['id', 'created_time']
    
    def get_contributors_count(self, obj):
        """Retourne le nombre de contributeurs"""
        return obj.contributors.count()
    
    def get_contributors_names(self, obj):
        """Retourne la liste des noms des contributeurs"""
        return [contributor.user.username for contributor in obj.contributors.all()]


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer complet pour le détail d'un projet"""
    author = UserSummarySerializer(read_only=True)  # Utiliser UserSummarySerializer pour cohérence
    contributors = ContributorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']
    
    def create(self, validated_data):
        """Créer un projet et ajouter l'auteur comme contributeur"""
        user = self.context['request'].user
        validated_data.pop('author', None)
        # La méthode save() du modèle s'occupera d'ajouter l'auteur comme contributeur
        project = Project.objects.create(author=user, **validated_data)
        return project


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la création/modification de projets"""
    class Meta:
        model = Project
        fields = ['name', 'description', 'type']
        
    def validate_type(self, value):
        """Valider le type de projet"""
        valid_types = ['back-end', 'front-end', 'iOS', 'Android']
        if value not in valid_types:
            raise serializers.ValidationError(f"Type invalide. Choisir parmi: {valid_types}")
        return value


class IssueListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des issues"""
    author = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Issue
        fields = ['id', 'name', 'priority', 'tag', 'status', 'author', 'created_time']


class IssueSerializer(serializers.ModelSerializer):
    """Serializer complet pour le détail d'une issue"""
    author = UserSerializer(read_only=True)
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

    def validate_assigned_to(self, value):
        """Valider que l'utilisateur assigné existe et est contributeur du projet"""
        if value is not None:
            # La validation du contributeur sera faite dans la vue
            # car on n'a pas accès au projet ici lors de la création
            pass
        return value
    
    def update(self, instance, validated_data):
        """Mettre à jour une issue en gérant assigned_to_id"""
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        if assigned_to_id is not None:
            if assigned_to_id == 0:  # Désassigner
                instance.assigned_to = None
            else:
                try:
                    instance.assigned_to = User.objects.get(id=assigned_to_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError("Utilisateur assigné non trouvé.")
        
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Comment"""
    author = UserSummarySerializer(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)  # En lecture seule
    project = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'description', 'project', 'issue', 'author', 'created_time']
        read_only_fields = ['id', 'author', 'project', 'issue', 'created_time']
    
    def get_project(self, obj):
        """Retourne l'ID du projet associé à l'issue"""
        return obj.issue.project.id