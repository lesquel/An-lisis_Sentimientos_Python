import re
import os


class RuleBasedAnalyzer:
    """
    Analizador de sentimientos basado en reglas (keywords).
    Se usa como fallback cuando los modelos de IA no están disponibles.
    """
    
    # Diccionario de palabras clave por categoría (español)
    KEYWORDS = {
        "Alegría": ["feliz", "contento", "alegre", "genial", "maravilloso", "increíble", "fantástico", 
                   "excelente", "bien", "super", "wow", "yay", "jaja", "😊", "😄", "🎉", "❤️", "amor",
                   "gracias", "agradecido", "bendecido", "perfecto", "éxito", "logré", "conseguí"],
        "Tristeza": ["triste", "llorar", "deprimido", "solo", "soledad", "melancolía", "pena", 
                    "dolor", "sufrir", "mal", "😢", "😭", "💔", "extraño", "perdí", "murió", "falleció"],
        "Enojo": ["enojado", "furioso", "molesto", "rabia", "ira", "odio", "maldito", "carajo",
                 "enfadado", "harto", "cansado de", "😠", "😡", "🤬", "injusto", "bronca"],
        "Miedo": ["miedo", "terror", "asustado", "pánico", "nervioso", "ansioso", "preocupado",
                 "temo", "aterrado", "😰", "😨", "😱", "horror", "susto"],
        "Sorpresa": ["sorpresa", "increíble", "no puedo creer", "wow", "impresionante", "inesperado",
                    "😮", "😲", "🤯", "qué", "cómo", "en serio"],
        "Amor": ["amor", "te amo", "te quiero", "enamorado", "cariño", "❤️", "💕", "💗", "😍", 
                "beso", "abrazo", "pareja", "novio", "novia", "esposo", "esposa"],
        "Humor": ["jaja", "jeje", "lol", "😂", "🤣", "gracioso", "chistoso", "divertido", "risa",
                 "broma", "chiste", "meme"],
        "Inspiración": ["motivado", "inspirado", "sueños", "metas", "lograr", "éxito", "adelante",
                       "lucha", "fuerza", "puedo", "💪", "🌟", "✨", "nunca rendirse"],
        "Confesión": ["confieso", "admito", "secreto", "verdad es que", "nunca dije", "oculté"],
        "Queja": ["queja", "mal servicio", "terrible", "pésimo", "horrible", "no funciona", 
                 "decepcionado", "peor", "basura", "estafa"],
        "Consejo": ["consejo", "recomiendo", "deberías", "tip", "sugerencia", "prueba", "intenta"],
        "Pregunta": ["?", "cómo", "qué", "cuál", "cuándo", "dónde", "por qué", "alguien sabe",
                    "ayuda", "pueden", "conocen"],
        "Reflexión": ["pienso", "creo que", "reflexión", "la vida", "sentido", "aprendí", "me doy cuenta"],
        "Nostalgia": ["extraño", "recuerdo", "antes", "aquellos tiempos", "cuando era", "ojalá"],
        "Ansiedad": ["ansiedad", "ansioso", "nervios", "no puedo dormir", "preocupado", "estrés"],
        "Frustración": ["frustrado", "no puedo", "imposible", "ya no sé", "estoy harto", "cansado"],
        "Sarcasmo": ["claro", "obvio", "seguro", "ajá", "sí claro", "como no", "🙄"],
        "Orgullo": ["orgulloso", "logré", "conseguí", "mi hijo", "graduación", "premio"],
        "Vergüenza": ["vergüenza", "pena", "qué oso", "ridículo", "bochorno"],
        "Envidia": ["envidia", "quisiera", "ojalá tuviera", "suerte la tuya"],
        "Asco": ["asco", "asqueroso", "repugnante", "🤮", "qué asco"],
        "Polémica": ["opinión impopular", "polémica", "controversial", "debate", "discusión"],
        "Terror": ["terror", "escalofriante", "pesadilla", "paranormal", "fantasma", "👻", "💀"]
    }
    
    @classmethod
    def analyze(cls, text: str) -> dict:
        """Analiza texto usando coincidencia de palabras clave."""
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in cls.KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 1
            # Normalizar score
            scores[category] = min(score / 3, 1.0) if score > 0 else 0.0
        
        # Si no hay coincidencias, asignar "Reflexión" por defecto
        if all(s == 0 for s in scores.values()):
            scores["Reflexión"] = 0.5
        
        # Ordenar por score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Obtener categorías detectadas
        primary = sorted_scores[0]
        threshold = primary[1] * 0.8
        
        detected = []
        for name, score in sorted_scores[:3]:
            if score > 0 and score >= threshold:
                detected.append({"name": name, "confidence": round(score, 2)})
        
        if not detected:
            detected = [{"name": primary[0], "confidence": max(0.3, round(primary[1], 2))}]
        
        return {
            "categories": detected,
            "primary_category": primary[0],
            "primary_confidence": round(primary[1], 2),
            "all_scores": {k: round(v, 2) for k, v in scores.items() if v > 0},
            "method": "rule-based"
        }


class MiningEngine:
    """
    Motor de Minería de Texto.
    Intenta usar modelos de IA, con fallback a análisis basado en reglas.
    """
    
    TAXONOMY = [
        "Alegría", "Tristeza", "Enojo", "Miedo", "Sorpresa", "Asco",
        "Amor", "Odio", "Vergüenza", "Orgullo", "Envidia", "Celos",
        "Humor", "Inspiración", "Confesión", "Queja", "Consejo",
        "Pregunta", "Reflexión", "Nostalgia", "Ansiedad", "Frustración",
        "Sarcasmo", "Polémica", "Terror"
    ]
    
    HYPOTHESIS_TEMPLATE = "Este texto expresa {}"
    RELATIVE_THRESHOLD = 0.97
    MAX_EMOTIONS = 3

    _classifier = None
    _use_ai = None  # None = no determinado, True = usar IA, False = usar reglas

    @classmethod
    def _try_load_ai_model(cls):
        """Intenta cargar un modelo de IA. Retorna True si tiene éxito."""
        if cls._use_ai is not None:
            return cls._use_ai
        
        # Verificar si debemos usar IA o no (por defecto desactivado en producción)
        use_ai_env = os.environ.get('USE_AI_MODEL', 'false').lower()
        if use_ai_env in ('false', '0', 'no'):
            print("🔧 Modo rule-based activado (USE_AI_MODEL=false)")
            cls._use_ai = False
            return False
        
        try:
            from transformers import pipeline, AutoTokenizer
            
            print("🧠 Intentando cargar modelo de IA...")
            
            # Usar modelo más ligero primero
            models_to_try = [
                ("typeform/distilbert-base-uncased-mnli", False),  # Más ligero
                ("facebook/bart-large-mnli", False),
            ]
            
            for model_name, use_slow_tokenizer in models_to_try:
                try:
                    print(f"📦 Cargando: {model_name}")
                    
                    if use_slow_tokenizer:
                        tokenizer = AutoTokenizer.from_pretrained(
                            model_name, 
                            use_fast=False,
                            local_files_only=False
                        )
                        cls._classifier = pipeline(
                            "zero-shot-classification",
                            model=model_name,
                            tokenizer=tokenizer,
                            device=-1
                        )
                    else:
                        cls._classifier = pipeline(
                            "zero-shot-classification",
                            model=model_name,
                            device=-1
                        )
                    
                    print(f"✅ Modelo {model_name} cargado!")
                    cls._use_ai = True
                    return True
                    
                except Exception as e:
                    print(f"⚠️ Error con {model_name}: {e}")
                    continue
            
            print("⚠️ No se pudo cargar ningún modelo de IA")
            cls._use_ai = False
            return False
            
        except ImportError as e:
            print(f"⚠️ Transformers no disponible: {e}")
            cls._use_ai = False
            return False
        except Exception as e:
            print(f"⚠️ Error general cargando IA: {e}")
            cls._use_ai = False
            return False

    @classmethod
    def analyze(cls, text: str) -> dict:
        """
        Analiza un texto y retorna múltiples emociones detectadas.
        Usa IA si está disponible, sino usa análisis basado en reglas.
        """
        # Intentar usar IA primero
        if cls._use_ai is None:
            cls._try_load_ai_model()
        
        if cls._use_ai and cls._classifier:
            try:
                return cls._analyze_with_ai(text)
            except Exception as e:
                print(f"⚠️ Error en análisis IA: {e}")
                # Fallback a reglas
                return RuleBasedAnalyzer.analyze(text)
        else:
            return RuleBasedAnalyzer.analyze(text)
    
    @classmethod
    def _analyze_with_ai(cls, text: str) -> dict:
        """Análisis usando modelo de IA."""
        result = cls._classifier(
            text, 
            cls.TAXONOMY, 
            hypothesis_template=cls.HYPOTHESIS_TEMPLATE,
            multi_label=True
        )
        
        all_scores = dict(zip(result['labels'], result['scores']))
        max_score = result['scores'][0]
        threshold = max_score * cls.RELATIVE_THRESHOLD
        
        detected_categories = []
        for label, score in zip(result['labels'], result['scores']):
            if score >= threshold and len(detected_categories) < cls.MAX_EMOTIONS:
                detected_categories.append({
                    "name": label,
                    "confidence": round(score, 2)
                })
        
        if not detected_categories:
            detected_categories = [{
                "name": result['labels'][0],
                "confidence": round(result['scores'][0], 2)
            }]
        
        return {
            "categories": detected_categories,
            "primary_category": result['labels'][0],
            "primary_confidence": round(result['scores'][0], 2),
            "all_scores": {k: round(v, 2) for k, v in all_scores.items()},
            "method": "ai-model"
        }
