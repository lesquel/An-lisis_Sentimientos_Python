from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from core.models import Post, Category, PostCategory
from core.infrastructure.serializers import PostSerializer
from core.application.ai_service import MiningEngine
import traceback


class PostListCreateView(generics.ListCreateAPIView):
    """
    Endpoint principal:
    - GET: Lista posts con filtro por categoría (?category=Alegría o ?primary_category=Alegría)
    - POST: Crea un post y ejecuta la IA automáticamente (detecta múltiples emociones).
    """
    queryset = Post.objects.prefetch_related('post_categories__category').all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primary_category']  # Filtrar por categoría principal

    def get_queryset(self):
        """Permite filtrar por cualquier categoría (no solo la principal)."""
        queryset = super().get_queryset()
        
        # Filtro adicional: posts que contengan una categoría específica
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories__name=category).distinct()
        
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
            
            # 1. Llamar a la capa de minería (Lógica de Negocio)
            try:
                analysis = MiningEngine.analyze(content)
            except Exception as e:
                print(f"⚠️ Error en análisis: {e}")
                traceback.print_exc()
                # Fallback: crear post sin categorización
                analysis = {
                    "categories": [{"name": "Reflexión", "confidence": 0.5}],
                    "primary_category": "Reflexión",
                    "primary_confidence": 0.5,
                    "method": "fallback-error"
                }
            
            # 2. Crear la entidad Post
            post = Post.objects.create(
                content=content,
                primary_category=analysis['primary_category'],
                primary_confidence=analysis['primary_confidence']
            )
            
            # 3. Crear las relaciones con las categorías detectadas
            for cat_data in analysis['categories']:
                # Obtener o crear la categoría
                category, _ = Category.objects.get_or_create(name=cat_data['name'])
                
                # Crear la relación Post-Category
                PostCategory.objects.create(
                    post=post,
                    category=category,
                    confidence=cat_data['confidence']
                )
            
            # 4. Serializar respuesta
            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ Error creando post: {e}")
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
