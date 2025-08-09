from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Administration personnalisée pour le modèle User
    """
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name',
        'age', 'created_time', 'is_staff'
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'created_time',
        'can_be_contacted',
        'can_data_be_shared',
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-created_time',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations personnelles supplémentaires', {
            'fields': ('age', 'can_be_contacted', 'can_data_be_shared', 'created_time')
        }),
    )
    
    readonly_fields = ('created_time',)


admin.site.register(User, CustomUserAdmin)
