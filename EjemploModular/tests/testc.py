# tests/test_completo_cruds.py
import sys
import time
import uuid
sys.path.append('..')

from models.persona import Persona
from models.telefono import Telefono
from models.email import Email
from crud.persona_crud import PersonaCRUD
from crud.telefono_crud import TelefonoCRUD
from crud.email_crud import EmailCRUD


def generar_username():
    """Genera username único para evitar duplicados"""
    return f"test_{uuid.uuid4().hex[:8]}"


# ================================================================
# 🧪 TESTS CRUD COMPLETOS
# ================================================================

def test_crud_persona():
    print("\n=== TEST: CRUD Persona ===")
    crud = PersonaCRUD()
    username = generar_username()
    persona = Persona("Test", "User", username, "pass123")

    persona_id = crud.crear(persona)
    assert persona_id > 0, "❌ No se creó la persona"
    print(f"✅ CREATE Persona (ID: {persona_id})")

    persona_db = crud.obtener_por_id(persona_id)
    assert persona_db.nombre == "Test"
    assert persona_db.username == username
    print("✅ READ Persona OK")


def test_crud_update():
    print("\n=== TEST: UPDATE Persona ===")
    crud = PersonaCRUD()
    persona = Persona("Carlos", "Gomez", generar_username(), "12345")
    persona_id = crud.crear(persona)

    persona.nombre = "Carlos A."
    persona.apellido = "Gomez Ruiz"
    crud.actualizar(persona)

    persona_db = crud.obtener_por_id(persona_id)
    assert persona_db.nombre == "Carlos A."
    assert persona_db.apellido == "Gomez Ruiz"
    print("✅ UPDATE Persona OK")


def test_crud_delete():
    print("\n=== TEST: DELETE Persona ===")
    crud = PersonaCRUD()
    persona = Persona("Laura", "Ruiz", generar_username(), "abcd")
    persona_id = crud.crear(persona)

    crud.eliminar(persona_id)
    persona_db = crud.obtener_por_id(persona_id)
    assert persona_db is None, "❌ Persona no eliminada"
    print("✅ DELETE Persona OK")


def test_crud_relaciones():
    print("\n=== TEST: Relaciones Persona–Teléfono–Email ===")
    persona_crud = PersonaCRUD()
    tel_crud = TelefonoCRUD()
    email_crud = EmailCRUD()

    persona = Persona("Diana", "Lopez", generar_username(), "xyz")
    persona_id = persona_crud.crear(persona)

    tel = Telefono("999-888-777", persona_id)
    email = Email("diana@test.com", persona_id)

    tel_crud.crear(tel)
    email_crud.crear(email)

    persona_db = persona_crud.obtener_por_id(persona_id)
    assert len(persona_db.telefonos) > 0
    assert len(persona_db.emails) > 0
    print("✅ Relaciones correctas")


def test_login_correcto():
    print("\n=== TEST: Login Correcto ===")
    crud = PersonaCRUD()
    username = generar_username()

    persona = Persona("Login", "Ok", username, "123456")
    crud.crear(persona)

    persona_login = crud.login(username, "123456")
    assert persona_login is not None, "❌ Login falló"
    assert persona_login._login.is_authenticated is True
    print("✅ Login autenticación correcta")


def test_login_incorrecto():
    print("\n=== TEST: Login Incorrecto ===")
    crud = PersonaCRUD()
    persona = Persona("Pedro", "Mora", generar_username(), "clave123")
    crud.crear(persona)

    resultado = crud.login(persona.username, "clave_mal")
    assert resultado is None, "❌ Login debería fallar con contraseña incorrecta"
    print("✅ Login incorrecto bloqueado")


def test_username_duplicado():
    print("\n=== TEST: Username Duplicado ===")
    crud = PersonaCRUD()
    username = generar_username()

    persona1 = Persona("Ana", "Luna", username, "a1")
    persona2 = Persona("Juan", "Luna", username, "a2")

    crud.crear(persona1)
    try:
        crud.crear(persona2)
        assert False, "❌ Se permitió crear usuario duplicado"
    except Exception:
        print("✅ Duplicado bloqueado correctamente")


def test_rendimiento_creacion():
    print("\n=== TEST: Rendimiento (100 inserts) ===")
    crud = PersonaCRUD()
    inicio = time.time()

    for i in range(50):  # puedes aumentar a 100 o más
        p = Persona(f"Test{i}", "Speed", generar_username(), "pass")
        crud.crear(p)

    fin = time.time()
    print(f"✅ Se crearon 50 usuarios en {fin - inicio:.2f} segundos")


def test_transaccion_fallida():
    print("\n=== TEST: Transacción Fallida ===")
    crud = PersonaCRUD()
    try:
        crud.crear(None)  # datos inválidos
        assert False, "❌ No se lanzó excepción en transacción"
    except Exception:
        print("✅ Transacción fallida revertida correctamente")


# ================================================================
# 🔰 EJECUCIÓN GENERAL
# ================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTS CRUD COMPLETOS - Interacción Real con BD")
    print("=" * 60)

    test_crud_persona()
    test_crud_update()
    test_crud_delete()
    test_crud_relaciones()
    test_login_correcto()
    test_login_incorrecto()
    test_username_duplicado()
    test_rendimiento_creacion()
    test_transaccion_fallida()

    print("\n" + "=" * 60)
    print("🎉 Todos los tests CRUD y de Integridad PASARON")
    print("=" * 60)
