from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from core.models import Post, Category, PostCategory
from core.infrastructure.serializers import PostSerializer
from core.application.ai_service import MiningEngine
import traceback

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Permite lectura a todos, escritura solo a autenticados."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class PostListCreateView(generics.ListCreateAPIView):
    """
    Endpoint principal:
    - GET: Lista posts con filtro por categoria
    - POST: Crea un post y ejecuta la IA automaticamente
    """
    queryset = Post.objects.select_related('author').prefetch_related('post_categories__category').all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primary_category']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Permite filtrar por cualquier categoria."""
        queryset = super().get_queryset()
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories__name=category).distinct()
        
        # Filtro por posts propios
        mine = self.request.query_params.get('mine')
        if mine and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
        
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            content = request.data.get('content')
            
            if not content or len(content.strip()) < 3:
                return Response(
                    {"error": "El contenido debe tener al menos 3 caracteres"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 1. Llamar a la capa de mineria
            try:
                analysis = MiningEngine.analyze(content)
            except Exception as e:
                print(f"Error en analisis: {e}")
                traceback.print_exc()
                analysis = {
                    "categories": [{"name": "Reflexion", "confidence": 0.5}],
                    "primary_category": "Reflexion",
                    "primary_confidence": 0.5,
                    "method": "fallback-error"
                }
            
            # 2. Crear la entidad Post con el autor
            post = Post.objects.create(
                content=content,
                author=request.user if request.user.is_authenticated else None,
                primary_category=analysis['primary_category'],
                primary_confidence=analysis['primary_confidence']
            )
            
            # 3. Crear las relaciones con las categorias detectadas
            for cat_data in analysis['categories']:
                category, _ = Category.objects.get_or_create(name=cat_data['name'])
                PostCategory.objects.create(
                    post=post,
                    category=category,
                    confidence=cat_data['confidence']
                )
            
            # 4. Serializar respuesta
            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error creando post: {e}")
            traceback.print_exc()
            return Response(
                {"error": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryListView(generics.GenericAPIView):
    """
    Endpoint para obtener las categorías disponibles.
    """
    def get(self, request):
        return Response({
            "categories": MiningEngine.TAXONOMY
        })
