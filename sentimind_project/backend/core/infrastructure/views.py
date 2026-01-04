from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Post
from core.infrastructure.serializers import PostSerializer
from core.application.ai_service import MiningEngine


class PostListCreateView(generics.ListCreateAPIView):
    """
    Endpoint principal:
    - GET: Lista posts con filtro por categoría (?category=Gracioso)
    - POST: Crea un post y ejecuta la IA automáticamente.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']  # ¡Magia! Permite filtrar por URL

    def create(self, request, *args, **kwargs):
        content = request.data.get('content')
        
        if not content or len(content.strip()) < 3:
            return Response(
                {"error": "El contenido debe tener al menos 3 caracteres"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 1. Llamar a la capa de minería (Lógica de Negocio)
        analysis = MiningEngine.analyze(content)
        
        # 2. Crear la entidad con los datos de la IA
        post = Post.objects.create(
            content=content,
            category=analysis['top_category'],
            confidence=analysis['confidence']
        )
        
        # 3. Serializar respuesta
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryListView(generics.GenericAPIView):
    """
    Endpoint para obtener las categorías disponibles.
    """
    def get(self, request):
        return Response({
            "categories": MiningEngine.TAXONOMY
        })
