# 📘 Sentimind Network - Documentación Completa

## Guía de Usuario y Documentación Técnica

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Categorías Disponibles](#categorías-disponibles)
4. [Guía de Uso: Cómo Publicar Posts](#guía-de-uso-cómo-publicar-posts)
5. [API Reference](#api-reference)
6. [Frontend: Estructura y Componentes](#frontend-estructura-y-componentes)
7. [Backend: Capas y Servicios](#backend-capas-y-servicios)
8. [Modelo de IA](#modelo-de-ia)
9. [Instalación y Ejecución](#instalación-y-ejecución)

---

## Introducción

**Sentimind Network** es una red social experimental que utiliza **Inteligencia Artificial** para clasificar automáticamente el contenido publicado por los usuarios en diferentes categorías emocionales y temáticas.

### Características Principales

- 🧠 **Clasificación Automática**: Cada post es analizado por un modelo de IA que determina su categoría.
- 🎯 **Zero-Shot Classification**: No requiere entrenamiento específico para nuevas categorías.
- ⚡ **Alto Rendimiento**: Backend gestionado con `uv` (Astral) para instalación ultrarrápida.
- 🏗️ **Arquitectura Limpia**: Separación clara entre lógica de negocio, infraestructura y presentación.

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Pages     │  │  Components │  │      Adapters           │  │
│  │  (Home.tsx) │  │ (PostCard,  │  │  (postAdapter.ts)       │  │
│  │             │  │  FilterBar) │  │  Comunicación con API   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                           │                                      │
│                    ┌──────┴──────┐                              │
│                    │    Hooks    │                              │
│                    │ (usePosts)  │                              │
│                    └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP/JSON
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (Django)                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    INFRASTRUCTURE                            ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  ││
│  │  │    Views     │  │  Serializers │  │      URLs        │  ││
│  │  │   (API)      │  │   (JSON)     │  │   (Routing)      │  ││
│  │  └──────────────┘  └──────────────┘  └──────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     APPLICATION                              ││
│  │  ┌──────────────────────────────────────────────────────┐  ││
│  │  │                   MiningEngine                        │  ││
│  │  │        (Servicio de IA - Zero-Shot Classification)    │  ││
│  │  └──────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                       DOMAIN                                 ││
│  │  ┌──────────────────────────────────────────────────────┐  ││
│  │  │                    Post Model                         │  ││
│  │  │   (content, category, confidence, created_at)         │  ││
│  │  └──────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │     SQLite      │
                    │   (Database)    │
                    └─────────────────┘
```

---

## Categorías Disponibles

El sistema clasifica automáticamente los posts en **12 categorías** predefinidas:

| Categoría         | Descripción                                   | Color    | Ejemplo                                        |
| ----------------- | --------------------------------------------- | -------- | ---------------------------------------------- |
| 🔴 **Tóxico**     | Contenido agresivo, hostil o negativo         | Rojo     | _"Odio cuando la gente no hace su trabajo"_    |
| 😂 **Gracioso**   | Contenido humorístico, bromas, memes          | Amarillo | _"Mi perro persigue su cola hace 20 minutos"_  |
| ✨ **Inspirador** | Mensajes motivacionales, logros, superación   | Verde    | _"Después de 5 años, terminé mi carrera"_      |
| 💔 **Triste**     | Contenido melancólico, pérdidas, nostalgia    | Azul     | _"Hoy hace un año que perdí a mi abuela"_      |
| 💕 **Romántico**  | Amor, relaciones, sentimientos afectivos      | Rosa     | _"Cada día me enamoro más de mi esposa"_       |
| 🔥 **Polémico**   | Opiniones controversiales, debates            | Naranja  | _"El sistema educativo necesita una reforma"_  |
| 🤢 **Asqueroso**  | Contenido repulsivo, desagradable             | Lima     | _"Encontré un pelo en mi comida"_              |
| 🤔 **Filosófico** | Reflexiones profundas, existenciales          | Púrpura  | _"¿Tenemos realmente libre albedrío?"_         |
| 🤫 **Confesión**  | Secretos, admisiones personales               | Índigo   | _"Nunca he leído Harry Potter y finjo que sí"_ |
| 😤 **Queja**      | Reclamos, inconformidades, frustraciones      | Gris     | _"El internet en mi ciudad es terrible"_       |
| 🧐 **Curiosidad** | Datos interesantes, descubrimientos           | Cian     | _"¿Sabían que los pulpos tienen 3 corazones?"_ |
| 👻 **Terror**     | Historias de miedo, experiencias paranormales | Pizarra  | _"Escuché pasos en el ático pero vivo solo"_   |

### Cómo Funciona la Clasificación

1. El usuario escribe un post
2. El texto se envía al backend
3. El **MiningEngine** procesa el texto con el modelo de IA
4. El modelo evalúa la probabilidad para cada categoría
5. Se selecciona la categoría con mayor probabilidad (confidence)
6. El post se guarda con su categoría y porcentaje de certeza

---

## Guía de Uso: Cómo Publicar Posts

### Paso 1: Escribir el Contenido

En la página principal, encontrarás un área de texto donde puedes escribir tu mensaje:

```
┌─────────────────────────────────────────────────────────────┐
│  ¿Qué estás pensando? La IA lo clasificará automáticamente  │
│  ____________________________________________________________│
│  │                                                          ││
│  │  Escribe tu mensaje aquí...                              ││
│  │                                                          ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
│  [         🧠 Publicar         ]                             │
└─────────────────────────────────────────────────────────────┘
```

### Paso 2: Enviar el Post

Tienes dos opciones:

- **Clic en "🧠 Publicar"**: Botón principal
- **Ctrl + Enter**: Atajo de teclado rápido

### Paso 3: Esperar la Clasificación

El sistema mostrará "Analizando con IA..." mientras procesa tu mensaje.

> ⚠️ **Nota**: La primera vez que se envía un post, el modelo de IA se descarga (~1GB). Esto puede tomar 1-2 minutos. Las siguientes clasificaciones son instantáneas.

### Paso 4: Ver el Resultado

Tu post aparecerá en el muro con:

- **Etiqueta de categoría**: La categoría asignada por la IA
- **Porcentaje de certeza**: Qué tan seguro está el modelo
- **Fecha y hora**: Cuándo fue publicado

```
┌─────────────────────────────────────────┐
│  [GRACIOSO]                    92% certeza│
│                                          │
│  "Mi perro persigue su cola hace 20     │
│   minutos, creo que es su cardio"        │
│                                          │
│  03/01/2026, 14:30                       │
└─────────────────────────────────────────┘
```

### Paso 5: Filtrar Posts

Usa los botones de categoría para ver solo posts de un tipo específico:

```
[Todas] [Tóxico] [Gracioso] [Inspirador] [Triste] [Romántico] ...
```

---

## API Reference

### Base URL

```
http://127.0.0.1:8000/api/
```

### Endpoints

#### 1. Listar Posts

```http
GET /api/posts/
```

**Query Parameters:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `category` | string | Filtrar por categoría (opcional) |

**Ejemplo de Respuesta:**

```json
[
  {
    "id": 1,
    "content": "Mi perro persigue su cola hace 20 minutos",
    "category": "Gracioso",
    "confidence": 0.92,
    "created_at": "2026-01-03T14:30:00Z"
  }
]
```

#### 2. Crear Post

```http
POST /api/posts/
Content-Type: application/json
```

**Body:**

```json
{
  "content": "Texto del post a clasificar"
}
```

**Respuesta (201 Created):**

```json
{
  "id": 2,
  "content": "Texto del post a clasificar",
  "category": "Filosófico",
  "confidence": 0.85,
  "created_at": "2026-01-03T15:00:00Z"
}
```

#### 3. Obtener Categorías

```http
GET /api/categories/
```

**Respuesta:**

```json
{
  "categories": [
    "Tóxico",
    "Gracioso",
    "Inspirador",
    "Triste",
    "Romántico",
    "Polémico",
    "Asqueroso",
    "Filosófico",
    "Confesión",
    "Queja",
    "Curiosidad",
    "Terror"
  ]
}
```

---

## Frontend: Estructura y Componentes

```
frontend/src/
├── adapters/
│   └── postAdapter.ts      # Comunicación con API
├── components/
│   ├── PostCard.tsx        # Tarjeta de post individual
│   ├── PostInput.tsx       # Área de entrada de texto
│   └── FilterBar.tsx       # Barra de filtros por categoría
├── hooks/
│   └── usePosts.ts         # Hook de estado para posts
├── pages/
│   └── Home.tsx            # Página principal
├── utils/
│   └── constants.ts        # Categorías y colores
├── App.tsx                 # Componente raíz
├── main.tsx                # Punto de entrada
└── index.css               # Estilos (Tailwind CSS)
```

### Componentes Principales

#### `PostInput.tsx`

Formulario para crear nuevos posts con:

- Textarea responsive
- Validación de contenido mínimo
- Estados de loading
- Soporte para Ctrl+Enter

#### `PostCard.tsx`

Tarjeta visual para mostrar cada post:

- Colores dinámicos según categoría
- Badge de categoría
- Indicador de confianza
- Fecha formateada

#### `FilterBar.tsx`

Barra de botones para filtrar:

- Botón "Todas" para reset
- Botones por cada categoría
- Estado visual activo/inactivo

---

## Backend: Capas y Servicios

```
backend/core/
├── domain/                 # Capa de Dominio
│   └── __init__.py
├── application/            # Capa de Aplicación
│   ├── __init__.py
│   └── ai_service.py       # MiningEngine (IA)
├── infrastructure/         # Capa de Infraestructura
│   ├── __init__.py
│   ├── views.py            # Vistas API
│   └── serializers.py      # Serializers DRF
├── models.py               # Modelo Post
├── urls.py                 # Rutas de la API
└── migrations/             # Migraciones de DB
```

### MiningEngine (ai_service.py)

El motor de IA implementa el patrón **Singleton** para cargar el modelo una sola vez:

```python
class MiningEngine:
    TAXONOMY = ["Tóxico", "Gracioso", ...]  # 12 categorías
    _classifier = None

    @classmethod
    def get_classifier(cls):
        if cls._classifier is None:
            cls._classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
        return cls._classifier

    @classmethod
    def analyze(cls, text: str) -> dict:
        classifier = cls.get_classifier()
        result = classifier(text, cls.TAXONOMY)
        return {
            "top_category": result['labels'][0],
            "confidence": result['scores'][0]
        }
```

---

## Modelo de IA

### Facebook BART Large MNLI

**Modelo utilizado:** `facebook/bart-large-mnli`

| Característica | Valor                         |
| -------------- | ----------------------------- |
| Arquitectura   | BART (Transformer)            |
| Parámetros     | ~400 millones                 |
| Tarea          | Zero-Shot Classification      |
| Idiomas        | Multilingüe (incluye español) |
| Tamaño         | ~1.5 GB                       |

### ¿Qué es Zero-Shot Classification?

Es una técnica de NLP que permite clasificar texto en categorías **sin necesidad de entrenamiento específico**. El modelo comprende el significado semántico del texto y las etiquetas de categoría, y determina cuál es más apropiada.

**Ventajas:**

- No requiere datos de entrenamiento etiquetados
- Se pueden agregar nuevas categorías sin re-entrenar
- Funciona en múltiples idiomas

---

## Instalación y Ejecución

### Requisitos

- Python 3.11+
- Node.js 18+
- uv (gestor de paquetes ultrarrápido)

### Backend

```bash
# 1. Navegar al directorio
cd sentimind_project/backend

# 2. Instalar dependencias con uv
uv sync

# 3. Ejecutar migraciones
uv run python manage.py migrate

# 4. (Opcional) Cargar datos de ejemplo
uv run python seed_data.py --silent

# 5. Iniciar servidor
uv run python manage.py runserver
```

### Frontend

```bash
# 1. Navegar al directorio
cd sentimind_project/frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev
```

### URLs de Acceso

| Servicio     | URL                          |
| ------------ | ---------------------------- |
| Frontend     | http://localhost:5173        |
| Backend API  | http://127.0.0.1:8000/api/   |
| Admin Django | http://127.0.0.1:8000/admin/ |

---

## 📝 Notas Técnicas

### Rendimiento

- El modelo de IA se carga en memoria una sola vez (patrón Singleton)
- La primera clasificación puede tomar 10-30 segundos (descarga del modelo)
- Las clasificaciones posteriores toman ~100-500ms

### Seguridad

- CORS configurado solo para localhost:5173
- CSRF deshabilitado para desarrollo
- Para producción: configurar ALLOWED_HOSTS y SECRET_KEY

### Base de Datos

- SQLite por defecto (archivo `db.sqlite3`)
- Índice en campo `category` para filtrado rápido
- Ordenamiento por fecha descendente

---

_Documentación generada para Sentimind Network - Proyecto de Minería de Datos_
_Universidad Laica Eloy Alfaro de Manabí (ULEAM) - 2026_
