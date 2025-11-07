import os
import sys
# Obtener el path absoluto del directorio padre
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import uuid
from models.persona import Persona
from models.telefono import Telefono
from crud.persona_crud import PersonaCRUD
from crud.telefono_crud import TelefonoCRUD

def generar_username(prefix="test_user"):
    """Genera un nombre de usuario único"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def test_crud_telefono_completo():
    """Prueba completa del CRUD de teléfonos"""
    print("\n" + "="*50)
    print("🧪 TEST: CRUD Teléfono Completo")
    print("="*50)
    
    print("\n📝 Paso 1: Preparando usuario de prueba...")
    persona_crud = PersonaCRUD()
    username = generar_username("test_tel_user")
    print(f"-> Creando usuario con username: {username}")
    persona = Persona("Test", "Teléfono", username, "pass123")
    persona_id = persona_crud.crear(persona)
    print(f"✅ Usuario creado con ID: {persona_id}")
    
    print("\n📝 Paso 2: Creando nuevo teléfono...")
    crud = TelefonoCRUD()
    numero = "555-0123"
    print(f"-> Número a crear: {numero}")
    telefono = Telefono(numero, persona_id)
    telefono_id = crud.crear(telefono)
    assert telefono_id > 0, "❌ CREATE: No se creó el teléfono"
    print(f"✅ CREATE: Teléfono creado correctamente (ID: {telefono_id})")
    
    print("\n📝 Paso 3: Leyendo teléfono creado...")
    print(f"-> Buscando teléfono con ID: {telefono_id}")
    tel_leido = crud.obtener_por_id(telefono_id)
    assert tel_leido is not None, "❌ READ: No se encontró el teléfono"
    assert tel_leido.numero == "555-0123", "❌ READ: Número de teléfono incorrecto"
    print(f"✅ READ: Teléfono leído correctamente")
    print(f"-> Datos del teléfono: ID={tel_leido.id}, Número={tel_leido.numero}")
    
    print("\n📝 Paso 4: Actualizando teléfono...")
    nuevo_numero = "555-9876"
    print(f"-> Cambiando número a: {nuevo_numero}")
    tel_leido.numero = nuevo_numero
    actualizado = crud.actualizar(tel_leido)
    assert actualizado, "❌ UPDATE: No se actualizó el teléfono"
    
    print("-> Verificando actualización...")
    tel_actualizado = crud.obtener_por_id(telefono_id)
    assert tel_actualizado.numero == nuevo_numero, "❌ UPDATE: Número no actualizado"
    print(f"✅ UPDATE: Teléfono actualizado correctamente")
    print(f"-> Nuevo número confirmado: {tel_actualizado.numero}")
    
    print("\n📝 Paso 5: Eliminando teléfono...")
    print(f"-> Eliminando teléfono con ID: {telefono_id}")
    eliminado = crud.eliminar(telefono_id)
    assert eliminado, "❌ DELETE: No se eliminó el teléfono"
    
    print("-> Verificando eliminación...")
    tel_eliminado = crud.obtener_por_id(telefono_id)
    assert tel_eliminado is None, "❌ DELETE: El teléfono aún existe"
    print("✅ DELETE: Teléfono eliminado correctamente")
    print("-> Confirmado: El teléfono ya no existe en la base de datos")
    
def actualizar_telefono_interactivo():
    """Permite actualizar un teléfono por ID de forma interactiva"""
    print("\n" + "="*50)
    print("📝 ACTUALIZAR TELÉFONO")
    print("="*50)
    
    crud = TelefonoCRUD()
    
    # Mostrar lista actual
    print("\n📱 Teléfonos disponibles:")
    telefonos = crud.listar_todos()
    if not telefonos:
        print("No hay teléfonos registrados.")
        return
    
    for tel in telefonos:
        print(f"-> ID: {tel.id}, Número: {tel.numero}")
    
    # Solicitar ID a actualizar
    try:
        telefono_id = int(input("\n🔍 Ingrese el ID del teléfono a actualizar (0 para cancelar): "))
        if telefono_id == 0:
            print("Operación cancelada.")
            return
        
        # Verificar que existe
        telefono = crud.obtener_por_id(telefono_id)
        if telefono is None:
            print(f"❌ No se encontró un teléfono con ID: {telefono_id}")
            return
        
        # Solicitar nuevo número
        print(f"\nNúmero actual: {telefono.numero}")
        nuevo_numero = input("Ingrese el nuevo número de teléfono: ").strip()
        if not nuevo_numero:
            print("Operación cancelada: el número no puede estar vacío.")
            return
        
        # Confirmar actualización
        confirmar = input(f"🚨 ¿Está seguro de actualizar el teléfono de {telefono.numero} a {nuevo_numero}? (s/n): ").lower()
        if confirmar != 's':
            print("Operación cancelada.")
            return
        
        # Actualizar
        telefono.numero = nuevo_numero
        if crud.actualizar(telefono):
            print(f"✅ Teléfono actualizado correctamente: ID={telefono_id}")
            print(f"   Anterior: {telefono.numero} -> Nuevo: {nuevo_numero}")
        else:
            print("❌ No se pudo actualizar el teléfono")
            
        # Mostrar lista actualizada
        print("\n📱 Lista actualizada de teléfonos:")
        telefonos = crud.listar_todos()
        for tel in telefonos:
            print(f"-> ID: {tel.id}, Número: {tel.numero}")
            
    except ValueError:
        print("❌ Error: El ID debe ser un número entero")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def eliminar_telefono_interactivo():
    """Permite eliminar un teléfono por ID de forma interactiva"""
    print("\n" + "="*50)
    print("🗑️  ELIMINAR TELÉFONO")
    print("="*50)
    
    crud = TelefonoCRUD()
    
    # Mostrar lista actual
    print("\n📱 Teléfonos disponibles:")
    telefonos = crud.listar_todos()
    if not telefonos:
        print("No hay teléfonos registrados.")
        return
    
    for tel in telefonos:
        print(f"-> ID: {tel.id}, Número: {tel.numero}")
    
    # Solicitar ID a eliminar
    try:
        telefono_id = int(input("\n🔍 Ingrese el ID del teléfono a eliminar (0 para cancelar): "))
        if telefono_id == 0:
            print("Operación cancelada.")
            return
        
        # Verificar que existe
        telefono = crud.obtener_por_id(telefono_id)
        if telefono is None:
            print(f"❌ No se encontró un teléfono con ID: {telefono_id}")
            return
        
        # Confirmar eliminación
        confirmar = input(f"🚨 ¿Está seguro de eliminar el teléfono {telefono.numero}? (s/n): ").lower()
        if confirmar != 's':
            print("Operación cancelada.")
            return
        
        # Eliminar
        if crud.eliminar(telefono_id):
            print(f"✅ Teléfono eliminado correctamente: ID={telefono_id}, Número={telefono.numero}")
        else:
            print("❌ No se pudo eliminar el teléfono")
            
        # Mostrar lista actualizada
        print("\n📱 Lista actualizada de teléfonos:")
        telefonos = crud.listar_todos()
        for tel in telefonos:
            print(f"-> ID: {tel.id}, Número: {tel.numero}")
            
    except ValueError:
        print("❌ Error: El ID debe ser un número entero")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_listar_telefonos():
    """Prueba el listado de teléfonos"""
    print("\n" + "="*50)
    print("🧪 TEST: Listar Teléfonos")
    print("="*50)
    
    print("\n📝 Paso 1: Preparando datos de prueba...")
    persona_crud = PersonaCRUD()
    username = generar_username("test_list_user")
    print(f"-> Creando usuario con username: {username}")
    persona = Persona("Test", "Listado", username, "pass123")
    persona_id = persona_crud.crear(persona)
    print(f"✅ Usuario creado con ID: {persona_id}")
    
    print("\n📝 Paso 2: Creando teléfonos de prueba...")
    crud = TelefonoCRUD()
    
    # Crear varios teléfonos
    numeros = ["111-2222", "333-4444"]
    telefonos_ids = []
    for numero in numeros:
        print(f"-> Creando teléfono: {numero}")
        tel = Telefono(numero, persona_id)
        tel_id = crud.crear(tel)
        telefonos_ids.append(tel_id)
        print(f"✅ Teléfono creado con ID: {tel_id}")
    
    print("\n📝 Paso 3: Listando todos los teléfonos...")
    telefonos = crud.listar_todos()
    assert len(telefonos) >= 2, "❌ No se encontraron los teléfonos creados"
    print(f"✅ Listado: Se encontraron {len(telefonos)} teléfonos")
    
    print("\nTeléfonos encontrados:")
    for tel in telefonos:
        print(f"-> ID: {tel.id}, Número: {tel.numero}")
        
    # Ofrecer eliminar un teléfono
    eliminar = input("\n¿Desea eliminar algún teléfono? (s/n): ").lower()
    if eliminar == 's':
        eliminar_telefono_interactivo()

if __name__ == "__main__":
    while True:
        print("\n" + "="*60)
        print("🔧 MENÚ PRINCIPAL - Gestión de Teléfonos")
        print("="*60)
        print("1. Ejecutar pruebas completas")
        print("2. Ver lista de teléfonos")
        print("3. Actualizar un teléfono")
        print("4. Eliminar un teléfono")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción (1-5): ")
        
        if opcion == "1":
            print("\n" + "="*60)
            print("🧪 TESTS CRUD Teléfono")
            print("="*60)
            test_crud_telefono_completo()
            test_listar_telefonos()
            print("\n" + "="*60)
            print("🎉 Todos los tests de CRUD Teléfono PASARON")
            print("="*60)
        
        elif opcion == "2":
            crud = TelefonoCRUD()
            print("\n📱 Lista de teléfonos registrados:")
            telefonos = crud.listar_todos()
            if not telefonos:
                print("No hay teléfonos registrados.")
            else:
                for tel in telefonos:
                    print(f"-> ID: {tel.id}, Número: {tel.numero}")
            input("\nPresione Enter para continuar...")
        
        elif opcion == "3":
            actualizar_telefono_interactivo()
        
        elif opcion == "4":
            eliminar_telefono_interactivo()
        
        elif opcion == "5":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción no válida. Por favor, seleccione 1, 2 o 3.")
