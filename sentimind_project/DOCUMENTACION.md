# Sentimind Network - Documentacion Completa

## Proyecto de Mineria de Datos y Aprendizaje Automatico

**Universidad:** ULEAM - Universidad Laica Eloy Alfaro de Manabi  
**Fecha:** 2026

---

## Indice

1. [Dataset y Fuente de Datos](#1-dataset-y-fuente-de-datos)
2. [Proceso KDD](#2-proceso-kdd)
3. [Algoritmo de Aprendizaje Supervisado](#3-algoritmo-de-aprendizaje-supervisado)
4. [Metricas de Evaluacion](#4-metricas-de-evaluacion)
5. [Sistema de Autenticacion](#5-sistema-de-autenticacion)
6. [Interfaz Web](#6-interfaz-web)
7. [API Reference](#7-api-reference)
8. [Instalacion y Ejecucion](#8-instalacion-y-ejecucion)

---

## 1. Dataset y Fuente de Datos

### 1.1 Fuente del Modelo

| Caracteristica | Valor |
|----------------|-------|
| **Modelo** | joeddav/xlm-roberta-large-xnli |
| **Fuente** | Hugging Face Model Hub |
| **Enlace** | https://huggingface.co/joeddav/xlm-roberta-large-xnli |
| **Arquitectura** | XLM-RoBERTa Large |
| **Parametros** | ~550 millones |
| **Idiomas** | 100+ idiomas (incluido espanol) |

### 1.2 Dataset de Entrenamiento Original

El modelo fue entrenado en:

- **XNLI Dataset**: 392,702 ejemplos de entrenamiento en 15 idiomas
- **CommonCrawl**: 2.5TB de texto filtrado en 100 idiomas

### 1.3 Justificacion del Problema

El analisis de sentimientos es relevante porque:

1. **Aplicacion practica**: Las redes sociales generan millones de textos que requieren clasificacion automatica
2. **Desafio tecnico**: La clasificacion multi-emocional es mas compleja que el analisis binario
3. **Innovacion**: Zero-Shot Classification permite clasificar sin datos de entrenamiento etiquetados
4. **Utilidad social**: Detectar contenido que requiere moderacion o identificar tendencias emocionales

---

## 2. Proceso KDD

### 2.1 Fase 1: Seleccion de Datos

**Variables de entrada:**
- `content` (string): Texto del post a clasificar

**Variables de salida:**
- `primary_category` (string): Emocion principal detectada
- `primary_confidence` (float): Confianza (0-1)
- `categories` (list): Lista de emociones detectadas

**Filtros aplicados:**
- Textos con menos de 3 caracteres son rechazados
- Textos mayores a 1000 caracteres son truncados

### 2.2 Fase 2: Preprocesamiento

El modelo XLM-RoBERTa maneja el preprocesamiento internamente:

- **Tokenizacion**: SentencePiece con BPE (~250,000 tokens)
- **Normalizacion**: Unicode NFD a NFC
- **Emojis**: Preservados (contienen informacion emocional)

### 2.3 Fase 3: Transformacion

- **Embeddings**: Dimension 1024 por token
- **Zero-Shot**: Convierte clasificacion en Natural Language Inference

```
Premisa: "Estoy muy feliz hoy"
Hipotesis: "Este texto expresa Alegria"
-> Modelo predice: Entailment (alta probabilidad)
```

### 2.4 Fase 4: Mineria de Datos

**Algoritmo:** Zero-Shot Classification con XLM-RoBERTa

**Hiperparametros:**
- `multi_label`: True (detecta multiples emociones)
- `RELATIVE_THRESHOLD`: 0.90 (umbral para incluir categoria)
- `MAX_EMOTIONS`: 3 (maximo de emociones por texto)

### 2.5 Fase 5: Evaluacion

Ver seccion 4 para metricas detalladas.

---

## 3. Algoritmo de Aprendizaje Supervisado

### 3.1 Algoritmo Seleccionado

**Zero-Shot Classification con XLM-RoBERTa Large XNLI**

### 3.2 Justificacion

| Criterio | Zero-Shot | Naive Bayes | Logistic Regression |
|----------|-----------|-------------|---------------------|
| Datos etiquetados | No requiere | Requiere miles | Requiere miles |
| Precision en NLP | Alta | Media | Media-Alta |
| Multilingue | Si | No | No |
| Nuevas categorias | Sin re-entrenar | Re-entrenar | Re-entrenar |

### 3.3 Categorias (25 emociones)

```
Basicas: Alegria, Tristeza, Enojo, Miedo, Sorpresa, Asco
Sociales: Amor, Odio, Verguenza, Orgullo, Envidia, Celos
Contenido: Humor, Inspiracion, Confesion, Queja, Consejo,
           Pregunta, Reflexion, Nostalgia, Ansiedad, Frustracion
Especial: Sarcasmo, Polemica, Terror
```

---

## 4. Metricas de Evaluacion

### 4.1 Metricas Utilizadas

| Metrica | Descripcion |
|---------|-------------|
| **Accuracy** | Proporcion de predicciones correctas |
| **Precision** | De los predichos positivos, cuantos son correctos |
| **Recall** | De los positivos reales, cuantos se detectaron |
| **F1-Score** | Media armonica de Precision y Recall |
| **Matriz de Confusion** | Visualizacion de predicciones vs reales |

### 4.2 Ejecucion de Evaluacion

```bash
cd backend
uv run python evaluate_model.py
```

**Archivos generados:**
- `evaluation_results/confusion_matrix.png`
- `evaluation_results/metrics_summary.png`
- `evaluation_results/metrics.json`

---

## 5. Sistema de Autenticacion

### 5.1 Tecnologia

- **Backend**: Django REST Framework + SimpleJWT
- **Frontend**: React Context API + Axios Interceptors
- **Tokens**: JWT (JSON Web Tokens)

### 5.2 Endpoints

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| `/api/auth/login/` | POST | Login, retorna JWT |
| `/api/auth/register/` | POST | Registro de usuario |
| `/api/auth/logout/` | POST | Invalida refresh token |
| `/api/auth/token/refresh/` | POST | Renueva access token |
| `/api/auth/me/` | GET | Datos del usuario actual |
| `/api/auth/password-reset/` | POST | Solicita reset por email |

### 5.3 Configuracion JWT

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

---

## 6. Interfaz Web

### 6.1 Paginas

| Pagina | Ruta | Descripcion |
|--------|------|-------------|
| Home | `/` | Feed de posts (protegida) |
| Login | `/login` | Inicio de sesion |
| Register | `/register` | Registro de usuario |
| ForgotPassword | `/forgot-password` | Recuperar contrasena |

### 6.2 Funcionalidades

1. **Formulario de entrada**: Textarea para escribir posts
2. **Envio de datos**: Boton "Publicar" o Ctrl+Enter
3. **Visualizacion de resultados**: Tarjetas con categoria y confianza
4. **Filtros por categoria**: Barra de botones para filtrar
5. **Autenticacion**: Login, registro, logout

---

## 7. API Reference

### 7.1 Endpoints de Posts

**Listar Posts:**
```http
GET /api/posts/
Authorization: Bearer <token>
```

**Crear Post:**
```http
POST /api/posts/
Authorization: Bearer <token>
Content-Type: application/json

{"content": "Texto del post"}
```

**Respuesta:**
```json
{
  "id": 1,
  "content": "Texto del post",
  "author": {"id": 1, "username": "usuario"},
  "primary_category": "Alegria",
  "primary_confidence": 0.85,
  "categories": [{"name": "Alegria", "confidence": 0.85}],
  "created_at": "2026-01-03T14:30:00Z"
}
```

---

## 8. Instalacion y Ejecucion

### 8.1 Requisitos

- Python 3.13+
- Node.js 18+
- uv (gestor de paquetes)

### 8.2 Backend

```bash
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

### 8.3 Frontend

```bash
cd frontend
npm install
npm run dev
```

### 8.4 URLs

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000/api/ |
| Admin Django | http://127.0.0.1:8000/admin/ |

---

_Universidad Laica Eloy Alfaro de Manabi (ULEAM) - 2026_
