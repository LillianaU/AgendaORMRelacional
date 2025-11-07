"""tests/test_modelos.py

Suite de pruebas para los modelos (Persona, Telefono, Email).
Usa import con ruta absoluta relativa al proyecto (sube un nivel desde tests/).
"""
import sys
import os

# PATH ABSOLUTO: Subir un nivel desde tests/
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

from models.telefono import Telefono
from models.email import Email
from models.persona import Persona


def test_modelo_telefono():
    """TEST: Modelo Telefono"""
    tel = Telefono("123-456-789", 1)
    assert tel.numero == "123-456-789"
    assert tel.persona_id == 1
    assert tel.id is None


def test_modelo_email():
    """TEST: Modelo Email"""
    email = Email("test@example.com", 2)
    assert email.direccion == "test@example.com"
    assert email.persona_id == 2
    assert email.id is None


def test_persona_herencia():
    """TEST: Herencia"""
    persona = Persona("Juan", "Perez", "juanp", "password123")
    assert hasattr(persona, 'verificar_password')
    assert persona.verificar_password("password123") is True
    assert persona.verificar_password("wrong") is False


def test_persona_composicion():
    """TEST: Composicion Login"""
    persona = Persona("Ana", "Garcia", "anag", "secret")
    assert hasattr(persona, '_login')
    assert persona._login is not None
    resultado = persona._login.authenticate("secret")
    assert resultado is True
    assert persona._login.is_authenticated is True


def test_persona_agregacion():
    """TEST: Agregacion"""
    persona = Persona("Luis", "Lopez", "luisl", "pass")
    persona.id = 999
    persona.agregar_telefono("555-1111")
    persona.agregar_telefono("555-2222")
    persona.agregar_email("luis@example.com")
    assert len(persona.telefonos) == 2
    assert len(persona.emails) == 1
    assert persona.telefonos[0].numero == "555-1111"


def test_persona_asociaciones():
    """TEST: Asociaciones"""
    persona = Persona("Maria", "Martinez", "mariam", "pass")
    persona.id = 888
    persona.agregar_telefono("666-7777")
    persona.agregar_email("maria@example.com")
    assert persona.telefonos[0].persona_id == 888
    assert persona.emails[0].persona_id == 888


if __name__ == "__main__":
    # Permitir ejecución directa para desarrollo rápido
    print("Ejecutando tests de modelos en modo standalone")
    import pytest
    raise SystemExit(pytest.main([__file__]))