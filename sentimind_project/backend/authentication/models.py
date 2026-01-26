"""
Modelos de autenticacion para SentiMind.
Utilizamos el modelo User por defecto de Django.
"""
from django.contrib.auth.models import User

# No necesitamos un modelo personalizado por ahora
# Django's User model incluye: username, email, password, first_name, last_name
