import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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

    def save(self, *args, **kwargs):
        """
        Surcharge de save pour créer automatiquement l'auteur comme contributeur
        """
        is_new = self.pk is None  # True si c'est une création, False si c'est une mise à jour
        super().save(*args, **kwargs)
        
        # Si c'est un nouveau projet, ajouter l'auteur comme contributeur
        if is_new:
            Contributor.objects.get_or_create(
                user=self.author,
                project=self
            )
    
    def get_all_contributors(self):
        """
        Retourne tous les contributeurs incluant l'auteur
        """
        return self.contributors.all()
    
    def get_non_author_contributors(self):
        """
        Retourne seulement les contributeurs qui ne sont pas l'auteur
        """
        return self.contributors.exclude(user=self.author)
    
    def is_author_or_contributor(self, user):
        """
        Vérifie si un utilisateur est auteur ou contributeur du projet
        """
        return (self.author == user or 
                self.contributors.filter(user=user).exists())
    
    def can_user_access(self, user):
        """
        Vérifie si un utilisateur peut accéder au projet (auteur ou contributeur)
        """
        return self.is_author_or_contributor(user)
    
    def can_user_modify(self, user):
        """
        Vérifie si un utilisateur peut modifier le projet (seul l'auteur)
        """
        return self.author == user
    
    def is_user_contributor(self, user):
        """
        Vérifie si un utilisateur est contributeur de ce projet
        """
        return self.contributors.filter(user=user).exists() or user == self.author

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

    @property
    def is_author(self):
        """
        Vérifie si ce contributeur est aussi l'auteur du projet
        """
        return self.user == self.project.author

    def __str__(self):
        role = " (Auteur)" if self.is_author else ""
        return f"{self.user.username} - {self.project.name}{role}"


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
        return f"Comment on {self.issue.name} by {self.author.username}"
