"""# tests/test_cruds.py
import sys
sys.path.append('..')  # ← Para encontrar models/ y crud/ desde tests/

def test_crud_persona():
    print("✅ CRUD Persona OK")

def test_crud_telefono():
    print("✅ CRUD Teléfono OK")

def test_crud_email():
    print("✅ CRUD Email OK")

def test_login():
    print("✅ Login OK")

if __name__ == "__main__":
    print("🧪 TESTS CRUDs")
    test_crud_persona()
    test_crud_telefono()
    test_crud_email()
    test_login()
    print("🎉 OK")"""
    
# tests/test_cruds.py
import os
import sys
# Obtener el path absoluto del directorio padre
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
import uuid

from models.persona import Persona
from models.telefono import Telefono
from models.email import Email
from crud.persona_crud import PersonaCRUD
from crud.telefono_crud import TelefonoCRUD
from crud.email_crud import EmailCRUD

def generar_username():
    """Genera username único para evitar duplicados"""
    return f"test_{uuid.uuid4().hex[:8]}"

def test_crud_persona():
    """✅ Prueba CREATE y READ de Persona"""
    print("\n=== TEST: CRUD Persona ===")
    
    crud = PersonaCRUD()
    
    # CREATE
    username = generar_username()
    persona = Persona("Test", "User", username, "testpass")
    persona.agregar_telefono("111-222-333")
    persona.agregar_email("test@example.com")
    
    persona_id = crud.crear(persona)
    assert persona_id > 0, "❌ No se creó la persona"
    print(f"✅ CREATE: Persona ID {persona_id}")
    
    # READ
    persona_db = crud.obtener_por_id(persona_id)
    assert persona_db.nombre == "Test"
    assert persona_db.apellido == "User"
    assert persona_db.username == username
    assert len(persona_db.telefonos) == 1
    assert len(persona_db.emails) == 1
    print("✅ READ: Persona recuperada con relaciones")

def test_crud_telefono():
    """✅ Prueba CREATE de Teléfono"""
    print("\n=== TEST: CRUD Teléfono ===")
    
    # 1. Crear persona primero (por foreign key)
    persona_crud = PersonaCRUD()
    persona = Persona("Test", "Teléfono", generar_username(), "pass")
    persona_id = persona_crud.crear(persona)
    
    # 2. Crear teléfono asociado
    crud = TelefonoCRUD()
    tel = Telefono("444-555-666", persona_id)
    tel_id = crud.crear(tel)
    
    assert tel_id > 0, "❌ No se creó el teléfono"
    assert tel.id == tel_id, "❌ ID no asignado"
    print(f"✅ Teléfono creado (ID: {tel_id})")

def test_crud_email():
    """✅ Prueba CREATE de Email"""
    print("\n=== TEST: CRUD Email ===")
    
    # 1. Crear persona primero
    persona_crud = PersonaCRUD()
    persona = Persona("Test", "Email", generar_username(), "pass")
    persona_id = persona_crud.crear(persona)
    
    # 2. Crear email asociado
    crud = EmailCRUD()
    email = Email("crud@example.com", persona_id)
    email_id = crud.crear(email)
    
    assert email_id > 0, "❌ No se creó el email"
    assert email.id == email_id, "❌ ID no asignado"
    print(f"✅ Email creado (ID: {email_id})")

def test_login():
    """✅ Prueba LOGIN con autenticación real"""
    print("\n=== TEST: Login ===")
    
    crud = PersonaCRUD()
    username = generar_username()
    
    # Crear usuario
    persona = Persona("Login", "Test", username, "123456")
    persona_id = crud.crear(persona)
    
    # Intentar login
    persona_login = crud.login(username, "123456")
    assert persona_login is not None, "❌ Login falló"
    assert persona_login._login.is_authenticated == True, "❌ No autenticado"
    assert persona_login.id == persona_id, "❌ ID no coincide"
    print("✅ Login autenticación correcta")

if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTS CRUDs - Interacción Real con BD")
    print("="*60)
    test_crud_persona()
    test_crud_telefono()
    test_crud_email()
    test_login()
    print("\n" + "="*60)
    print("🎉 Todos los tests de CRUD PASARON")
    print("="*60)