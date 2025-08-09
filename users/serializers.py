from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()  # Récupère le modèle User configuré dans settings.py


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle User"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'age',
            'can_be_contacted', 'can_data_be_shared'
        ]
        read_only_fields = ['id']


class UserSummarySerializer(serializers.ModelSerializer):
    """Serializer minimal pour afficher un résumé utilisateur"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared']


class UserMiniSerializer(serializers.ModelSerializer):
    """Serializer minimal pour afficher uniquement id, username, email"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un nouvel utilisateur"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'age', 
                  'can_be_contacted', 'can_data_be_shared']
    
    def validate_age(self, value):
        """Valider que l'utilisateur a au moins 15 ans"""
        if value < 15:
            raise serializers.ValidationError(
                "L'utilisateur doit avoir au moins 15 ans."
            )
        return value
    
    def validate(self, attrs):
        """Valider que les mots de passe correspondent"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        """Créer un nouvel utilisateur"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour du profil utilisateur"""
    class Meta:
        model = User
        fields = ['email', 'age', 'can_be_contacted', 'can_data_be_shared']
        
    def validate_age(self, value):
        """Valider que l'utilisateur a au moins 15 ans"""
        if value < 15:
            raise serializers.ValidationError(
                "L'utilisateur doit avoir au moins 15 ans."
            )
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'utilisateur avec validation RGPD"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    age = serializers.IntegerField(min_value=15, error_messages={
        'min_value': 'L\'âge minimum requis est de 15 ans (conformité RGPD).'
    })
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'age', 'can_be_contacted', 'can_data_be_shared',
            'password', 'password_confirm'
        ]
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
