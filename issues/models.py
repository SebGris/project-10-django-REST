import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec gestion RGPD et âge
    """
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(15)],
        null=True,
        blank=True,
        help_text="L'utilisateur doit avoir au moins 15 ans (RGPD)"
    )
    can_be_contacted = models.BooleanField(
        default=False,
        help_text="L'utilisateur peut-il être contacté ?"
    )
    can_data_be_shared = models.BooleanField(
        default=False,
        help_text="Les données de l'utilisateur peuvent-elles être partagées ?"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Project(models.Model):
    """
    Modèle pour les projets d'applications clientes
    """
    PROJECT_TYPES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='authored_projects'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """
    Modèle pour les contributeurs d'un projet spécifique
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'], 
                name='unique_user_project_contributor'
            )
        ]  # Un utilisateur ne peut être contributeur qu'une fois par projet, évite les doublons dans la table

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


class Issue(models.Model):
    """
    Modèle pour les problèmes/tâches d'un projet
    """
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]

    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='LOW')
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='To Do')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='authored_issues'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_issues',
        help_text="Contributeur à qui l'issue est assignée"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project.name}"


class Comment(models.Model):
    """
    Modèle pour les commentaires d'une issue
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='authored_comments'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.issue.name} by {self.author.username}"
