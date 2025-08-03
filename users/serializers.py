from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User (toutes les informations)
    """
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time', 'password']
        read_only_fields = ['id', 'created_time']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Gérer le mot de passe séparément s'il est fourni
        password = validated_data.pop('password', None)
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Mettre à jour le mot de passe si fourni
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Serializer pour les informations publiques de l'utilisateur
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour la mise à jour du profil (sans mot de passe)
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time']
        read_only_fields = ['id', 'created_time']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription des utilisateurs"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    age = serializers.IntegerField(min_value=15, error_messages={
        'min_value': 'L\'âge minimum requis est de 15 ans (conformité RGPD).'
    })
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'age', 'can_be_contacted', 'can_data_be_shared']
        
    def validate(self, attrs):
        """Validation des données"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        # Validation RGPD - âge minimum
        if attrs.get('age', 0) < 15:
            raise serializers.ValidationError({
                'age': 'Vous devez avoir au moins 15 ans pour vous inscrire (conformité RGPD).'
            })
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSummarySerializer(serializers.ModelSerializer):
    """Serializer pour afficher un résumé des utilisateurs"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared']
        read_only_fields = ['id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared']
        read_only_fields = ['id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'utilisateur avec validation RGPD"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    age = serializers.IntegerField(min_value=15, error_messages={
        'min_value': 'L\'âge minimum requis est de 15 ans (conformité RGPD).'
    })
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                 'age', 'can_be_contacted', 'can_data_be_shared', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': True},
            'age': {'required': True},
        }

    def validate(self, attrs):
        """Validation globale avec vérification de l'âge et des mots de passe"""
        # Vérification de l'âge minimum (RGPD)
        if attrs.get('age', 0) < 15:
            raise serializers.ValidationError({
                "age": "L'âge minimum requis est de 15 ans (conformité RGPD)."
            })
        
        # Vérification des mots de passe
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        
        return attrs

    def create(self, validated_data):
        """Créer l'utilisateur avec le mot de passe hashé"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
