from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Categoría/Emoción detectada por la IA.
    Separada para permitir relación muchos-a-muchos con Post.
    """
    name = models.CharField(max_length=50, unique=True, db_index=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Entidad principal. Representa una publicacion en el muro.
    Soporta multiples emociones/categorias por post.
    """
    content = models.TextField(help_text="El mensaje del usuario")
    
    # Autor del post (opcional para compatibilidad con posts anonimos)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
        help_text="Usuario que creo el post"
    )
    
    # Relacion muchos-a-muchos con categorias (a traves de PostCategory)
    categories = models.ManyToManyField(
        Category, 
        through='PostCategory',
        related_name='posts'
    )
    
    # Categoria principal (la de mayor confianza) - para filtrado rapido
    primary_category = models.CharField(max_length=50, db_index=True)
    
    # Confianza de la categoria principal
    primary_confidence = models.FloatField()
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.primary_category}] {self.content[:30]}..."
    
    def get_categories_list(self):
        """Retorna lista de categorías con sus confianzas."""
        return list(self.post_categories.values('category__name', 'confidence'))


class PostCategory(models.Model):
    """
    Tabla intermedia para la relación Post-Category.
    Almacena la confianza de cada categoría para cada post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')
    confidence = models.FloatField(help_text="Nivel de confianza (0-1)")
    
    class Meta:
        unique_together = ('post', 'category')
        ordering = ['-confidence']
    
    def __str__(self):
        return f"{self.post.id} - {self.category.name}: {self.confidence:.2%}"
