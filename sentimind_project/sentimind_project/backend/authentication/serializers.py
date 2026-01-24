"""
Serializers para autenticación JWT.
Incluye: Registro, Login, Perfil de usuario, Reset de contraseña.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para incluir datos del usuario en el token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar datos personalizados al token
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Agregar datos del usuario a la respuesta
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de nuevos usuarios.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden."
            })
        
        # Verificar que el email no esté en uso
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                "email": "Este email ya está registrado."
            })
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para datos del usuario actual.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para cambio de contraseña.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Las nuevas contraseñas no coinciden."
            })
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer para solicitar reset de contraseña.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No existe una cuenta con este email.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer para confirmar reset de contraseña.
    """
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Las contraseñas no coinciden."
            })
        return attrs
