"""softdesk_support URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """
    Page d'accueil de l'API SoftDesk Support
    """
    return Response({
        'message': 'Bienvenue sur l\'API SoftDesk Support',
        'description': 'API de gestion des problèmes techniques',
        'endpoints': {
            'admin': reverse('admin:index', request=request, format=format),
            'api_auth': {
                'login': request.build_absolute_uri('/api-auth/login/'),
                'logout': request.build_absolute_uri('/api-auth/logout/'),
            }
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
