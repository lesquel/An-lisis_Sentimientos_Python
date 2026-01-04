from django.db import models


class Post(models.Model):
    """
    Entidad principal. Representa una publicación en el muro.
    """
    content = models.TextField(help_text="El mensaje anónimo")
    
    # Categoría predicha (Indexed para filtrado rápido en SQL)
    category = models.CharField(max_length=50, db_index=True)
    
    # Puntuación de confianza (Qué tan segura está la IA)
    confidence = models.FloatField()
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.category}] {self.content[:30]}..."
