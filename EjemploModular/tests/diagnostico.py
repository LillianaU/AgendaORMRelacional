# diagnostico.py
import sys
sys.path.append('.')

# LIMPIAR CACHÉ DE MÓDULOS
if 'models.telefono' in sys.modules:
    del sys.modules['models.telefono']
if 'models.email' in sys.modules:
    del sys.modules['models.email']

# Importar y verificar RUTA REAL del archivo
import models.telefono
import models.email

print("="*60)
print("DIAGNOSTICO DE ARCHIVOS")
print("="*60)
print(f"Ruta telefono.py: {models.telefono.__file__}")
print(f"Ruta email.py: {models.email.__file__}")
print("="*60)

# Mostrar contenido REAL que Python está viendo
print("\nCONTENIDO DE models/telefono.py:")
with open(models.telefono.__file__, 'r', encoding='utf-8') as f:
    print(f.read())

print("\nCONTENIDO DE models/email.py:")
with open(models.email.__file__, 'r', encoding='utf-8') as f:
    print(f.read())