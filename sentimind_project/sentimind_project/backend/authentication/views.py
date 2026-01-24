"""
Vistas de autenticación para SentiMind.
Implementa: Registro, Login, Logout, Perfil, Cambio de contraseña, Reset de contraseña.
"""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para login con JWT.
    POST /api/auth/login/
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    Vista para registro de nuevos usuarios.
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens para el nuevo usuario
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
    Vista para logout (invalida el refresh token).
    POST /api/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'message': 'Sesión cerrada exitosamente'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Token inválido'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vista para obtener/actualizar perfil del usuario actual.
    GET/PUT /api/auth/me/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    Vista para cambiar contraseña.
    PUT /api/auth/change-password/
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña actualizada exitosamente'
        }, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """
    Vista para solicitar reset de contraseña.
    POST /api/auth/password-reset/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generar token de reset
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # En producción, aquí se enviaría un email con el enlace
        # Por ahora, retornamos el token directamente para testing
        reset_link = f"/reset-password/{uid}/{token}/"
        
        return Response({
            'message': 'Se ha enviado un enlace de recuperación a tu email',
            'debug': {
                'uid': uid,
                'token': token,
                'reset_link': reset_link
            }
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Vista para confirmar reset de contraseña.
    POST /api/auth/password-reset-confirm/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uid = request.data.get('uid')
        token = request.data.get('token')
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Enlace de recuperación inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({
                'error': 'El enlace de recuperación ha expirado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña restablecida exitosamente'
        }, status=status.HTTP_200_OK)
