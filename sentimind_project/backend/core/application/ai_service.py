"""
Motor de Minería de Texto con HuggingFace Inference API.
Usa el modelo XLM-RoBERTa (2GB) en la nube de HuggingFace.
"""
import os
import requests
import time


class HuggingFaceInferenceAPI:
    """
    Cliente para la HuggingFace Inference API.
    Permite usar modelos grandes sin cargarlos en memoria local.
    """
    
    # Modelo multilingüe potente para zero-shot classification
    MODEL_ID = "joeddav/xlm-roberta-large-xnli"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    
    # Timeout y reintentos
    TIMEOUT = 60  # segundos (el modelo puede tardar en cargar la primera vez)
    MAX_RETRIES = 3
    
    @classmethod
    def get_headers(cls):
        """Obtiene headers con token de autenticación si está disponible."""
        token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGINGFACE_TOKEN')
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}
    
    @classmethod
    def classify(cls, text: str, labels: list, hypothesis_template: str = "Este texto expresa {}") -> dict:
        """
        Clasifica texto usando la API de HuggingFace.
        
        Args:
            text: Texto a clasificar
            labels: Lista de etiquetas posibles
            hypothesis_template: Template para zero-shot
            
        Returns:
            dict con labels y scores ordenados
        """
        payload = {
            "inputs": text,
            "parameters": {
                "candidate_labels": labels,
                "hypothesis_template": hypothesis_template,
                "multi_label": True
            }
        }
        
        headers = cls.get_headers()
        last_error = None
        
        for attempt in range(cls.MAX_RETRIES):
            try:
                response = requests.post(
                    cls.API_URL,
                    headers=headers,
                    json=payload,
                    timeout=cls.TIMEOUT
                )
                
                if response.status_code == 200:
                    return response.json()
                
                # Si el modelo está cargando, esperar y reintentar
                if response.status_code == 503:
                    data = response.json()
                    wait_time = data.get('estimated_time', 20)
                    print(f"⏳ Modelo cargando, esperando {wait_time}s...")
                    time.sleep(min(wait_time, 30))
                    continue
                
                # Error de rate limit
                if response.status_code == 429:
                    print("⚠️ Rate limit alcanzado, esperando...")
                    time.sleep(5)
                    continue
                
                last_error = f"HTTP {response.status_code}: {response.text}"
                
            except requests.exceptions.Timeout:
                last_error = "Timeout en la API"
                print(f"⏱️ Timeout (intento {attempt + 1}/{cls.MAX_RETRIES})")
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                print(f"⚠️ Error de conexión: {e}")
            
            time.sleep(2)
        
        raise RuntimeError(f"Error en HuggingFace API después de {cls.MAX_RETRIES} intentos: {last_error}")


class RuleBasedAnalyzer:
    """
    Analizador de sentimientos basado en reglas (keywords).
    Se usa como fallback cuando la API no está disponible.
    """
    
    KEYWORDS = {
        "Alegría": ["feliz", "contento", "alegre", "genial", "maravilloso", "increíble", "fantástico", 
                   "excelente", "bien", "super", "wow", "yay", "jaja", "😊", "😄", "🎉", "❤️",
                   "gracias", "agradecido", "bendecido", "perfecto", "éxito", "logré", "conseguí"],
        "Tristeza": ["triste", "llorar", "deprimido", "solo", "soledad", "melancolía", "pena", 
                    "dolor", "sufrir", "mal", "😢", "😭", "💔", "extraño", "perdí", "murió", "falleció"],
        "Enojo": ["enojado", "furioso", "molesto", "rabia", "ira", "odio", "maldito", "carajo",
                 "enfadado", "harto", "cansado de", "😠", "😡", "🤬", "injusto", "bronca"],
        "Miedo": ["miedo", "terror", "asustado", "pánico", "nervioso", "ansioso", "preocupado",
                 "temo", "aterrado", "😰", "😨", "😱", "horror", "susto"],
        "Sorpresa": ["sorpresa", "increíble", "no puedo creer", "wow", "impresionante", "inesperado",
                    "😮", "😲", "🤯", "en serio"],
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
        "Pregunta": ["?", "cómo", "cuál", "cuándo", "dónde", "por qué", "alguien sabe",
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
        "Terror": ["terror", "escalofriante", "pesadilla", "paranormal", "fantasma", "👻", "💀"],
        "Odio": ["odio", "detesto", "aborrezco", "no soporto"],
        "Celos": ["celos", "celoso", "celosa", "desconfianza"]
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
            scores[category] = min(score / 3, 1.0) if score > 0 else 0.0
        
        if all(s == 0 for s in scores.values()):
            scores["Reflexión"] = 0.5
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
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
    Usa HuggingFace Inference API para clasificación con XLM-RoBERTa.
    """
    
    # Lista completa de 25 categorías emocionales
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
    
    HYPOTHESIS_TEMPLATE = "Este texto expresa {}"
    RELATIVE_THRESHOLD = 0.90  # Umbral para detectar emociones secundarias
    MAX_EMOTIONS = 3

    @classmethod
    def analyze(cls, text: str) -> dict:
        """
        Analiza un texto y retorna múltiples emociones detectadas.
        Usa la API de HuggingFace con fallback a reglas.
        """
        # Verificar si debemos usar solo reglas
        use_rules_only = os.environ.get('USE_RULES_ONLY', 'false').lower() in ('true', '1', 'yes')
        
        if use_rules_only:
            return RuleBasedAnalyzer.analyze(text)
        
        try:
            print(f"🧠 Analizando con XLM-RoBERTa: '{text[:50]}...'")
            
            result = HuggingFaceInferenceAPI.classify(
                text=text,
                labels=cls.TAXONOMY,
                hypothesis_template=cls.HYPOTHESIS_TEMPLATE
            )
            
            # Procesar resultado de la API
            labels = result.get('labels', [])
            scores = result.get('scores', [])
            
            if not labels or not scores:
                print("⚠️ Respuesta vacía de la API, usando fallback")
                return RuleBasedAnalyzer.analyze(text)
            
            # Crear diccionario de scores
            all_scores = dict(zip(labels, scores))
            
            # Obtener categorías que superen el umbral relativo
            max_score = scores[0]
            threshold = max_score * cls.RELATIVE_THRESHOLD
            
            detected_categories = []
            for label, score in zip(labels, scores):
                if score >= threshold and len(detected_categories) < cls.MAX_EMOTIONS:
                    detected_categories.append({
                        "name": label,
                        "confidence": round(score, 2)
                    })
            
            if not detected_categories:
                detected_categories = [{
                    "name": labels[0],
                    "confidence": round(scores[0], 2)
                }]
            
            print(f"✅ Resultado: {detected_categories[0]['name']} ({detected_categories[0]['confidence']})")
            
            return {
                "categories": detected_categories,
                "primary_category": labels[0],
                "primary_confidence": round(scores[0], 2),
                "all_scores": {k: round(v, 2) for k, v in all_scores.items()},
                "method": "xlm-roberta-api"
            }
            
        except Exception as e:
            print(f"⚠️ Error en API, usando fallback: {e}")
            return RuleBasedAnalyzer.analyze(text)
