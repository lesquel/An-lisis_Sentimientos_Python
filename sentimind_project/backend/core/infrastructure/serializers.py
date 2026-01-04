from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer para convertir Post a JSON y viceversa.
    """
    class Meta:
        model = Post
        fields = ['id', 'content', 'category', 'confidence', 'created_at']
        read_only_fields = ['id', 'category', 'confidence', 'created_at']


class PostCreateSerializer(serializers.Serializer):
    """
    Serializer para validar la entrada de creación de posts.
    """
    content = serializers.CharField(min_length=3, max_length=1000)
