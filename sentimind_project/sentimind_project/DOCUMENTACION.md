# Sentimind Network - Documentacion Completa

## Proyecto de Mineria de Datos y Despliegue de Modelos de Aprendizaje Automatico

**Universidad:** ULEAM - Universidad Laica Eloy Alfaro de Manabi

**Asignatura:** Mineria de Datos

**Fecha:** 2026

---

## Indice

1. [Informacion del Dataset](#1-informacion-del-dataset)
2. [Proceso KDD](#2-proceso-kdd)
3. [Algoritmo de Aprendizaje Supervisado](#3-algoritmo-de-aprendizaje-supervisado)
4. [Metricas de Evaluacion](#4-metricas-de-evaluacion)
5. [Sistema de Autenticacion](#5-sistema-de-autenticacion)
6. [Interfaz Web](#6-interfaz-web)
7. [Arquitectura del Sistema](#7-arquitectura-del-sistema)
8. [API Reference](#8-api-reference)
9. [Instalacion y Ejecucion](#9-instalacion-y-ejecucion)
10. [Evidencias de Funcionamiento](#10-evidencias-de-funcionamiento)

---

## 1. Informacion del Dataset

### 1.1 Fuente del Dataset

Este proyecto utiliza **Transfer Learning** con un modelo pre-entrenado de Hugging Face:

| Caracteristica | Valor |
|----------------|-------|
| **Modelo** | joeddav/xlm-roberta-large-xnli |
| **Fuente** | Hugging Face Model Hub |
| **Enlace de descarga** | https://huggingface.co/joeddav/xlm-roberta-large-xnli |
| **Arquitectura** | XLM-RoBERTa Large |
| **Parametros** | ~550 millones |
| **Idiomas soportados** | 100+ idiomas (incluido espanol) |

### 1.2 Dataset de Entrenamiento Original

El modelo base fue entrenado en:

1. **XNLI Dataset** (Cross-lingual Natural Language Inference):
   - 392,702 ejemplos de entrenamiento
   - 15 idiomas diferentes
   - Fuente: https://github.com/facebookresearch/XNLI

2. **CommonCrawl**:
   - 2.5TB de texto filtrado
   - 100 idiomas
   - Utilizado para pre-entrenamiento

### 1.3 Dataset de Evaluacion (Creado para este proyecto)

Para evaluar el modelo en nuestra tarea especifica, creamos un dataset de evaluacion:

- **72 textos** etiquetados manualmente
- **18 categorias** emocionales
- **4 ejemplos** por categoria
- Textos en **espanol** representativos de redes sociales

### 1.4 Descripcion General de los Datos

El sistema clasifica textos en **25 categorias emocionales**:

```
Emociones basicas: Alegria, Tristeza, Enojo, Miedo, Sorpresa, Asco
Emociones sociales: Amor, Odio, Verguenza, Orgullo, Envidia, Celos
Tipos de contenido: Humor, Inspiracion, Confesion, Queja, Consejo,
                    Pregunta, Reflexion, Nostalgia, Ansiedad, Frustracion
Contenido especial: Sarcasmo, Polemica, Terror
```

### 1.5 Justificacion del Problema Seleccionado

El analisis de sentimientos es relevante porque:

1. **Aplicacion practica**: Las redes sociales generan millones de textos diarios que requieren clasificacion automatica.

2. **Desafio tecnico**: La clasificacion multi-emocional es mas compleja que el analisis binario (positivo/negativo).

3. **Innovacion**: Utilizamos Zero-Shot Classification que permite clasificar sin datos de entrenamiento etiquetados.

4. **Utilidad social**: Puede ayudar a detectar contenido que requiere moderacion o identificar tendencias emocionales.

---

## 2. Proceso KDD

### 2.1 Fase 1: Seleccion de Datos

**Variables de entrada:**

| Variable | Tipo | Descripcion |
|----------|------|-------------|
| `content` | string | Texto del post a clasificar |

**Variables de salida:**

| Variable | Tipo | Descripcion |
|----------|------|-------------|
| `primary_category` | string | Emocion principal detectada |
| `primary_confidence` | float | Confianza (0-1) |
| `categories` | list | Lista de emociones detectadas |

**Eliminacion de datos irrelevantes:**
- Textos con menos de 3 caracteres son rechazados
- Textos mayores a 1000 caracteres son truncados
- Espacios en blanco al inicio/final son eliminados

### 2.2 Fase 2: Preprocesamiento

El modelo XLM-RoBERTa maneja el preprocesamiento internamente:

1. **Tokenizacion con SentencePiece (BPE)**:
   - Divide palabras en subunidades
   - Ejemplo: "corriendo" -> ["corr", "iendo"]
   - Vocabulario de ~250,000 tokens multilingues

2. **Normalizacion**:
   - Unicode NFD -> NFC
   - Eliminacion de caracteres de control

3. **Manejo de valores especiales**:
   | Caso | Manejo |
   |------|--------|
   | Emojis | Preservados (informacion emocional) |
   | URLs | Tokenizados como tokens |
   | Hashtags | Divididos en subwords |
   | Texto vacio | Rechazado |

### 2.3 Fase 3: Transformacion

**Embeddings Contextuales:**
- Dimension: 1024 por token
- Contextuales: El mismo token tiene diferentes representaciones segun contexto
- Multilingue: Embeddings comparables entre idiomas

**Zero-Shot Classification:**

El problema de clasificacion se convierte en Natural Language Inference (NLI):

```
Premisa: "Estoy muy feliz hoy"
Hipotesis: "Este texto expresa Alegria"
-> El modelo predice: Entailment (alta probabilidad)
```

**Parametros de transformacion:**
```python
HYPOTHESIS_TEMPLATE = "Este texto expresa {}"
RELATIVE_THRESHOLD = 0.90  # 90% del score maximo
MAX_EMOTIONS = 3  # Maximo de emociones por texto
```

### 2.4 Fase 4: Mineria de Datos

**Algoritmo seleccionado:** Zero-Shot Classification con XLM-RoBERTa

**Implementacion (MiningEngine):**

```python
class MiningEngine:
    TAXONOMY = [25 categorias emocionales]
    _classifier = None  # Patron Singleton
    
    @classmethod
    def analyze(cls, text: str) -> dict:
        classifier = cls.get_classifier()
        result = classifier(
            text, 
            cls.TAXONOMY,
            hypothesis_template="Este texto expresa {}",
            multi_label=True
        )
        return {
            "categories": detected_categories,
            "primary_category": result['labels'][0],
            "primary_confidence": result['scores'][0]
        }
```

**Ajuste de hiperparametros:**

| Hiperparametro | Valor | Justificacion |
|----------------|-------|---------------|
| `multi_label` | True | Permite detectar multiples emociones |
| `RELATIVE_THRESHOLD` | 0.90 | Umbral para incluir categoria |
| `MAX_EMOTIONS` | 3 | Limite de emociones por texto |
| `device` | -1 (CPU) | Compatibilidad sin GPU |

### 2.5 Fase 5: Evaluacion

Las metricas se detallan en la Seccion 4.

---

## 3. Algoritmo de Aprendizaje Supervisado

### 3.1 Algoritmo Seleccionado

**Zero-Shot Classification con XLM-RoBERTa Large XNLI**

### 3.2 Justificacion de la Eleccion

| Criterio | Zero-Shot | Naive Bayes | Logistic Regression |
|----------|-----------|-------------|---------------------|
| Datos etiquetados | No requiere | Requiere miles | Requiere miles |
| Precision en NLP | Alta | Media | Media-Alta |
| Multilingue | Si | No | No |
| Nuevas categorias | Sin re-entrenar | Re-entrenar | Re-entrenar |
| Contexto | Comprende | Bag of Words | Bag of Words |
| Emojis/Sarcasmo | Maneja bien | Problemas | Problemas |

### 3.3 Ventajas del Enfoque

1. **Sin datos etiquetados**: No necesitamos crear un dataset de miles de ejemplos
2. **Flexibilidad**: Facil agregar/modificar categorias sin re-entrenar
3. **Multilingue**: Funciona para multiples idiomas
4. **Estado del arte**: Mejor rendimiento que metodos tradicionales
5. **Transfer Learning**: Aprovecha conocimiento de tareas similares

### 3.4 Arquitectura del Modelo

```
Texto
   |
   v
Tokenizacion (SentencePiece BPE)
   |
   v
Embeddings (token + position + segment)
   |
   v
24 capas Transformer (Self-Attention)
   |
   v
Zero-Shot Classification Head
   |
   v
Probabilidades por categoria
```

---

## 4. Metricas de Evaluacion

### 4.1 Metricas Utilizadas

Para analisis de sentimientos, utilizamos:

| Metrica | Descripcion | Formula |
|---------|-------------|---------|
| **Accuracy** | Proporcion de predicciones correctas | (TP + TN) / Total |
| **Precision** | De los predichos positivos, cuantos son correctos | TP / (TP + FP) |
| **Recall** | De los positivos reales, cuantos se detectaron | TP / (TP + FN) |
| **F1-Score** | Media armonica de Precision y Recall | 2*(P*R)/(P+R) |
| **Matriz de Confusion** | Visualizacion de predicciones vs reales | - |

### 4.2 Resultados de Evaluacion

Basado en el dataset de evaluacion de 72 textos:

| Metrica | Valor |
|---------|-------|
| Accuracy | ~75% |
| Precision (weighted) | ~78% |
| Recall (weighted) | ~75% |
| F1-Score (weighted) | ~76% |

### 4.3 Script de Evaluacion

El script `evaluate_model.py` genera:
- Metricas globales
- Metricas por categoria
- Matriz de confusion
- Visualizaciones graficas

**Ejecucion:**
```bash
cd backend
uv run python evaluate_model.py
```

**Archivos generados en `evaluation_results/`:**
- `confusion_matrix.png` - Matriz de confusion visual
- `metrics_by_category.png` - Metricas por categoria
- `distribution.png` - Distribucion real vs predicho
- `metrics_summary.png` - Resumen de metricas
- `metrics.json` - Metricas en formato JSON

### 4.4 Analisis de Errores

Las confusiones mas comunes ocurren entre:
- **Tristeza <-> Nostalgia**: Emociones relacionadas
- **Enojo <-> Frustracion**: Expresiones similares
- **Humor <-> Sarcasmo**: Dificiles de distinguir sin contexto

---

## 5. Sistema de Autenticacion

### 5.1 Tecnologia

- **Backend**: Django REST Framework + SimpleJWT
- **Frontend**: React Context API + Axios Interceptors
- **Tokens**: JWT (JSON Web Tokens)

### 5.2 Flujo de Autenticacion

```
REGISTRO:
Usuario -> Formulario -> POST /api/auth/register/ -> Token JWT

LOGIN:
Usuario -> Credenciales -> POST /api/auth/login/ -> Token JWT (access + refresh)

LOGOUT:
Usuario -> POST /api/auth/logout/ -> Invalida refresh token
```

### 5.3 Endpoints de Autenticacion

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Registro de usuario |
| `/api/auth/login/` | POST | Login, retorna JWT |
| `/api/auth/logout/` | POST | Invalida refresh token |
| `/api/auth/token/refresh/` | POST | Renueva access token |
| `/api/auth/password-reset/` | POST | Solicita reset por email |
| `/api/auth/password-reset-confirm/` | POST | Confirma nueva contrasena |
| `/api/auth/me/` | GET | Datos del usuario actual |

### 5.4 Configuracion JWT

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 5.5 Proteccion de Rutas

- **Backend**: `permission_classes = [IsAuthenticated]` en vistas
- **Frontend**: Componente `ProtectedRoute` wrapper
- **Posts**: Asociados al usuario creador (campo `author`)

---

## 6. Interfaz Web

### 6.1 Funcionalidades

1. **Formulario de entrada**: Textarea para escribir posts
2. **Envio de datos**: Boton "Publicar" o Ctrl+Enter
3. **Visualizacion de resultados**: Tarjetas con categoria y confianza
4. **Filtros por categoria**: Barra de botones para filtrar posts
5. **Autenticacion**: Login, registro, recuperacion de contrasena

### 6.2 Paginas del Frontend

| Pagina | Ruta | Descripcion |
|--------|------|-------------|
| Home | `/` | Feed de posts (protegida) |
| Login | `/login` | Inicio de sesion |
| Register | `/register` | Registro de usuario |
| ForgotPassword | `/forgot-password` | Recuperar contrasena |

### 6.3 Componentes Principales

```
frontend/src/
├── pages/
│   ├── Home.tsx           # Feed principal
│   ├── Login.tsx          # Inicio de sesion
│   ├── Register.tsx       # Registro
│   └── ForgotPassword.tsx # Recuperar contrasena
├── components/
│   ├── PostCard.tsx       # Tarjeta de post
│   ├── PostInput.tsx      # Formulario de entrada
│   ├── FilterBar.tsx      # Filtros por categoria
│   ├── Navbar.tsx         # Navegacion
│   └── ProtectedRoute.tsx # Wrapper de rutas
├── contexts/
│   └── AuthContext.tsx    # Estado de autenticacion
├── adapters/
│   ├── postAdapter.ts     # API de posts
│   └── authAdapter.ts     # API de autenticacion
```

---

## 7. Arquitectura del Sistema

### 7.1 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Pages     │  │  Components │  │      Contexts           │  │
│  │  Login      │  │  PostCard   │  │  AuthContext            │  │
│  │  Register   │  │  PostInput  │  │  (Estado global)        │  │
│  │  Home       │  │  Navbar     │  │                         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                           │                                      │
│                    ┌──────┴──────┐                              │
│                    │   Adapters  │                              │
│                    │ (API calls) │                              │
│                    └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP/JSON + JWT
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (Django)                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    AUTHENTICATION                            ││
│  │  JWT (SimpleJWT) - Login, Register, Token Refresh           ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    INFRASTRUCTURE                            ││
│  │  Views (API REST) + Serializers + URLs                      ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     APPLICATION                              ││
│  │  MiningEngine (Zero-Shot Classification)                    ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                       DOMAIN                                 ││
│  │  Models: User, Post, Category, PostCategory                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │     SQLite      │
                    │   (Database)    │
                    └─────────────────┘
```

### 7.2 Tecnologias Utilizadas

**Backend:**
- Django 6.0
- Django REST Framework
- SimpleJWT (autenticacion)
- Transformers (Hugging Face)
- PyTorch (CPU)
- SQLite

**Frontend:**
- React 19
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router

---

## 8. API Reference

### 8.1 Base URL

```
http://127.0.0.1:8000/api/
```

### 8.2 Endpoints de Posts

#### Listar Posts

```http
GET /api/posts/
Authorization: Bearer <token>
```

**Query Parameters:**
| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `category` | string | Filtrar por categoria |
| `mine` | boolean | Solo mis posts |

#### Crear Post

```http
POST /api/posts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Texto del post a clasificar"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "content": "Texto del post",
  "author": {"id": 1, "username": "usuario"},
  "primary_category": "Alegria",
  "primary_confidence": 0.85,
  "categories": [
    {"name": "Alegria", "confidence": 0.85}
  ],
  "created_at": "2026-01-03T14:30:00Z"
}
```

### 8.3 Endpoints de Autenticacion

#### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "usuario",
  "password": "contrasena"
}
```

**Respuesta:**
```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@email.com"
  }
}
```

#### Registro

```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "email@ejemplo.com",
  "password": "contrasena123",
  "password2": "contrasena123",
  "first_name": "Nombre",
  "last_name": "Apellido"
}
```

---

## 9. Instalacion y Ejecucion

### 9.1 Requisitos

- Python 3.13+
- Node.js 18+
- uv (gestor de paquetes Python)

### 9.2 Backend

```bash
# 1. Navegar al directorio
cd sentimind_project/backend

# 2. Instalar dependencias
uv sync

# 3. Ejecutar migraciones
uv run python manage.py migrate

# 4. Crear superusuario (opcional)
uv run python manage.py createsuperuser

# 5. Iniciar servidor
uv run python manage.py runserver
```

### 9.3 Frontend

```bash
# 1. Navegar al directorio
cd sentimind_project/frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev
```

### 9.4 URLs de Acceso

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000/api/ |
| Admin Django | http://127.0.0.1:8000/admin/ |

### 9.5 Evaluacion del Modelo

```bash
cd backend
uv run python evaluate_model.py
```

---

## 10. Evidencias de Funcionamiento

### 10.1 Capturas Requeridas

Para el documento PDF, incluir capturas de:

1. **Preprocesamiento de datos**
   - Tokenizacion de textos
   - Notebook KDD_Process.ipynb

2. **Entrenamiento del modelo**
   - Carga del modelo XLM-RoBERTa
   - Proceso de clasificacion

3. **Metricas de evaluacion**
   - `evaluation_results/metrics_summary.png`
   - `evaluation_results/confusion_matrix.png`
   - `evaluation_results/metrics_by_category.png`

4. **Interfaz web en uso**
   - Pagina de Login
   - Pagina de Registro
   - Formulario de entrada (PostInput)
   - Resultado de clasificacion (PostCard)
   - Filtros por categoria

### 10.2 Archivos de Evidencia

Los siguientes archivos contienen evidencias del proceso:

- `backend/notebooks/KDD_Process.ipynb` - Documentacion del proceso KDD
- `backend/evaluate_model.py` - Script de evaluacion
- `backend/evaluation_results/` - Graficos y metricas
- `backend/test_classification.py` - Tests de clasificacion

---

## Notas Finales

### Rendimiento

- El modelo de IA se carga en memoria una sola vez (patron Singleton)
- Primera clasificacion: ~30 segundos (descarga del modelo)
- Clasificaciones posteriores: ~100-500ms

### Seguridad

- JWT para autenticacion
- CORS configurado para frontend
- Passwords hasheados con Django

### Base de Datos

- SQLite por defecto
- Soporte para PostgreSQL en produccion
- Migraciones con Django ORM

---

_Documentacion generada para Sentimind Network_

_Universidad Laica Eloy Alfaro de Manabi (ULEAM) - 2026_
