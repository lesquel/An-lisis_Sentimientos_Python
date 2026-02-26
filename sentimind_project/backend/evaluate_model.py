"""
Script de Evaluacion del Modelo de Clasificacion de Sentimientos.
Genera metricas formales: Accuracy, Precision, Recall, F1-Score, Matriz de Confusion.
"""
import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentimind.settings')

import django
django.setup()

from core.application.ai_service import MiningEngine

try:
    import numpy as np
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report
    )
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    HAS_SKLEARN = True
except ImportError as e:
    print(f"Dependencias no instaladas: {e}")
    print("Instala con: pip install scikit-learn matplotlib")
    HAS_SKLEARN = False

# Dataset de evaluacion
EVALUATION_DATASET = [
    ("Qué día tan increíble! Todo salió perfecto", "Alegría"),
    ("Estoy tan feliz, me dieron el trabajo que quería", "Alegría"),
    ("Hoy es el mejor día de mi vida", "Alegría"),
    ("No puedo dejar de sonreír, recibí buenas noticias", "Alegría"),
    
    ("Hoy se murió mi perro, lo extraño mucho", "Tristeza"),
    ("Me siento muy solo, nadie me entiende", "Tristeza"),
    ("Perdí a mi abuela hace un mes y sigo llorando", "Tristeza"),
    ("Me dejó mi pareja y no sé cómo seguir", "Tristeza"),
    
    ("Estoy furioso, me mintieron en la cara", "Enojo"),
    ("No soporto la injusticia, me hierve la sangre", "Enojo"),
    ("Me enfada que la gente sea tan irresponsable", "Enojo"),
    ("Odio cuando me hacen perder el tiempo", "Enojo"),
    
    ("Anoche vi una sombra en mi cuarto y no pude dormir", "Miedo"),
    ("Tengo mucho miedo de lo que pueda pasar mañana", "Miedo"),
    ("Me aterra pensar en el futuro", "Miedo"),
    ("Escuché ruidos extraños en la noche y me paralicé", "Miedo"),
    
    ("No puedo creerlo! Gané la lotería!", "Sorpresa"),
    ("Qué sorpresa verte aquí! No me lo esperaba", "Sorpresa"),
    ("Me quedé sin palabras cuando vi el resultado", "Sorpresa"),
    ("Increíble! Nunca pensé que pasaría esto", "Sorpresa"),
    
    ("Te amo con todo mi corazón, eres mi vida", "Amor"),
    ("Cada día me enamoro más de ti", "Amor"),
    ("Mi familia es lo más importante para mí", "Amor"),
    ("Amo a mis hijos más que a nada en el mundo", "Amor"),
    
    ("Jajaja me caí en la calle y todos me vieron", "Humor"),
    ("Este meme está buenísimo, no puedo parar de reír", "Humor"),
    ("Mi vida es un chiste, pero al menos me río", "Humor"),
    ("Qué gracioso cuando se equivocó de puerta", "Humor"),
    
    ("Nunca te rindas, cada día es una nueva oportunidad", "Inspiración"),
    ("Cree en ti mismo y lograrás todo", "Inspiración"),
    ("El éxito es la suma de pequeños esfuerzos", "Inspiración"),
    ("Hoy es el día perfecto para empezar de nuevo", "Inspiración"),
    
    ("Extraño tanto los días de mi infancia", "Nostalgia"),
    ("Quisiera volver al tiempo cuando todo era más simple", "Nostalgia"),
    ("Recordar esos momentos me llena de melancolía", "Nostalgia"),
    ("Cómo extraño a mis amigos del colegio", "Nostalgia"),
    
    ("El servicio de esta empresa es pésimo", "Queja"),
    ("Me tienen harto con tanta ineficiencia", "Queja"),
    ("No es posible que todo funcione tan mal", "Queja"),
    ("Llevo horas esperando y nadie me atiende", "Queja"),
]


def evaluate_model():
    """Evalua el modelo con metricas formales."""
    print("=" * 80)
    print("EVALUACION FORMAL DEL MODELO DE CLASIFICACION")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modelo: XLM-RoBERTa Large XNLI (Zero-Shot)")
    print(f"Textos de evaluacion: {len(EVALUATION_DATASET)}")
    print("=" * 80)
    
    y_true = []
    y_pred = []
    results = []
    
    print("\nEjecutando clasificacion...")
    
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
            
            status = "OK" if is_correct else "X"
            print(f"  {i:3d}. [{status}] {predicted} ({confidence:.1%}) - {text[:40]}...")
            
        except Exception as e:
            print(f"  {i:3d}. ERROR: {e}")
            y_true.append(expected_category)
            y_pred.append("Error")
    
    print("\n" + "=" * 80)
    print("METRICAS DE EVALUACION")
    print("=" * 80)
    
    metrics = {}
    labels = sorted(list(set(y_true + y_pred)))
    
    metrics['accuracy'] = accuracy_score(y_true, y_pred)
    print(f"\nACCURACY: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    
    metrics['precision_weighted'] = precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    metrics['recall_weighted'] = recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    metrics['f1_weighted'] = f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    
    print(f"\nMETRICAS WEIGHTED:")
    print(f"   Precision: {metrics['precision_weighted']:.4f}")
    print(f"   Recall:    {metrics['recall_weighted']:.4f}")
    print(f"   F1-Score:  {metrics['f1_weighted']:.4f}")
    
    print("\n" + "=" * 80)
    print("REPORTE DE CLASIFICACION POR CATEGORIA")
    print("=" * 80)
    
    report = classification_report(y_true, y_pred, labels=labels, zero_division=0)
    print(report)
    
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    metrics['confusion_matrix'] = cm.tolist()
    
    return metrics, results, y_true, y_pred, labels


def generate_visualizations(y_true, y_pred, labels, output_dir='evaluation_results'):
    """Genera visualizaciones."""
    if not HAS_SKLEARN:
        print("No se pueden generar visualizaciones sin matplotlib")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nGenerando visualizaciones en '{output_dir}/'...")
    
    # Matriz de Confusion
    plt.figure(figsize=(12, 10))
    present_labels = [l for l in labels if l in y_true or l in y_pred]
    cm = confusion_matrix(y_true, y_pred, labels=present_labels)
    
    plt.imshow(cm, interpolation='nearest', cmap='Blues')
    plt.title('Matriz de Confusion - Clasificacion de Emociones', fontsize=14, fontweight='bold')
    plt.colorbar(label='Cantidad')
    
    tick_marks = np.arange(len(present_labels))
    plt.xticks(tick_marks, present_labels, rotation=45, ha='right', fontsize=9)
    plt.yticks(tick_marks, present_labels, fontsize=9)
    
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    
    plt.ylabel('Categoria Real')
    plt.xlabel('Categoria Predicha')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/confusion_matrix.png', dpi=150)
    plt.close()
    print(f"   Matriz de confusion guardada: {output_dir}/confusion_matrix.png")
    
    # Resumen de Metricas
    plt.figure(figsize=(10, 6))
    
    metrics_summary = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0),
        'Recall': recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0),
        'F1-Score': f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0),
    }
    
    colors = ['#667eea', '#764ba2', '#10b981', '#f59e0b']
    bars = plt.bar(metrics_summary.keys(), metrics_summary.values(), color=colors)
    
    for bar, value in zip(bars, metrics_summary.values()):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{value:.2%}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.ylim(0, 1.2)
    plt.ylabel('Score')
    plt.title('Resumen de Metricas Globales', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/metrics_summary.png', dpi=150)
    plt.close()
    print(f"   Resumen de metricas guardado: {output_dir}/metrics_summary.png")


def save_results(metrics, results, output_dir='evaluation_results'):
    """Guarda resultados en JSON."""
    os.makedirs(output_dir, exist_ok=True)
    
    metrics_json = {}
    for key, value in metrics.items():
        if hasattr(value, 'tolist'):
            metrics_json[key] = value.tolist()
        elif isinstance(value, (np.float32, np.float64)):
            metrics_json[key] = float(value)
        else:
            metrics_json[key] = value
    
    metrics_json['timestamp'] = datetime.now().isoformat()
    metrics_json['model'] = 'XLM-RoBERTa Large XNLI'
    
    with open(f'{output_dir}/metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics_json, f, indent=2, ensure_ascii=False)
    print(f"   Metricas guardadas: {output_dir}/metrics.json")


def main():
    """Funcion principal."""
    if not HAS_SKLEARN:
        print("Error: Se requiere scikit-learn y matplotlib")
        return
    
    metrics, results, y_true, y_pred, labels = evaluate_model()
    
    output_dir = 'evaluation_results'
    generate_visualizations(y_true, y_pred, labels, output_dir)
    save_results(metrics, results, output_dir)
    
    print("\n" + "=" * 80)
    print("EVALUACION COMPLETADA")
    print("=" * 80)
    print(f"\nArchivos generados en '{output_dir}/':")
    print("   - confusion_matrix.png")
    print("   - metrics_summary.png")
    print("   - metrics.json")
    print(f"\nAccuracy: {metrics['accuracy']:.2%}")
    print(f"F1-Score: {metrics['f1_weighted']:.2%}")


if __name__ == "__main__":
    main()
