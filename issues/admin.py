from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Administration pour les projets"""

    list_display = ("id", "name", "type", "author", "created_time")
    list_filter = ("type", "created_time")
    search_fields = ("name", "description")
    readonly_fields = ("created_time",)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    """Administration pour les contributeurs"""

    list_display = ("id", "user", "project", "created_time")
    list_filter = ("created_time",)
    search_fields = ("user__username", "project__name")


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Administration pour les issues"""

    list_display = (
        "id",
        "name",
        "project",
        "priority",
        "tag",
        "status",
        "author",
        "assigned_to",
        "created_time",
    )
    list_filter = ("priority", "tag", "status", "created_time")
    search_fields = ("name", "description", "project__name")
    readonly_fields = ("created_time",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Administration pour les commentaires"""

    list_display = ("id", "issue", "author", "created_time")
    list_filter = ("created_time",)
    search_fields = ("description", "issue__name", "author__username")
    readonly_fields = ("id", "created_time")
