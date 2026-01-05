from transformers import pipeline


class MiningEngine:
    """
    Motor de Minería de Texto basado en Transformers.
    Patrón Singleton para cargar el modelo en memoria una sola vez.
    
    Características:
    - Clasificación Zero-Shot multilingüe (optimizado para español)
    - Soporte multi-label (un post puede tener múltiples emociones)
    - Umbral configurable para detectar emociones secundarias
    """
    
    # Lista expandida de categorías para la red social (25 categorías)
    TAXONOMY = [
        # Emociones básicas
        "Alegría", "Tristeza", "Enojo", "Miedo", "Sorpresa", "Asco",
        # Emociones sociales
        "Amor", "Odio", "Vergüenza", "Orgullo", "Envidia", "Celos",
        # Tipos de contenido
        "Humor", "Inspiración", "Confesión", "Queja", "Consejo",
        "Pregunta", "Reflexión", "Nostalgia", "Ansiedad", "Frustración",
        # Contenido especial
        "Sarcasmo", "Polémica", "Terror"
    ]
    
    # Mapeo de etiquetas a hypothesis templates en español para mejor precisión
    HYPOTHESIS_TEMPLATE = "Este texto expresa {}"
    
    # Umbral mínimo de confianza (porcentaje del score máximo)
    # Una emoción secundaria debe tener al menos 97% del score de la primaria
    RELATIVE_THRESHOLD = 0.97
    
    # Máximo de emociones a retornar
    MAX_EMOTIONS = 3

    _classifier = None

    @classmethod
    def get_classifier(cls):
        if cls._classifier is None:
            # Modelo multilingüe optimizado para Zero-Shot en español
            print("🧠 Cargando modelo neuronal multilingüe... (esto pasa solo una vez)")
            cls._classifier = pipeline(
                "zero-shot-classification", 
                #model="facebook/bart-large-mnli"
                model="joeddav/xlm-roberta-large-xnli",  # Modelo multilingüe!
                device=-1  # CPU (cambiar a 0 para GPU)
            )
            print("✅ Modelo multilingüe cargado exitosamente!")
        return cls._classifier

    @classmethod
    def analyze(cls, text: str) -> dict:
        """
        Analiza un texto y retorna múltiples emociones detectadas.
        
        Returns:
            dict: {
                "categories": ["Alegría", "Humor"],  # Lista de categorías detectadas
                "primary_category": "Alegría",       # Categoría principal
                "primary_confidence": 0.85,          # Confianza de la principal
                "all_scores": {...}                  # Todos los scores
            }
        """
        classifier = cls.get_classifier()
        
        # Inferencia con multi_label=True para detectar múltiples emociones
        result = classifier(
            text, 
            cls.TAXONOMY, 
            hypothesis_template=cls.HYPOTHESIS_TEMPLATE,
            multi_label=True  # ¡Permite múltiples categorías!
        )
        
        # Crear diccionario de scores
        all_scores = dict(zip(result['labels'], result['scores']))
        
        # Obtener el score máximo para calcular umbrales relativos
        max_score = result['scores'][0]
        threshold = max_score * cls.RELATIVE_THRESHOLD
        
        # Filtrar emociones que superen el umbral relativo
        detected_categories = []
        for label, score in zip(result['labels'], result['scores']):
            if score >= threshold and len(detected_categories) < cls.MAX_EMOTIONS:
                detected_categories.append({
                    "name": label,
                    "confidence": score
                })
        
        # Si ninguna supera el umbral, tomar la más alta
        if not detected_categories:
            detected_categories = [{
                "name": result['labels'][0],
                "confidence": result['scores'][0]
            }]
        
        return {
            "categories": detected_categories,  # Lista de categorías con confianza
            "primary_category": result['labels'][0],
            "primary_confidence": result['scores'][0],
            "all_scores": all_scores,
            # Mantener compatibilidad con versión anterior
            "top_category": result['labels'][0],
            "confidence": result['scores'][0]
        }
