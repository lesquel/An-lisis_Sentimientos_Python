from rest_framework import serializers
from core.models import Post, Category, PostCategory


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías."""
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostCategorySerializer(serializers.ModelSerializer):
    """Serializer para la relación Post-Category con confianza."""
    name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = PostCategory
        fields = ['name', 'confidence']


class AuthorSerializer(serializers.Serializer):
    """Serializer para informacion del autor."""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer para convertir Post a JSON y viceversa.
    Incluye las multiples categorias detectadas.
    """
    categories = PostCategorySerializer(source='post_categories', many=True, read_only=True)
    # Mantener compatibilidad: category = primary_category
    category = serializers.CharField(source='primary_category', read_only=True)
    confidence = serializers.FloatField(source='primary_confidence', read_only=True)
    # Informacion del autor
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'content', 
            'author',  # Nuevo: informacion del autor
            'category', 'confidence',  # Compatibilidad con frontend existente
            'primary_category', 'primary_confidence',
            'categories',  # Nueva: lista de todas las categorias
            'created_at'
        ]
        read_only_fields = ['id', 'author', 'category', 'confidence', 'primary_category', 
                           'primary_confidence', 'categories', 'created_at']


class PostCreateSerializer(serializers.Serializer):
    """
    Serializer para validar la entrada de creación de posts.
    """
    content = serializers.CharField(min_length=3, max_length=1000)
