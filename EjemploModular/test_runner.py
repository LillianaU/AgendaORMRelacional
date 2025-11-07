# test_runner.py - EN RAÍZ DEL PROYECTO
import subprocess
import sys
import os

# Directorio RAÍZ absoluto
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

print("="*60)
print("🧪 EJECUTOR DE TESTS")
print(f"📁 Raíz: {ROOT_DIR}")
print("="*60)

# Tests con rutas absolutas
tests = [
    (os.path.join(ROOT_DIR, "tests", "test_modelos.py"), "MODELOS"),
    (os.path.join(ROOT_DIR, "tests", "test_cruds.py"), "CRUDs")
]

for test_path, nombre in tests:
    print(f"\n{'='*40}")
    print(f"📂 {nombre}")
    print('='*40)
    
    result = subprocess.run(
        [sys.executable, test_path],
        capture_output=True,
        text=True,
        cwd=ROOT_DIR
    )
    
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"\n❌ ERROR:")
        print(result.stderr)
        sys.exit(1)

print("\n" + "="*60)
print("✅ ¡TODOS LOS TESTS PASARON!")
print("="*60)