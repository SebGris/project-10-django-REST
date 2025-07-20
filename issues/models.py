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
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Si c'est un nouveau projet, ajouter l'auteur comme contributeur
        if is_new:
            self.add_author_as_contributor()
    
    def add_author_as_contributor(self):
        """
        Ajoute l'auteur du projet comme contributeur automatiquement
        """
        Contributor.objects.get_or_create(
            user=self.author,
            project=self,
            defaults={'created_time': self.created_time}
        )
    
    def get_all_contributors(self):
        """
        Retourne tous les contributeurs incluant l'auteur
        """
        return self.contributors.all()
    
    def is_author_or_contributor(self, user):
        """
        Vérifie si un utilisateur est auteur ou contributeur du projet
        """
        return (self.author == user or 
                self.contributors.filter(user=user).exists())

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
