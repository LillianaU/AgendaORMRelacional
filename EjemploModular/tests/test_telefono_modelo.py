# tests/test_telefono_modelo.py - PRUEBA SOLO LA CLASE (sin BD)
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

from models.telefono import Telefono

def confirmar(mensaje):
    """Pregunta si desea continuar"""
    while True:
        resp = input(f"\n{mensaje} (s/n): ").lower().strip()
        if resp == 's':
            return True
        elif resp == 'n':
            return False
        print("❌ Ingrese 's' o 'n'")

def test_telefono_modelo():
    """PRUEBA DE LA CLASE TELEFONO (sin BD)"""
    print("="*60)
    print("🧪 PRUEBA DEL MODELO TELEFONO (Sin BD)")
    print("="*60)
    
    # === 1. CREAR OBJETO ===
    print("\n" + "="*50)
    print("PASO 1: CREAR OBJETO TELEFONO")
    print("="*50)
    
    tel = Telefono("555-1234", persona_id=1)
    print(f"✅ Objeto creado: {tel}")
    print(f"  - Número: {tel.numero}")
    print(f"  - Persona ID: {tel.persona_id}")
    print(f"  - ID (None inicial): {tel.id}")
    
    if not confirmar("¿Continuar al PASO 2 (modificar atributos)?"):
        return
    
    # === 2. MODIFICAR ATRIBUTOS ===
    print("\n" + "="*50)
    print("PASO 2: MODIFICAR ATRIBUTOS DEL OBJETO")
    print("="*50)
    
    tel.numero = "555-9999"
    tel.id = 42  # Simular ID asignado por BD
    
    print(f"✅ Atributos modificados:")
    print(f"  - Nuevo número: {tel.numero}")
    print(f"  - Nuevo ID: {tel.id}")
    
    if not confirmar("¿Continuar al PASO 3 (crear múltiples)?"):
        return
    
    # === 3. CREAR MÚLTIPLES OBJETOS ===
    print("\n" + "="*50)
    print("PASO 3: CREAR MÚLTIPLES OBJETOS TELEFONO")
    print("="*50)
    
    lista_telefonos = [
        Telefono("111-2222", persona_id=1),
        Telefono("333-4444", persona_id=2),
        Telefono("555-6666", persona_id=1)
    ]
    
    # Asignar IDs simulados
    for i, tel_obj in enumerate(lista_telefonos):
        tel_obj.id = i + 100
    
    print(f"✅ Lista de {len(lista_telefonos)} teléfonos creada:")
    for tel_obj in lista_telefonos:
        print(f"  - {tel_obj}")
    
    if not confirmar("¿Continuar al PASO 4 (filtrar)?"):
        return
    
    # === 4. FILTRAR POR PERSONA_ID ===
    print("\n" + "="*50)
    print("PASO 4: FILTRAR TELEFONOS POR PERSONA_ID")
    print("="*50)
    
    persona_id_filtro = 1
    telefonos_filtrados = [tel for tel in lista_telefonos if tel.persona_id == persona_id_filtro]
    
    print(f"✅ Teléfonos de persona_id={persona_id_filtro}: {len(telefonos_filtrados)}")
    for tel_obj in telefonos_filtrados:
        print(f"  - {tel_obj}")
    
    if not confirmar("¿Continuar al PASO 5 (validaciones)?"):
        return
    
    # === 5. VALIDACIONES ===
    print("\n" + "="*50)
    print("PASO 5: VALIDAR CONTENIDO DE OBJETOS")
    print("="*50)
    
    # Crear teléfono con datos específicos para validar
    tel_validar = Telefono("777-8888", persona_id=999)
    tel_validar.id = 999
    
    assert tel_validar.numero == "777-8888", "❌ Número incorrecto"
    assert tel_validar.persona_id == 999, "❌ Persona ID incorrecto"
    assert tel_validar.id == 999, "❌ ID incorrecto"
    
    print("✅ Todas las validaciones pasaron:")
    print(f"  - Número: {tel_validar.numero} ✓")
    print(f"  - Persona ID: {tel_validar.persona_id} ✓")
    print(f"  - ID: {tel_validar.id} ✓")
    
    # === RESUMEN FINAL ===
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL PRUEBA MODELO")
    print("="*60)
    print(f"✅ Objetos creados: {len(lista_telefonos) + 2}")
    print(f"✅ Atributos validados: 3/3")
    print(f"✅ Filtraciones exitosas: 1")
    
    print("\n" + "🎉" * 30)
    print("✅ PRUEBA DEL MODELO TELEFONO FINALIZADA")
    print("🎉" * 30)

if __name__ == "__main__":
    test_telefono_modelo()