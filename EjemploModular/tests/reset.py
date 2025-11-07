# reset.py
import sys
import os

# BORRAR TODA LA CACHÉ DEL PROYECTO
for root, dirs, files in os.walk("."):
    for dir in dirs:
        if dir == "__pycache__":
            path = os.path.join(root, dir)
            print(f"Borrando: {path}")
            os.system(f'rmdir /S /Q "{path}"' if os.name == 'nt' else f'rm -rf "{path}"')

print("🗑️ Caché eliminada. Ejecuta: python test_runner.py")