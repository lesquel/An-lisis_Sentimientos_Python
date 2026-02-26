"""
Script de prueba para verificar la clasificación de textos.
Ejecuta múltiples textos de prueba para validar el funcionamiento del MiningEngine.
Versión 2.0: Soporta multi-label (múltiples emociones por texto)
"""
import sys
import os

# Agregar el path del backend para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.application.ai_service import MiningEngine

# Textos de prueba con categorías esperadas (actualizadas a nueva taxonomía)
TEST_CASES = [
    # (texto, categorías esperadas posibles)
    ("Te odio, eres la peor persona del mundo, ojalá te mueras", ["Odio", "Enojo"]),
    ("Jajaja me caí en la calle y todos me vieron 😂", ["Humor", "Vergüenza"]),
    ("Nunca te rindas, cada día es una nueva oportunidad para ser mejor", ["Inspiración"]),
    ("Hoy se murió mi perro, lo extraño mucho 😢", ["Tristeza", "Nostalgia"]),
    ("Te amo con todo mi corazón, eres el amor de mi vida ❤️", ["Amor"]),
    ("El aborto debería ser legal, cambien mi opinión", ["Polémica", "Reflexión"]),
    ("Encontré una cucaracha en mi comida del restaurante 🤮", ["Asco", "Queja"]),
    ("¿Por qué existimos? ¿Cuál es el sentido de la vida?", ["Reflexión", "Pregunta"]),
    ("Confieso que una vez robé dinero de la cartera de mi mamá", ["Confesión", "Vergüenza"]),
    ("El servicio de esta empresa es pésimo, nunca contestan", ["Queja", "Frustración", "Enojo"]),
    ("¿Alguien sabe por qué el cielo es azul?", ["Pregunta"]),
    ("Anoche vi una sombra en mi cuarto y no pude dormir del miedo", ["Miedo", "Terror"]),
    ("¡Qué sorpresa! No esperaba verte aquí", ["Sorpresa", "Alegría"]),
    ("Estoy muy orgulloso de mi hijo, se graduó con honores", ["Orgullo", "Alegría"]),
    ("Extraño tanto los días de mi infancia", ["Nostalgia", "Tristeza"]),
    ("No sé si podré hacerlo, estoy muy nervioso", ["Ansiedad", "Miedo"]),
    ("Ella tiene todo lo que yo quiero, no es justo", ["Envidia", "Frustración"]),
    ("Mi mejor consejo: ahorra desde joven", ["Consejo"]),
    
    # Casos con emociones mixtas (para probar multi-label)
    ("Me río para no llorar, perdí todo pero aquí seguimos 😅😢", ["Humor", "Tristeza"]),
    ("Te amo pero a veces me haces enojar tanto", ["Amor", "Enojo", "Frustración"]),
    ("¿Por qué me dejaste? Te odio pero aún te amo", ["Amor", "Odio", "Tristeza"]),
    ("Confieso que le fui infiel a mi pareja y me arrepiento mucho 😢", ["Confesión", "Tristeza", "Vergüenza"]),
    ("Qué asco esta comida pero jaja igual me la comí toda 😂🤮", ["Asco", "Humor"]),
    ("Claro, seguro que tú nunca te equivocas 🙄", ["Sarcasmo", "Enojo"]),
]

def run_tests():
    print("=" * 80)
    print("🧪 INICIANDO TESTS DE CLASIFICACIÓN v2.0 (MULTI-LABEL)")
    print("=" * 80)
    print(f"📋 Categorías disponibles: {len(MiningEngine.TAXONOMY)}")
    print(f"   {MiningEngine.TAXONOMY}")
    print(f"🎯 Umbral relativo: {MiningEngine.RELATIVE_THRESHOLD:.0%} del score máximo")
    print(f"📊 Máx. emociones por texto: {MiningEngine.MAX_EMOTIONS}")
    print("=" * 80)
    
    results = []
    
    for i, (text, expected) in enumerate(TEST_CASES, 1):
        print(f"\n📝 Test #{i}")
        print(f"   Texto: \"{text[:70]}{'...' if len(text) > 70 else ''}\"")
        print(f"   Esperado: {expected}")
        
        try:
            analysis = MiningEngine.analyze(text)
            
            # Obtener categorías detectadas
            detected = [cat['name'] for cat in analysis['categories']]
            detected_with_conf = [(cat['name'], f"{cat['confidence']:.1%}") for cat in analysis['categories']]
            
            print(f"   🎯 Detectado: {detected_with_conf}")
            
            # Mostrar top 5 de todos los scores
            sorted_scores = sorted(analysis['all_scores'].items(), key=lambda x: x[1], reverse=True)
            top5 = sorted_scores[:5]
            print(f"   📊 Top 5: {[(cat, f'{score:.1%}') for cat, score in top5]}")
            
            # Verificar si al menos una categoría detectada está en las esperadas
            matches = set(detected) & set(expected)
            is_correct = len(matches) > 0
            
            results.append({
                'text': text,
                'expected': expected,
                'detected': detected,
                'matches': list(matches),
                'primary': analysis['primary_category'],
                'primary_conf': analysis['primary_confidence'],
                'correct': is_correct
            })
            
            if is_correct:
                print(f"   ✅ CORRECTO (coincidencias: {list(matches)})")
            else:
                print(f"   ⚠️ NO COINCIDE")
                
        except Exception as e:
            import traceback
            print(f"   ❌ ERROR: {e}")
            traceback.print_exc()
            results.append({
                'text': text,
                'expected': expected,
                'detected': None,
                'error': str(e)
            })
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 80)
    
    correct = sum(1 for r in results if r.get('correct', False))
    total = len(results)
    
    print(f"\n✅ Correctos: {correct}/{total} ({correct/total:.1%})")
    print(f"⚠️ Incorrectos: {total - correct}/{total}")
    
    # Mostrar los incorrectos
    incorrect = [r for r in results if not r.get('correct', False) and r.get('detected')]
    if incorrect:
        print("\n📋 Casos incorrectos:")
        for r in incorrect:
            print(f"\n   - \"{r['text'][:50]}...\"")
            print(f"     Esperado: {r['expected']}")
            print(f"     Detectado: {r['detected']}")
    
    return results

if __name__ == "__main__":
    run_tests()
