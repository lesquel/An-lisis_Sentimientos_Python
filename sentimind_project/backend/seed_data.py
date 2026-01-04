"""
Script de Seed de Datos para Sentimind Network.
Ejecutar con: uv run python seed_data.py

Este script pobla la base de datos con posts de ejemplo
para cada categoría disponible en el sistema.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentimind.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Post

# Datos de ejemplo para cada categoría
SEED_POSTS = [
    # Tóxico
    {
        "content": "Odio cuando la gente no sabe hacer su trabajo, son unos inútiles.",
        "category": "Tóxico",
        "confidence": 0.89
    },
    {
        "content": "Mi vecino es insoportable, ojalá se mude lejos de aquí.",
        "category": "Tóxico",
        "confidence": 0.85
    },
    
    # Gracioso
    {
        "content": "Mi perro intenta atrapar su cola desde hace 20 minutos, creo que es su cardio del día 😂",
        "category": "Gracioso",
        "confidence": 0.92
    },
    {
        "content": "Le dije a mi jefe que llegaría tarde porque mi pez se ahogó. No preguntó más.",
        "category": "Gracioso",
        "confidence": 0.88
    },
    {
        "content": "Acabo de descubrir que llevo la camiseta al revés... desde ayer.",
        "category": "Gracioso",
        "confidence": 0.91
    },
    
    # Inspirador
    {
        "content": "Después de 5 años de esfuerzo, finalmente terminé mi carrera universitaria. ¡Nunca es tarde!",
        "category": "Inspirador",
        "confidence": 0.94
    },
    {
        "content": "Cada día es una nueva oportunidad para ser mejor que ayer. No te rindas.",
        "category": "Inspirador",
        "confidence": 0.87
    },
    
    # Triste
    {
        "content": "Hoy hace un año que perdí a mi abuela. La extraño mucho.",
        "category": "Triste",
        "confidence": 0.93
    },
    {
        "content": "A veces me siento solo aunque esté rodeado de gente.",
        "category": "Triste",
        "confidence": 0.86
    },
    
    # Romántico
    {
        "content": "Llevo 10 años con mi esposa y cada día me enamoro más de ella.",
        "category": "Romántico",
        "confidence": 0.91
    },
    {
        "content": "Hoy tuve mi primera cita y fue mágica. Creo que encontré a alguien especial.",
        "category": "Romántico",
        "confidence": 0.88
    },
    
    # Polémico
    {
        "content": "Creo que el sistema educativo necesita una reforma completa, no funciona.",
        "category": "Polémico",
        "confidence": 0.82
    },
    {
        "content": "Las redes sociales están destruyendo la comunicación real entre personas.",
        "category": "Polémico",
        "confidence": 0.79
    },
    
    # Asqueroso
    {
        "content": "Encontré un pelo en mi comida del restaurante. Nunca vuelvo.",
        "category": "Asqueroso",
        "confidence": 0.84
    },
    {
        "content": "Mi compañero de cuarto dejó comida podrida en el refrigerador por un mes.",
        "category": "Asqueroso",
        "confidence": 0.87
    },
    
    # Filosófico
    {
        "content": "¿Realmente tenemos libre albedrío o todo está predeterminado?",
        "category": "Filosófico",
        "confidence": 0.89
    },
    {
        "content": "La vida es como un río, fluye constantemente y nunca puedes pisar el mismo agua dos veces.",
        "category": "Filosófico",
        "confidence": 0.85
    },
    
    # Confesión
    {
        "content": "Confesión: Nunca he leído Harry Potter y finjo que sí cuando todos hablan de ello.",
        "category": "Confesión",
        "confidence": 0.90
    },
    {
        "content": "A veces como postre antes de la comida cuando nadie me ve.",
        "category": "Confesión",
        "confidence": 0.83
    },
    
    # Queja
    {
        "content": "El servicio de internet en mi ciudad es terrible, pago mucho por casi nada.",
        "category": "Queja",
        "confidence": 0.88
    },
    {
        "content": "¿Por qué los hospitales tienen tantas horas de espera? Es frustrante.",
        "category": "Queja",
        "confidence": 0.86
    },
    
    # Curiosidad
    {
        "content": "¿Sabían que los pulpos tienen tres corazones y sangre azul?",
        "category": "Curiosidad",
        "confidence": 0.91
    },
    {
        "content": "Acabo de descubrir que las abejas pueden reconocer rostros humanos.",
        "category": "Curiosidad",
        "confidence": 0.87
    },
    
    # Terror
    {
        "content": "Anoche escuché pasos en el ático pero vivo solo. No subí a revisar.",
        "category": "Terror",
        "confidence": 0.92
    },
    {
        "content": "Mi hija de 3 años me dijo que 'el hombre de la esquina' la visita por las noches.",
        "category": "Terror",
        "confidence": 0.89
    },
]


def run_seed():
    """Ejecuta el seed de datos."""
    print("🌱 Iniciando seed de datos para Sentimind Network...")
    print("-" * 50)
    
    # Limpiar posts existentes (opcional)
    existing_count = Post.objects.count()
    if existing_count > 0:
        print(f"⚠️  Se encontraron {existing_count} posts existentes.")
        response = input("¿Desea eliminarlos antes de insertar los nuevos? (s/n): ")
        if response.lower() == 's':
            Post.objects.all().delete()
            print("🗑️  Posts existentes eliminados.")
    
    # Insertar posts de seed
    created_count = 0
    for post_data in SEED_POSTS:
        Post.objects.create(**post_data)
        created_count += 1
        print(f"  ✅ [{post_data['category']}] {post_data['content'][:50]}...")
    
    print("-" * 50)
    print(f"🎉 ¡Seed completado! Se crearon {created_count} posts.")
    
    # Mostrar resumen por categoría
    print("\n📊 Resumen por categoría:")
    from django.db.models import Count
    categories = Post.objects.values('category').annotate(count=Count('id')).order_by('-count')
    for cat in categories:
        print(f"   • {cat['category']}: {cat['count']} posts")


def run_seed_silent():
    """Ejecuta el seed sin preguntar (para automatización)."""
    print("🌱 Ejecutando seed silencioso...")
    
    for post_data in SEED_POSTS:
        Post.objects.create(**post_data)
    
    print(f"✅ Se crearon {len(SEED_POSTS)} posts de ejemplo.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--silent":
        run_seed_silent()
    else:
        run_seed()
