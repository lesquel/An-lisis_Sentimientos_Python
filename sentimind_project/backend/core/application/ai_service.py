from transformers import pipeline


class MiningEngine:
    """
    Motor de Minería de Texto basado en Transformers.
    Patrón Singleton para cargar el modelo en memoria una sola vez.
    """
    
    # Lista expandida de categorías para la red social
    TAXONOMY = [
        "Tóxico", "Gracioso", "Inspirador", "Triste", 
        "Romántico", "Polémico", "Asqueroso", "Filosófico", 
        "Confesión", "Queja", "Curiosidad", "Terror"
    ]

    _classifier = None

    @classmethod
    def get_classifier(cls):
        if cls._classifier is None:
            # Modelo multilingüe optimizado para Zero-Shot
            print("🧠 Cargando modelo neuronal... (esto pasa solo una vez)")
            cls._classifier = pipeline(
                "zero-shot-classification", 
                model="facebook/bart-large-mnli"
            )
            print("✅ Modelo cargado exitosamente!")
        return cls._classifier

    @classmethod
    def analyze(cls, text: str) -> dict:
        classifier = cls.get_classifier()
        
        # Inferencia
        result = classifier(text, cls.TAXONOMY, multi_label=False)
        
        return {
            "top_category": result['labels'][0],
            "confidence": result['scores'][0],
            "all_scores": dict(zip(result['labels'], result['scores']))
        }
