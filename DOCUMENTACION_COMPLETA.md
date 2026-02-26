# SENTIMIND NETWORK - DOCUMENTACION TECNICA COMPLETA

## Sistema de Analisis de Sentimientos con Inteligencia Artificial

**Proyecto:** Mineria de Datos y Aprendizaje Automatico  
**Universidad:** ULEAM - Universidad Laica Eloy Alfaro de Manabi  
**Fecha:** Enero 2026

---

## TABLA DE CONTENIDOS

1. [Resumen del Sistema](#1-resumen-del-sistema)
2. [Arquitectura General](#2-arquitectura-general)
3. [Estructura de Carpetas](#3-estructura-de-carpetas)
4. [Backend - Django REST Framework](#4-backend---django-rest-framework)
5. [Frontend - React + TypeScript](#5-frontend---react--typescript)
6. [Sistema de Inteligencia Artificial](#6-sistema-de-inteligencia-artificial)
7. [Proceso KDD (Knowledge Discovery in Databases)](#7-proceso-kdd)
8. [Sistema de Autenticacion JWT](#8-sistema-de-autenticacion-jwt)
9. [Flujo de Datos Completo](#9-flujo-de-datos-completo)
10. [API Reference](#10-api-reference)
11. [Archivos Modificados/Creados](#11-archivos-modificadoscreados)
12. [Instalacion y Ejecucion](#12-instalacion-y-ejecucion)
13. [Metricas y Evaluacion](#13-metricas-y-evaluacion)

---

## 1. RESUMEN DEL SISTEMA

### 1.1 Que es Sentimind Network?

Sentimind Network es una **red social experimental** que utiliza **Inteligencia Artificial** para clasificar automaticamente el contenido publicado por los usuarios en diferentes categorias emocionales y tematicas.

### 1.2 Tecnologias Principales

| Componente | Tecnologia |
|------------|------------|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS |
| **Backend** | Django 6.0, Django REST Framework |
| **IA/ML** | Transformers, XLM-RoBERTa, Zero-Shot Classification |
| **Base de Datos** | SQLite (desarrollo), PostgreSQL (produccion) |
| **Autenticacion** | JWT (SimpleJWT) |
| **Gestor de Paquetes** | uv (Python), npm/bun (Node.js) |

### 1.3 Caracteristicas Principales

- **Clasificacion Automatica**: Cada post es analizado por IA que determina su categoria emocional
- **Zero-Shot Classification**: No requiere entrenamiento especifico para nuevas categorias
- **Multi-Label**: Detecta multiples emociones en un solo texto
- **25 Categorias Emocionales**: Amplia taxonomia de emociones
- **Autenticacion JWT**: Sistema seguro de login/registro
- **Multilingue**: Soporta 100+ idiomas (optimizado para espanol)

---

## 2. ARQUITECTURA GENERAL

### 2.1 Diagrama de Arquitectura

```
+------------------------------------------------------------------+
|                         CLIENTE (Browser)                         |
+------------------------------------------------------------------+
                                |
                                | HTTP/HTTPS
                                v
+------------------------------------------------------------------+
|                    FRONTEND (React + Vite)                        |
|  +------------+  +------------+  +---------------------------+    |
|  |   Pages    |  | Components |  |        Adapters           |    |
|  | - Home     |  | - PostCard |  | - postAdapter.ts          |    |
|  | - Login    |  | - Navbar   |  | - authAdapter.ts          |    |
|  | - Register |  | - FilterBar|  | (Axios + JWT Interceptors)|    |
|  +------------+  +------------+  +---------------------------+    |
|                        |                                          |
|                 +------+------+                                   |
|                 |   Contexts  |                                   |
|                 | AuthContext |                                   |
|                 +-------------+                                   |
+------------------------------------------------------------------+
                                |
                                | REST API (JSON)
                                | Authorization: Bearer <JWT>
                                v
+------------------------------------------------------------------+
|                   BACKEND (Django REST Framework)                 |
|  +------------------+  +------------------+  +-----------------+  |
|  |  Authentication  |  |      Core        |  |   AI Service    |  |
|  |  - login/        |  |  - posts/        |  |  MiningEngine   |  |
|  |  - register/     |  |  - categories/   |  |  (Singleton)    |  |
|  |  - logout/       |  |                  |  |                 |  |
|  |  - token/refresh |  |                  |  |                 |  |
|  +------------------+  +------------------+  +-----------------+  |
|                                |                     |            |
|                                v                     v            |
|  +------------------+  +------------------+  +-----------------+  |
|  |     Models       |  |   Serializers    |  |   Transformers  |  |
|  | - User (Django)  |  | - PostSerializer |  |   Pipeline      |  |
|  | - Post           |  | - AuthSerializers|  |   XLM-RoBERTa   |  |
|  | - Category       |  |                  |  |                 |  |
|  | - PostCategory   |  |                  |  |                 |  |
|  +------------------+  +------------------+  +-----------------+  |
|                                |                                  |
+------------------------------------------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                      BASE DE DATOS (SQLite)                       |
|  +------------+  +------------+  +------------+  +------------+   |
|  |   Users    |  |   Posts    |  | Categories |  |PostCategory|   |
|  +------------+  +------------+  +------------+  +------------+   |
+------------------------------------------------------------------+
```

### 2.2 Flujo de Comunicacion

```
Usuario escribe post --> React captura texto --> Axios envia POST con JWT
                                                        |
                                                        v
                                              Django recibe request
                                                        |
                                                        v
                                              Valida JWT y usuario
                                                        |
                                                        v
                                              MiningEngine.analyze(texto)
                                                        |
                                                        v
                                              XLM-RoBERTa procesa texto
                                                        |
                                                        v
                                              Retorna categorias + confianza
                                                        |
                                                        v
                                              Guarda Post en DB
                                                        |
                                                        v
                                              Retorna JSON al frontend
                                                        |
                                                        v
                                              React actualiza UI
```

---

## 3. ESTRUCTURA DE CARPETAS

```
sentimind_project/
|
+-- backend/                          # Servidor Django
|   +-- authentication/               # App de autenticacion (NUEVO)
|   |   +-- __init__.py
|   |   +-- models.py                 # Usa User de Django
|   |   +-- serializers.py            # JWT serializers
|   |   +-- views.py                  # Login, Register, Logout
|   |   +-- urls.py                   # Rutas /api/auth/
|   |
|   +-- core/                         # App principal
|   |   +-- application/              # Capa de logica de negocio
|   |   |   +-- __init__.py
|   |   |   +-- ai_service.py         # MiningEngine (IA)
|   |   |
|   |   +-- domain/                   # Capa de dominio
|   |   |   +-- __init__.py
|   |   |
|   |   +-- infrastructure/           # Capa de infraestructura
|   |   |   +-- __init__.py
|   |   |   +-- serializers.py        # DRF Serializers
|   |   |   +-- views.py              # API Views
|   |   |
|   |   +-- migrations/               # Migraciones DB
|   |   +-- __init__.py
|   |   +-- admin.py
|   |   +-- apps.py
|   |   +-- models.py                 # Post, Category, PostCategory
|   |   +-- urls.py
|   |   +-- views.py
|   |
|   +-- sentimind/                    # Configuracion Django
|   |   +-- __init__.py
|   |   +-- asgi.py
|   |   +-- settings.py               # Configuracion principal
|   |   +-- urls.py                   # URLs raiz
|   |   +-- wsgi.py
|   |
|   +-- data/                         # Datos persistentes
|   |   +-- db.sqlite3                # Base de datos
|   |
|   +-- evaluation_results/           # Resultados de evaluacion (generado)
|   |   +-- confusion_matrix.png
|   |   +-- metrics_summary.png
|   |   +-- metrics.json
|   |
|   +-- manage.py                     # CLI Django
|   +-- pyproject.toml                # Dependencias Python
|   +-- evaluate_model.py             # Script de evaluacion (NUEVO)
|   +-- uv.lock
|
+-- frontend/                         # Cliente React
|   +-- src/
|   |   +-- adapters/                 # Comunicacion con API
|   |   |   +-- postAdapter.ts        # CRUD de posts
|   |   |   +-- authAdapter.ts        # Auth API (NUEVO)
|   |   |
|   |   +-- components/               # Componentes React
|   |   |   +-- FilterBar.tsx         # Filtros por categoria
|   |   |   +-- Navbar.tsx            # Barra navegacion (NUEVO)
|   |   |   +-- PostCard.tsx          # Tarjeta de post
|   |   |   +-- PostInput.tsx         # Input de nuevo post
|   |   |   +-- ProtectedRoute.tsx    # Ruta protegida (NUEVO)
|   |   |
|   |   +-- contexts/                 # Estado global (NUEVO)
|   |   |   +-- AuthContext.tsx       # Contexto autenticacion
|   |   |
|   |   +-- hooks/                    # Custom hooks
|   |   |   +-- usePosts.ts           # Hook para posts
|   |   |
|   |   +-- pages/                    # Paginas
|   |   |   +-- Home.tsx              # Pagina principal
|   |   |   +-- Login.tsx             # Login (NUEVO)
|   |   |   +-- Register.tsx          # Registro (NUEVO)
|   |   |   +-- ForgotPassword.tsx    # Reset password (NUEVO)
|   |   |
|   |   +-- utils/                    # Utilidades
|   |   |   +-- constants.ts          # Constantes
|   |   |
|   |   +-- App.tsx                   # Componente raiz
|   |   +-- main.tsx                  # Entry point
|   |   +-- index.css                 # Estilos globales
|   |
|   +-- package.json                  # Dependencias Node
|   +-- vite.config.ts                # Configuracion Vite
|   +-- tsconfig.json                 # Configuracion TypeScript
|
+-- DOCUMENTACION.md                  # Documentacion basica
+-- DOCUMENTACION_COMPLETA.md         # Este archivo
+-- docker-compose.yml                # Docker produccion
+-- docker-compose.dev.yml            # Docker desarrollo
```

---

## 4. BACKEND - DJANGO REST FRAMEWORK

### 4.1 Modelos de Datos (core/models.py)

```python
# Usuario: Se usa el modelo User de Django
from django.contrib.auth.models import User

class Category(models.Model):
    """Categoria/Emocion detectada por la IA."""
    name = models.CharField(max_length=50, unique=True, db_index=True)

class Post(models.Model):
    """Publicacion en el muro."""
    content = models.TextField(help_text="El mensaje del usuario")
    
    # Relacion con usuario (NUEVO)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,  # Permite posts anonimos
        blank=True
    )
    
    # Relacion muchos-a-muchos con categorias
    categories = models.ManyToManyField(
        Category,
        through='PostCategory',
        related_name='posts'
    )
    
    # Categoria principal (mayor confianza)
    primary_category = models.CharField(max_length=50, db_index=True)
    primary_confidence = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)

class PostCategory(models.Model):
    """Relacion Post-Category con confianza."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    confidence = models.FloatField()
```

### 4.2 Diagrama Entidad-Relacion

```
+------------------+       +-------------------+       +------------------+
|      User        |       |       Post        |       |    Category      |
+------------------+       +-------------------+       +------------------+
| id (PK)          |<---+  | id (PK)           |  +--->| id (PK)          |
| username         |    |  | content           |  |    | name (unique)    |
| email            |    |  | author_id (FK) ---+  |    +------------------+
| password (hash)  |    |  | primary_category  |  |
| first_name       |    |  | primary_confidence|  |
| last_name        |    |  | created_at        |  |
+------------------+    |  +-------------------+  |
                        |          |              |
                        |          | M:N          |
                        |          v              |
                        |  +-------------------+  |
                        |  |   PostCategory    |  |
                        |  +-------------------+  |
                        |  | id (PK)           |  |
                        +--| post_id (FK)      |  |
                           | category_id (FK) -+--+
                           | confidence        |
                           +-------------------+
```

### 4.3 Vistas API (core/infrastructure/views.py)

```python
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Permite lectura a todos, escritura solo a autenticados."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class PostListCreateView(generics.ListCreateAPIView):
    """
    GET /api/posts/  - Lista posts (publico)
    POST /api/posts/ - Crea post (requiere auth)
    """
    queryset = Post.objects.select_related('author').prefetch_related(
        'post_categories__category'
    ).all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por categoria
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories__name=category).distinct()
        
        # Filtro por posts propios
        mine = self.request.query_params.get('mine')
        if mine and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
        
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        content = request.data.get('content')
        
        # 1. Analizar con IA
        analysis = MiningEngine.analyze(content)
        
        # 2. Crear Post con autor
        post = Post.objects.create(
            content=content,
            author=request.user if request.user.is_authenticated else None,
            primary_category=analysis['primary_category'],
            primary_confidence=analysis['primary_confidence']
        )
        
        # 3. Crear relaciones con categorias
        for cat_data in analysis['categories']:
            category, _ = Category.objects.get_or_create(name=cat_data['name'])
            PostCategory.objects.create(
                post=post,
                category=category,
                confidence=cat_data['confidence']
            )
        
        return Response(PostSerializer(post).data, status=201)
```

### 4.4 Serializers (core/infrastructure/serializers.py)

```python
class AuthorSerializer(serializers.Serializer):
    """Info del autor del post."""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class PostCategorySerializer(serializers.ModelSerializer):
    """Categoria con confianza."""
    name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = PostCategory
        fields = ['name', 'confidence']


class PostSerializer(serializers.ModelSerializer):
    """Serializer completo de Post."""
    categories = PostCategorySerializer(source='post_categories', many=True)
    category = serializers.CharField(source='primary_category')
    confidence = serializers.FloatField(source='primary_confidence')
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'content', 'author',
            'category', 'confidence',
            'primary_category', 'primary_confidence',
            'categories', 'created_at'
        ]
```

---

## 5. FRONTEND - REACT + TYPESCRIPT

### 5.1 Estructura de Componentes

```
App.tsx
|
+-- Navbar (siempre visible si autenticado)
|
+-- Routes
    |
    +-- /login --> Login.tsx (publico)
    +-- /register --> Register.tsx (publico)
    +-- /forgot-password --> ForgotPassword.tsx (publico)
    +-- / --> ProtectedRoute --> Home.tsx (protegido)
```

### 5.2 Contexto de Autenticacion (contexts/AuthContext.tsx)

```typescript
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Verificar token al cargar
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const userData = await authService.getProfile();
          setUser(userData);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
      }
      setIsLoading(false);
    };
    initAuth();
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const response = await authService.login(username, password);
    localStorage.setItem("access_token", response.access);
    localStorage.setItem("refresh_token", response.refresh);
    setUser(response.user);
  }, []);

  // ... register, logout
}
```

### 5.3 Adapter de Posts con JWT (adapters/postAdapter.ts)

```typescript
const api = axios.create({
  baseURL: API_URL,
});

// Interceptor: Agregar JWT a cada request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor: Renovar token si expiro
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");
      
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          localStorage.setItem("access_token", response.data.access);
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return api(originalRequest);
        } catch {
          // Token refresh fallido, redirigir a login
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);
```

### 5.4 Ruta Protegida (components/ProtectedRoute.tsx)

```typescript
export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
```

---

## 6. SISTEMA DE INTELIGENCIA ARTIFICIAL

### 6.1 Motor de Mineria (core/application/ai_service.py)

El corazon del sistema es la clase `MiningEngine`, que implementa el patron **Singleton** para cargar el modelo de IA una sola vez en memoria.

```python
class MiningEngine:
    """
    Motor de Mineria de Texto basado en Transformers.
    Patron Singleton para cargar el modelo en memoria una sola vez.
    """
    
    # 25 categorias emocionales
    TAXONOMY = [
        # Emociones basicas
        "Alegria", "Tristeza", "Enojo", "Miedo", "Sorpresa", "Asco",
        # Emociones sociales
        "Amor", "Odio", "Verguenza", "Orgullo", "Envidia", "Celos",
        # Tipos de contenido
        "Humor", "Inspiracion", "Confesion", "Queja", "Consejo",
        "Pregunta", "Reflexion", "Nostalgia", "Ansiedad", "Frustracion",
        # Contenido especial
        "Sarcasmo", "Polemica", "Terror"
    ]
    
    # Template para Zero-Shot
    HYPOTHESIS_TEMPLATE = "Este texto expresa {}"
    
    # Configuracion
    RELATIVE_THRESHOLD = 0.90  # 90% del score maximo
    MAX_EMOTIONS = 3  # Maximo de emociones a retornar
    
    _classifier = None  # Singleton

    @classmethod
    def get_classifier(cls):
        """Carga el modelo (Singleton)."""
        if cls._classifier is None:
            print("[AI] Cargando modelo XLM-RoBERTa...")
            
            model_name = "joeddav/xlm-roberta-large-xnli"
            
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                use_fast=False  # Usar SentencePiece
            )
            
            cls._classifier = pipeline(
                "zero-shot-classification",
                model=model_name,
                tokenizer=tokenizer,
                device=-1  # CPU
            )
            
            print("[OK] Modelo cargado!")
        
        return cls._classifier

    @classmethod
    def analyze(cls, text: str) -> dict:
        """Analiza texto y retorna categorias detectadas."""
        classifier = cls.get_classifier()
        
        # Inferencia Zero-Shot
        result = classifier(
            text,
            cls.TAXONOMY,
            hypothesis_template=cls.HYPOTHESIS_TEMPLATE,
            multi_label=True  # Detectar multiples emociones
        )
        
        # Filtrar por umbral relativo
        max_score = result['scores'][0]
        threshold = max_score * cls.RELATIVE_THRESHOLD
        
        detected = []
        for label, score in zip(result['labels'], result['scores']):
            if score >= threshold and len(detected) < cls.MAX_EMOTIONS:
                detected.append({
                    "name": label,
                    "confidence": round(score, 2)
                })
        
        return {
            "categories": detected,
            "primary_category": result['labels'][0],
            "primary_confidence": round(result['scores'][0], 2),
            "method": "xlm-roberta-local"
        }
```

### 6.2 Modelo XLM-RoBERTa

| Caracteristica | Valor |
|----------------|-------|
| **Nombre** | joeddav/xlm-roberta-large-xnli |
| **Arquitectura** | XLM-RoBERTa Large |
| **Parametros** | ~550 millones |
| **Dimension Embeddings** | 1024 |
| **Capas Transformer** | 24 |
| **Attention Heads** | 16 |
| **Vocabulario** | ~250,000 tokens (SentencePiece BPE) |
| **Idiomas** | 100+ |
| **Pre-entrenamiento** | CommonCrawl (2.5TB) |
| **Fine-tuning** | XNLI (392,702 ejemplos en 15 idiomas) |

### 6.3 Zero-Shot Classification

El modelo convierte la clasificacion en un problema de **Natural Language Inference (NLI)**:

```
Entrada: "Hoy me siento muy feliz porque consegui trabajo"

Proceso:
  Premisa: "Hoy me siento muy feliz porque consegui trabajo"
  
  Para cada categoria:
    Hipotesis: "Este texto expresa Alegria"    -> Entailment: 0.95
    Hipotesis: "Este texto expresa Tristeza"   -> Entailment: 0.02
    Hipotesis: "Este texto expresa Orgullo"    -> Entailment: 0.87
    ...

Salida:
  {
    "primary_category": "Alegria",
    "primary_confidence": 0.95,
    "categories": [
      {"name": "Alegria", "confidence": 0.95},
      {"name": "Orgullo", "confidence": 0.87}
    ]
  }
```

### 6.4 Diagrama del Pipeline NLP

```
+------------------+     +------------------+     +------------------+
|   Texto Input    | --> |   Tokenizacion   | --> |    Embeddings    |
| "Estoy feliz..." |     |  SentencePiece   |     |   dim=1024       |
+------------------+     +------------------+     +------------------+
                                                          |
                                                          v
+------------------+     +------------------+     +------------------+
|     Softmax      | <-- |   Clasificador   | <-- |   Transformer    |
|  Probabilidades  |     |   NLI Head       |     |   24 capas       |
+------------------+     +------------------+     +------------------+
         |
         v
+------------------+
|   Categorias     |
|   + Confianza    |
+------------------+
```

---

## 7. PROCESO KDD

El sistema implementa las 5 fases del proceso **KDD (Knowledge Discovery in Databases)**:

### 7.1 Fase 1: Seleccion de Datos

**Variables de Entrada:**
- `content` (string): Texto del post a clasificar

**Variables de Salida:**
- `primary_category` (string): Emocion principal
- `primary_confidence` (float): Confianza (0-1)
- `categories` (list): Lista de emociones detectadas

**Filtros:**
- Textos < 3 caracteres: Rechazados
- Textos > 1000 caracteres: Truncados

### 7.2 Fase 2: Preprocesamiento

El modelo XLM-RoBERTa maneja el preprocesamiento internamente:

| Operacion | Descripcion |
|-----------|-------------|
| **Tokenizacion** | SentencePiece con BPE (~250,000 tokens) |
| **Normalizacion** | Unicode NFD a NFC |
| **Lowercase** | No aplicado (case-sensitive) |
| **Emojis** | Preservados (contienen info emocional) |
| **URLs/Mentions** | Preservados |

### 7.3 Fase 3: Transformacion

```
Texto Original:
  "Estoy muy feliz hoy!"

Tokenizacion:
  ["▁Estoy", "▁muy", "▁fel", "iz", "▁hoy", "!"]

Token IDs:
  [5765, 1810, 8976, 3421, 1234, 5]

Embeddings:
  Matriz [6 x 1024] - Un vector de 1024 dims por token

Contextualizacion:
  24 capas de Transformer procesan los embeddings
  Cada token "ve" a todos los demas (self-attention)

Output:
  Vector [1 x 1024] representando todo el texto
```

### 7.4 Fase 4: Mineria de Datos

**Algoritmo:** Zero-Shot Classification con XLM-RoBERTa

**Hiperparametros:**
| Parametro | Valor | Descripcion |
|-----------|-------|-------------|
| `multi_label` | True | Detecta multiples emociones |
| `RELATIVE_THRESHOLD` | 0.90 | Umbral para emociones secundarias |
| `MAX_EMOTIONS` | 3 | Maximo de emociones por texto |
| `device` | -1 | Usar CPU |

### 7.5 Fase 5: Evaluacion

Ver seccion 13 para metricas detalladas.

---

## 8. SISTEMA DE AUTENTICACION JWT

### 8.1 Arquitectura JWT

```
+-------------+                                  +-------------+
|   Cliente   |                                  |   Servidor  |
+-------------+                                  +-------------+
      |                                                |
      |  1. POST /api/auth/login/                      |
      |     {username, password}                       |
      |----------------------------------------------->|
      |                                                |
      |  2. Valida credenciales                        |
      |                                                |
      |  3. Response: {access_token, refresh_token}    |
      |<-----------------------------------------------|
      |                                                |
      |  4. Guarda tokens en localStorage              |
      |                                                |
      |  5. GET /api/posts/                            |
      |     Header: Authorization: Bearer <access>     |
      |----------------------------------------------->|
      |                                                |
      |  6. Valida JWT                                 |
      |                                                |
      |  7. Response: [posts...]                       |
      |<-----------------------------------------------|
      |                                                |
      |  === Si access_token expira (401) ===          |
      |                                                |
      |  8. POST /api/auth/token/refresh/              |
      |     {refresh: refresh_token}                   |
      |----------------------------------------------->|
      |                                                |
      |  9. Response: {access: new_token}              |
      |<-----------------------------------------------|
      |                                                |
      | 10. Reintenta request original con nuevo token |
      |----------------------------------------------->|
```

### 8.2 Configuracion JWT (settings.py)

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),   # 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # 7 dias
    'ROTATE_REFRESH_TOKENS': True,                    # Nuevo refresh en cada uso
    'BLACKLIST_AFTER_ROTATION': True,                 # Invalida refresh antiguo
    'UPDATE_LAST_LOGIN': True,                        # Actualiza last_login
    'ALGORITHM': 'HS256',                             # Algoritmo de firma
    'SIGNING_KEY': SECRET_KEY,                        # Clave secreta
    'AUTH_HEADER_TYPES': ('Bearer',),                 # Tipo de header
}
```

### 8.3 Endpoints de Autenticacion

| Endpoint | Metodo | Descripcion | Auth |
|----------|--------|-------------|------|
| `/api/auth/login/` | POST | Obtener tokens | No |
| `/api/auth/register/` | POST | Registrar usuario | No |
| `/api/auth/logout/` | POST | Invalidar refresh token | Si |
| `/api/auth/token/refresh/` | POST | Renovar access token | No |
| `/api/auth/me/` | GET | Datos del usuario actual | Si |
| `/api/auth/change-password/` | PUT | Cambiar contrasena | Si |
| `/api/auth/password-reset/` | POST | Solicitar reset | No |

### 8.4 Vistas de Autenticacion (authentication/views.py)

```python
class CustomTokenObtainPairView(TokenObtainPairView):
    """Login: Retorna tokens + datos del usuario."""
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """Registro de nuevos usuarios."""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens automaticamente
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=201)


class LogoutView(APIView):
    """Logout: Invalida el refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Agregar a lista negra
        return Response({'message': 'Sesion cerrada'})
```

---

## 9. FLUJO DE DATOS COMPLETO

### 9.1 Flujo de Registro

```
1. Usuario llena formulario en Register.tsx
   - username, email, password, password2
   
2. Frontend valida passwords coinciden
   
3. POST /api/auth/register/
   {
     "username": "juan",
     "email": "juan@email.com",
     "password": "SecurePass123",
     "password2": "SecurePass123"
   }

4. Backend valida:
   - Username unico
   - Email unico
   - Password cumple politicas
   
5. Crea usuario en DB
   
6. Genera JWT tokens
   
7. Response:
   {
     "user": {"id": 1, "username": "juan", ...},
     "tokens": {
       "access": "eyJ0eXAiOiJKV1Q...",
       "refresh": "eyJ0eXAiOiJKV1Q..."
     }
   }

8. Frontend guarda tokens en localStorage
   
9. Redirige a Home (/)
```

### 9.2 Flujo de Crear Post

```
1. Usuario escribe en PostInput.tsx
   "Hoy me siento muy feliz!"

2. Click en "Publicar" o Ctrl+Enter

3. postAdapter.create(content) llamado

4. Axios interceptor agrega JWT:
   POST /api/posts/
   Authorization: Bearer eyJ0eXAiOiJKV1Q...
   Content-Type: application/json
   {"content": "Hoy me siento muy feliz!"}

5. Backend (PostListCreateView.create):
   a. Valida JWT -> obtiene request.user
   b. Valida content (>= 3 chars)
   c. Llama MiningEngine.analyze(content)

6. MiningEngine:
   a. get_classifier() -> carga modelo si no existe
   b. Tokeniza texto
   c. Ejecuta inferencia Zero-Shot
   d. Filtra por umbral
   e. Retorna categorias

7. Backend crea Post en DB:
   - content: "Hoy me siento muy feliz!"
   - author: User(id=1)
   - primary_category: "Alegria"
   - primary_confidence: 0.95

8. Crea relaciones PostCategory

9. Response:
   {
     "id": 5,
     "content": "Hoy me siento muy feliz!",
     "author": {"id": 1, "username": "juan"},
     "category": "Alegria",
     "confidence": 0.95,
     "categories": [
       {"name": "Alegria", "confidence": 0.95}
     ],
     "created_at": "2026-01-24T..."
   }

10. Frontend actualiza estado -> renderiza nuevo post
```

### 9.3 Flujo de Filtrado

```
1. Usuario click en "Tristeza" en FilterBar

2. setFilter("Tristeza") actualiza estado

3. usePosts hook detecta cambio en filter

4. GET /api/posts/?category=Tristeza
   Authorization: Bearer ...

5. Backend filtra:
   queryset.filter(categories__name="Tristeza")

6. Response: [posts con categoria Tristeza]

7. Frontend renderiza posts filtrados
```

---

## 10. API REFERENCE

### 10.1 Autenticacion

#### POST /api/auth/login/
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "usuario",
  "password": "contrasena"
}
```

**Response 200:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@email.com",
    "first_name": "",
    "last_name": ""
  }
}
```

#### POST /api/auth/register/
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "nuevo@email.com",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "Juan",
  "last_name": "Perez"
}
```

**Response 201:**
```json
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 2,
    "username": "nuevo_usuario",
    "email": "nuevo@email.com",
    "first_name": "Juan",
    "last_name": "Perez"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### POST /api/auth/token/refresh/
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response 200:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 10.2 Posts

#### GET /api/posts/
```http
GET /api/posts/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `category` (string): Filtrar por categoria
- `mine` (boolean): Solo posts del usuario actual

**Response 200:**
```json
[
  {
    "id": 1,
    "content": "Texto del post",
    "author": {
      "id": 1,
      "username": "usuario"
    },
    "category": "Alegria",
    "confidence": 0.95,
    "primary_category": "Alegria",
    "primary_confidence": 0.95,
    "categories": [
      {"name": "Alegria", "confidence": 0.95},
      {"name": "Orgullo", "confidence": 0.87}
    ],
    "created_at": "2026-01-24T10:30:00Z"
  }
]
```

#### POST /api/posts/
```http
POST /api/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content": "Hoy me siento muy feliz!"
}
```

**Response 201:**
```json
{
  "id": 5,
  "content": "Hoy me siento muy feliz!",
  "author": {
    "id": 1,
    "username": "usuario"
  },
  "category": "Alegria",
  "confidence": 0.95,
  "primary_category": "Alegria",
  "primary_confidence": 0.95,
  "categories": [
    {"name": "Alegria", "confidence": 0.95}
  ],
  "created_at": "2026-01-24T10:35:00Z"
}
```

#### GET /api/categories/
```http
GET /api/categories/
```

**Response 200:**
```json
{
  "categories": [
    "Alegria", "Tristeza", "Enojo", "Miedo", "Sorpresa", "Asco",
    "Amor", "Odio", "Verguenza", "Orgullo", "Envidia", "Celos",
    "Humor", "Inspiracion", "Confesion", "Queja", "Consejo",
    "Pregunta", "Reflexion", "Nostalgia", "Ansiedad", "Frustracion",
    "Sarcasmo", "Polemica", "Terror"
  ]
}
```

---

## 11. ARCHIVOS MODIFICADOS/CREADOS

### 11.1 Backend - Nuevos Archivos

| Archivo | Descripcion |
|---------|-------------|
| `authentication/__init__.py` | Inicializacion app auth |
| `authentication/models.py` | Usa User de Django |
| `authentication/serializers.py` | JWT serializers |
| `authentication/views.py` | Login, Register, Logout, etc. |
| `authentication/urls.py` | Rutas /api/auth/ |
| `evaluate_model.py` | Script de evaluacion con metricas |

### 11.2 Backend - Archivos Modificados

| Archivo | Cambio |
|---------|--------|
| `pyproject.toml` | Agregado: djangorestframework-simplejwt, scikit-learn, matplotlib |
| `sentimind/settings.py` | Agregado: INSTALLED_APPS (simplejwt, authentication), REST_FRAMEWORK config, SIMPLE_JWT config |
| `sentimind/urls.py` | Agregado: path('api/auth/', include('authentication.urls')) |
| `core/models.py` | Agregado: campo `author` ForeignKey a User en Post |
| `core/infrastructure/views.py` | Agregado: IsAuthenticatedOrReadOnly, autor en create() |
| `core/infrastructure/serializers.py` | Agregado: AuthorSerializer, campo author en PostSerializer |
| `core/application/ai_service.py` | Removido: emojis en prints (fix Windows cp1252) |

### 11.3 Frontend - Nuevos Archivos

| Archivo | Descripcion |
|---------|-------------|
| `src/adapters/authAdapter.ts` | API calls de auth + interceptores JWT |
| `src/contexts/AuthContext.tsx` | Estado global de autenticacion |
| `src/pages/Login.tsx` | Pagina de login |
| `src/pages/Register.tsx` | Pagina de registro |
| `src/pages/ForgotPassword.tsx` | Pagina reset password |
| `src/components/Navbar.tsx` | Barra de navegacion |
| `src/components/ProtectedRoute.tsx` | HOC para rutas protegidas |

### 11.4 Frontend - Archivos Modificados

| Archivo | Cambio |
|---------|--------|
| `package.json` | Agregado: react-router-dom |
| `src/main.tsx` | Agregado: BrowserRouter, AuthProvider |
| `src/App.tsx` | Agregado: Routes, Navbar, rutas auth |
| `src/pages/Home.tsx` | Agregado: paddingTop para navbar |
| `src/adapters/postAdapter.ts` | Agregado: interceptores JWT, interface Author |

---

## 12. INSTALACION Y EJECUCION

### 12.1 Requisitos

- Python 3.13+
- Node.js 18+ (o Bun)
- uv (gestor de paquetes Python)
- Git

### 12.2 Instalacion Backend

```bash
# Clonar repositorio
git clone <repo-url>
cd sentimind_project/backend

# Instalar dependencias
uv sync

# Ejecutar migraciones
uv run python manage.py migrate

# Crear superusuario (opcional)
uv run python manage.py createsuperuser

# Iniciar servidor
uv run python manage.py runserver
```

### 12.3 Instalacion Frontend

```bash
cd sentimind_project/frontend

# Instalar dependencias
npm install
# o con bun
bun install

# Iniciar servidor de desarrollo
npm run dev
# o con bun
bun run dev
```

### 12.4 URLs de Acceso

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000/api/ |
| Admin Django | http://127.0.0.1:8000/admin/ |

### 12.5 Variables de Entorno

**Backend (.env):**
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Frontend (.env):**
```
VITE_API_URL=http://127.0.0.1:8000/api
```

---

## 13. METRICAS Y EVALUACION

### 13.1 Ejecutar Evaluacion

```bash
cd backend
uv run python evaluate_model.py
```

### 13.2 Metricas Calculadas

| Metrica | Descripcion | Formula |
|---------|-------------|---------|
| **Accuracy** | % predicciones correctas | TP+TN / Total |
| **Precision** | % positivos predichos correctos | TP / (TP+FP) |
| **Recall** | % positivos reales detectados | TP / (TP+FN) |
| **F1-Score** | Media armonica Precision/Recall | 2*(P*R)/(P+R) |

### 13.3 Dataset de Evaluacion

El script `evaluate_model.py` incluye un dataset de 40 textos etiquetados manualmente:

```python
EVALUATION_DATASET = [
    ("Que dia tan increible! Todo salio perfecto", "Alegria"),
    ("Hoy se murio mi perro, lo extrano mucho", "Tristeza"),
    ("Estoy furioso, me mintieron en la cara", "Enojo"),
    ("Tengo mucho miedo de lo que pueda pasar", "Miedo"),
    # ... 36 textos mas
]
```

### 13.4 Archivos Generados

```
evaluation_results/
+-- confusion_matrix.png    # Matriz de confusion visual
+-- metrics_summary.png     # Grafico de metricas
+-- metrics.json            # Metricas en JSON
```

### 13.5 Ejemplo de Salida

```
================================================================================
EVALUACION FORMAL DEL MODELO DE CLASIFICACION
================================================================================
Fecha: 2026-01-24 10:30:00
Modelo: XLM-RoBERTa Large XNLI (Zero-Shot)
Textos de evaluacion: 40
================================================================================

ACCURACY: 0.8500 (85.00%)

METRICAS WEIGHTED:
   Precision: 0.8723
   Recall:    0.8500
   F1-Score:  0.8542

================================================================================
EVALUACION COMPLETADA
================================================================================
```

---

## RESUMEN FINAL

Sentimind Network es un sistema completo de analisis de sentimientos que integra:

1. **Frontend moderno** con React 19, TypeScript y autenticacion JWT
2. **Backend robusto** con Django REST Framework y arquitectura limpia
3. **IA de vanguardia** con XLM-RoBERTa y Zero-Shot Classification
4. **Proceso KDD completo** desde seleccion de datos hasta evaluacion
5. **25 categorias emocionales** para clasificacion detallada
6. **Soporte multilingue** para 100+ idiomas

El sistema demuestra la aplicacion practica de tecnicas de Mineria de Datos y Aprendizaje Automatico en un problema real de clasificacion de texto.

---

_Documento generado para el proyecto de Mineria de Datos - ULEAM 2026_
