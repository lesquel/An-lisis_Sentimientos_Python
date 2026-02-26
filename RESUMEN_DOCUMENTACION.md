# Resumen de Documentación - Sentimind

Este documento resume los puntos clave de la documentación técnica y académica del proyecto.

## Objetivo

Analizar emociones en publicaciones de texto y exponer resultados en una aplicación web full-stack.

## Stack principal

- **Backend:** Django + DRF + JWT
- **Frontend:** React + TypeScript + Vite
- **NLP:** Zero-Shot Classification con XLM-RoBERTa
- **Infra:** Docker / Docker Compose

## Proceso de Minería de Datos (KDD)

1. Selección de datos (`content` del post)
2. Preprocesamiento (tokenización por modelo)
3. Transformación (embeddings + NLI)
4. Minería (clasificación multi-etiqueta)
5. Evaluación (accuracy, precision, recall, f1)

## Funcionalidades clave

- Registro/inicio de sesión con JWT.
- Publicación de posts y clasificación automática por emociones.
- Visualización de emoción principal + confianza.
- Filtro de posts por categoría.

## Emociones soportadas

Taxonomía de 25 categorías (básicas, sociales, de contenido y especiales), incluyendo: Alegría, Tristeza, Enojo, Miedo, Humor, Inspiración, Sarcasmo, Polémica y más.

## Ejecución recomendada

```bash
make dev
```

## Documentos relacionados

- `DOCUMENTACION.md` (principal)
- `DOCUMENTACION_COMPLETA.md` (extendida)
- `README.md` (onboarding open source)
