"""
Script de Evaluación del Modelo de Clasificación de Sentimientos.
Genera métricas formales: Accuracy, Precision, Recall, F1-Score, Matriz de Confusión.
Guarda visualizaciones para el documento PDF.

Autor: Sentimind Network Team
Fecha: 2026
"""
import sys
import os
import json
from datetime import datetime

# Agregar el path del backend para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django settings antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentimind.settings')

import django
django.setup()

from core.application.ai_service import MiningEngine

# Dependencias para métricas y visualización
try:
    import numpy as np
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        confusion_matrix,
        classification_report
    )
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Backend sin GUI para servidores
    HAS_SKLEARN = True
except ImportError as e:
    print(f"⚠️ Dependencias opcionales no instaladas: {e}")
    print("   Instala con: pip install scikit-learn matplotlib")
    HAS_SKLEARN = False


# ============================================================================
# DATASET DE EVALUACIÓN
# ============================================================================
# Conjunto de textos con etiquetas verificadas manualmente
# Cada texto tiene UNA categoría principal esperada para evaluación

EVALUATION_DATASET = [
    # ========== ALEGRÍA ==========
    ("¡Qué día tan increíble! Todo salió perfecto", "Alegría"),
    ("Estoy tan feliz, me dieron el trabajo que quería", "Alegría"),
    ("Hoy es el mejor día de mi vida, me comprometí", "Alegría"),
    ("No puedo dejar de sonreír, recibí buenas noticias", "Alegría"),
    
    # ========== TRISTEZA ==========
    ("Hoy se murió mi perro, lo extraño mucho", "Tristeza"),
    ("Me siento muy solo, nadie me entiende", "Tristeza"),
    ("Perdí a mi abuela hace un mes y sigo llorando", "Tristeza"),
    ("Me dejó mi pareja y no sé cómo seguir adelante", "Tristeza"),
    
    # ========== ENOJO ==========
    ("Estoy furioso, me mintieron en la cara", "Enojo"),
    ("No soporto la injusticia, me hierve la sangre", "Enojo"),
    ("Me enfada que la gente sea tan irresponsable", "Enojo"),
    ("Odio cuando me hacen perder el tiempo", "Enojo"),
    
    # ========== MIEDO ==========
    ("Anoche vi una sombra en mi cuarto y no pude dormir", "Miedo"),
    ("Tengo mucho miedo de lo que pueda pasar mañana", "Miedo"),
    ("Me aterra pensar en el futuro con tanta incertidumbre", "Miedo"),
    ("Escuché ruidos extraños en la noche y me paralicé", "Miedo"),
    
    # ========== SORPRESA ==========
    ("¡No puedo creerlo! ¡Gané la lotería!", "Sorpresa"),
    ("¡Qué sorpresa verte aquí! No me lo esperaba", "Sorpresa"),
    ("Me quedé sin palabras cuando vi el resultado", "Sorpresa"),
    ("¡Increíble! Nunca pensé que pasaría esto", "Sorpresa"),
    
    # ========== AMOR ==========
    ("Te amo con todo mi corazón, eres mi vida", "Amor"),
    ("Cada día me enamoro más de ti", "Amor"),
    ("Mi familia es lo más importante para mí", "Amor"),
    ("Amo a mis hijos más que a nada en el mundo", "Amor"),
    
    # ========== ODIO ==========
    ("Te odio, eres la peor persona que conozco", "Odio"),
    ("Ojalá nunca te hubiera conocido, te detesto", "Odio"),
    ("No soporto a esa persona, me cae pésimo", "Odio"),
    ("Le tengo un rencor terrible, nunca lo perdonaré", "Odio"),
    
    # ========== HUMOR ==========
    ("Jajaja me caí en la calle y todos me vieron", "Humor"),
    ("Este meme está buenísimo, no puedo parar de reír", "Humor"),
    ("Mi vida es un chiste, pero al menos me río", "Humor"),
    ("Qué gracioso cuando se equivocó de puerta", "Humor"),
    
    # ========== INSPIRACIÓN ==========
    ("Nunca te rindas, cada día es una nueva oportunidad", "Inspiración"),
    ("Cree en ti mismo y lograrás todo lo que te propongas", "Inspiración"),
    ("El éxito es la suma de pequeños esfuerzos repetidos", "Inspiración"),
    ("Hoy es el día perfecto para empezar de nuevo", "Inspiración"),
    
    # ========== NOSTALGIA ==========
    ("Extraño tanto los días de mi infancia", "Nostalgia"),
    ("Quisiera volver al tiempo cuando todo era más simple", "Nostalgia"),
    ("Recordar esos momentos me llena de melancolía", "Nostalgia"),
    ("Cómo extraño a mis amigos del colegio", "Nostalgia"),
    
    # ========== QUEJA ==========
    ("El servicio de esta empresa es pésimo", "Queja"),
    ("Me tienen harto con tanta ineficiencia", "Queja"),
    ("No es posible que todo funcione tan mal aquí", "Queja"),
    ("Llevo horas esperando y nadie me atiende", "Queja"),
    
    # ========== REFLEXIÓN ==========
    ("¿Por qué existimos? ¿Cuál es el sentido de la vida?", "Reflexión"),
    ("A veces me pregunto si tomé las decisiones correctas", "Reflexión"),
    ("La vida es un constante aprendizaje", "Reflexión"),
    ("He estado pensando mucho en mis prioridades", "Reflexión"),
    
    # ========== ANSIEDAD ==========
    ("No puedo dejar de preocuparme por todo", "Ansiedad"),
    ("Siento que algo malo va a pasar", "Ansiedad"),
    ("Estoy muy nervioso por la entrevista de mañana", "Ansiedad"),
    ("No puedo dormir pensando en todos mis problemas", "Ansiedad"),
    
    # ========== FRUSTRACIÓN ==========
    ("Ya no sé qué hacer, nada me sale bien", "Frustración"),
    ("Me esfuerzo mucho pero no veo resultados", "Frustración"),
    ("Es desesperante intentar y fallar una y otra vez", "Frustración"),
    ("Estoy cansado de que las cosas no funcionen", "Frustración"),
    
    # ========== CONFESIÓN ==========
    ("Confieso que una vez robé dinero de mi mamá", "Confesión"),
    ("Nunca se lo dije a nadie, pero yo fui quien lo hizo", "Confesión"),
    ("Tengo un secreto que me pesa mucho", "Confesión"),
    ("Debo admitir que mentí sobre eso", "Confesión"),
    
    # ========== CONSEJO ==========
    ("Mi mejor consejo: ahorra desde joven", "Consejo"),
    ("Deberías escuchar más y hablar menos", "Consejo"),
    ("Te recomiendo que estudies programación", "Consejo"),
    ("Haz ejercicio todos los días, tu cuerpo lo agradecerá", "Consejo"),
    
    # ========== PREGUNTA ==========
    ("¿Alguien sabe por qué el cielo es azul?", "Pregunta"),
    ("¿Cómo puedo mejorar mi inglés rápidamente?", "Pregunta"),
    ("¿Qué opinan ustedes sobre este tema?", "Pregunta"),
    ("¿Cuál es la mejor forma de invertir dinero?", "Pregunta"),
    
    # ========== ORGULLO ==========
    ("Estoy muy orgulloso de mi hijo, se graduó con honores", "Orgullo"),
    ("Logré mi meta después de años de esfuerzo", "Orgullo"),
    ("Me siento orgulloso de lo que he construido", "Orgullo"),
    ("Mi equipo ganó el campeonato y es el mejor", "Orgullo"),
]


def evaluate_model():
    """
    Evalúa el modelo con métricas formales de Machine Learning.
    """
    print("=" * 80)
    print("📊 EVALUACIÓN FORMAL DEL MODELO DE CLASIFICACIÓN")
    print("=" * 80)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🤖 Modelo: XLM-RoBERTa Large XNLI (Zero-Shot)")
    print(f"📋 Categorías: {len(MiningEngine.TAXONOMY)}")
    print(f"📝 Textos de evaluación: {len(EVALUATION_DATASET)}")
    print("=" * 80)
    
    # Almacenar resultados
    y_true = []  # Etiquetas reales
    y_pred = []  # Predicciones del modelo
    results = []
    
    print("\n🔬 Ejecutando clasificación...")
    
    for i, (text, expected_category) in enumerate(EVALUATION_DATASET, 1):
        try:
            analysis = MiningEngine.analyze(text)
            predicted = analysis['primary_category']
            confidence = analysis['primary_confidence']
            
            y_true.append(expected_category)
            y_pred.append(predicted)
            
            is_correct = predicted == expected_category
            results.append({
                'text': text[:50] + '...' if len(text) > 50 else text,
                'expected': expected_category,
                'predicted': predicted,
                'confidence': confidence,
                'correct': is_correct
            })
            
            status = "✅" if is_correct else "❌"
            print(f"  {i:3d}. {status} [{predicted}] ({confidence:.1%}) - {text[:40]}...")
            
        except Exception as e:
            print(f"  {i:3d}. ❌ ERROR: {e}")
            y_true.append(expected_category)
            y_pred.append("Error")
    
    print("\n" + "=" * 80)
    print("📈 MÉTRICAS DE EVALUACIÓN")
    print("=" * 80)
    
    # Calcular métricas
    metrics = {}
    
    # Accuracy
    metrics['accuracy'] = accuracy_score(y_true, y_pred)
    print(f"\n🎯 ACCURACY: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    
    # Obtener etiquetas únicas presentes en los datos
    labels = sorted(list(set(y_true + y_pred)))
    
    # Precision, Recall, F1 (weighted para manejar desbalance)
    metrics['precision_weighted'] = precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    metrics['recall_weighted'] = recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    metrics['f1_weighted'] = f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    
    print(f"\n📊 MÉTRICAS WEIGHTED (promedio ponderado):")
    print(f"   Precision: {metrics['precision_weighted']:.4f}")
    print(f"   Recall:    {metrics['recall_weighted']:.4f}")
    print(f"   F1-Score:  {metrics['f1_weighted']:.4f}")
    
    # Precision, Recall, F1 (macro para ver rendimiento por clase)
    metrics['precision_macro'] = precision_score(y_true, y_pred, labels=labels, average='macro', zero_division=0)
    metrics['recall_macro'] = recall_score(y_true, y_pred, labels=labels, average='macro', zero_division=0)
    metrics['f1_macro'] = f1_score(y_true, y_pred, labels=labels, average='macro', zero_division=0)
    
    print(f"\n📊 MÉTRICAS MACRO (promedio simple por clase):")
    print(f"   Precision: {metrics['precision_macro']:.4f}")
    print(f"   Recall:    {metrics['recall_macro']:.4f}")
    print(f"   F1-Score:  {metrics['f1_macro']:.4f}")
    
    # Reporte de clasificación completo
    print("\n" + "=" * 80)
    print("📋 REPORTE DE CLASIFICACIÓN POR CATEGORÍA")
    print("=" * 80)
    
    report = classification_report(y_true, y_pred, labels=labels, zero_division=0)
    print(report)
    
    # Matriz de confusión
    print("\n" + "=" * 80)
    print("🔢 MATRIZ DE CONFUSIÓN")
    print("=" * 80)
    
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    metrics['confusion_matrix'] = cm.tolist()
    
    # Imprimir matriz en formato legible
    print(f"\nEtiquetas: {labels}")
    print("\nMatriz (filas=real, columnas=predicho):")
    for i, row in enumerate(cm):
        print(f"  {labels[i]:15s}: {row}")
    
    return metrics, results, y_true, y_pred, labels


def generate_visualizations(y_true, y_pred, labels, output_dir='evaluation_results'):
    """
    Genera visualizaciones y las guarda como imágenes.
    """
    if not HAS_SKLEARN:
        print("⚠️ No se pueden generar visualizaciones sin matplotlib")
        return
    
    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📊 Generando visualizaciones en '{output_dir}/'...")
    
    # 1. Matriz de Confusión con Heatmap
    plt.figure(figsize=(14, 12))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # Usar solo las clases que aparecen en los datos
    present_labels = [l for l in labels if l in y_true or l in y_pred]
    cm_present = confusion_matrix(y_true, y_pred, labels=present_labels)
    
    plt.imshow(cm_present, interpolation='nearest', cmap='Blues')
    plt.title('Matriz de Confusión - Clasificación de Emociones\nModelo: XLM-RoBERTa (Zero-Shot)', fontsize=14, fontweight='bold')
    plt.colorbar(label='Cantidad')
    
    tick_marks = np.arange(len(present_labels))
    plt.xticks(tick_marks, present_labels, rotation=45, ha='right', fontsize=9)
    plt.yticks(tick_marks, present_labels, fontsize=9)
    
    # Añadir valores en las celdas
    thresh = cm_present.max() / 2.
    for i in range(cm_present.shape[0]):
        for j in range(cm_present.shape[1]):
            plt.text(j, i, format(cm_present[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm_present[i, j] > thresh else "black",
                    fontsize=8)
    
    plt.ylabel('Categoría Real', fontsize=12)
    plt.xlabel('Categoría Predicha', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/confusion_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Matriz de confusión guardada: {output_dir}/confusion_matrix.png")
    
    # 2. Gráfico de Métricas por Categoría
    plt.figure(figsize=(14, 8))
    
    # Calcular métricas por clase
    from sklearn.metrics import precision_recall_fscore_support
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=present_labels, zero_division=0
    )
    
    x = np.arange(len(present_labels))
    width = 0.25
    
    bars1 = plt.bar(x - width, precision, width, label='Precision', color='#667eea')
    bars2 = plt.bar(x, recall, width, label='Recall', color='#764ba2')
    bars3 = plt.bar(x + width, f1, width, label='F1-Score', color='#10b981')
    
    plt.xlabel('Categoría', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title('Métricas de Clasificación por Categoría\nModelo: XLM-RoBERTa (Zero-Shot)', fontsize=14, fontweight='bold')
    plt.xticks(x, present_labels, rotation=45, ha='right', fontsize=9)
    plt.ylim(0, 1.1)
    plt.legend(loc='upper right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/metrics_by_category.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Métricas por categoría guardadas: {output_dir}/metrics_by_category.png")
    
    # 3. Distribución de Predicciones
    plt.figure(figsize=(12, 6))
    
    from collections import Counter
    pred_counts = Counter(y_pred)
    true_counts = Counter(y_true)
    
    all_cats = sorted(set(list(pred_counts.keys()) + list(true_counts.keys())))
    x = np.arange(len(all_cats))
    width = 0.35
    
    pred_values = [pred_counts.get(cat, 0) for cat in all_cats]
    true_values = [true_counts.get(cat, 0) for cat in all_cats]
    
    plt.bar(x - width/2, true_values, width, label='Real', color='#667eea')
    plt.bar(x + width/2, pred_values, width, label='Predicho', color='#764ba2')
    
    plt.xlabel('Categoría', fontsize=12)
    plt.ylabel('Cantidad', fontsize=12)
    plt.title('Distribución de Categorías: Real vs Predicho', fontsize=14, fontweight='bold')
    plt.xticks(x, all_cats, rotation=45, ha='right', fontsize=9)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Distribución guardada: {output_dir}/distribution.png")
    
    # 4. Resumen de Métricas
    plt.figure(figsize=(10, 6))
    
    metrics_summary = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision\n(weighted)': precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0),
        'Recall\n(weighted)': recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0),
        'F1-Score\n(weighted)': f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0),
    }
    
    colors = ['#667eea', '#764ba2', '#10b981', '#f59e0b']
    bars = plt.bar(metrics_summary.keys(), metrics_summary.values(), color=colors)
    
    # Añadir valores encima de las barras
    for bar, value in zip(bars, metrics_summary.values()):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{value:.2%}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.ylim(0, 1.2)
    plt.ylabel('Score', fontsize=12)
    plt.title('Resumen de Métricas Globales\nModelo: XLM-RoBERTa (Zero-Shot)', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/metrics_summary.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Resumen de métricas guardado: {output_dir}/metrics_summary.png")


def save_results(metrics, results, output_dir='evaluation_results'):
    """
    Guarda los resultados en archivos JSON y CSV.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar métricas en JSON
    metrics_file = f'{output_dir}/metrics.json'
    
    # Convertir numpy arrays a listas para JSON
    metrics_json = {}
    for key, value in metrics.items():
        if isinstance(value, np.ndarray):
            metrics_json[key] = value.tolist()
        elif isinstance(value, (np.float32, np.float64)):
            metrics_json[key] = float(value)
        else:
            metrics_json[key] = value
    
    metrics_json['timestamp'] = datetime.now().isoformat()
    metrics_json['model'] = 'XLM-RoBERTa Large XNLI'
    metrics_json['dataset_size'] = len(results)
    
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics_json, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Métricas guardadas: {metrics_file}")
    
    # Guardar resultados detallados en JSON
    results_file = f'{output_dir}/detailed_results.json'
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Resultados detallados guardados: {results_file}")


def main():
    """
    Función principal de evaluación.
    """
    if not HAS_SKLEARN:
        print("❌ Error: Se requiere scikit-learn y matplotlib")
        print("   Instala con: pip install scikit-learn matplotlib")
        return
    
    # Ejecutar evaluación
    metrics, results, y_true, y_pred, labels = evaluate_model()
    
    # Generar visualizaciones
    output_dir = 'evaluation_results'
    generate_visualizations(y_true, y_pred, labels, output_dir)
    
    # Guardar resultados
    print(f"\n💾 Guardando resultados...")
    save_results(metrics, results, output_dir)
    
    # Resumen final
    print("\n" + "=" * 80)
    print("✅ EVALUACIÓN COMPLETADA")
    print("=" * 80)
    print(f"\n📁 Archivos generados en '{output_dir}/':")
    print("   - confusion_matrix.png     : Matriz de confusión visual")
    print("   - metrics_by_category.png  : Métricas por categoría")
    print("   - distribution.png         : Distribución real vs predicho")
    print("   - metrics_summary.png      : Resumen de métricas globales")
    print("   - metrics.json             : Métricas en formato JSON")
    print("   - detailed_results.json    : Resultados detallados")
    print("\n📊 Resumen de métricas:")
    print(f"   Accuracy:        {metrics['accuracy']:.2%}")
    print(f"   Precision (w):   {metrics['precision_weighted']:.2%}")
    print(f"   Recall (w):      {metrics['recall_weighted']:.2%}")
    print(f"   F1-Score (w):    {metrics['f1_weighted']:.2%}")


if __name__ == "__main__":
    main()
