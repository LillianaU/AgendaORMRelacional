from models.persona import Persona
from utils.security import hash_password, verify_password
from sqlalchemy.orm import joinedload

class AuthService:
    def __init__(self, session_service):
        self.session_service = session_service

    def hay_usuarios_registrados(self) -> bool:
        """Verifica si hay usuarios registrados en el sistema"""
        session = self.session_service.get_session()
        try:
            count = session.query(Persona).count()
            return count > 0
        except Exception as e:
            print(f"❌ Error al verificar usuarios: {e}")
            return False
        finally:
            session.close()

    def registrar_usuario(self, nombre: str, apellido: str, username: str, password: str) -> bool:
        """Registra un nuevo usuario"""
        session = self.session_service.get_session()
        try:
            # Verificar si el username ya existe
            usuario_existente = session.query(Persona).filter_by(username=username).first()
            if usuario_existente:
                print("❌ El username ya está en uso")
                return False
            
            # Crear nuevo usuario
            password_hash = hash_password(password)
            nuevo_usuario = Persona(
                nombre=nombre,
                apellido=apellido,
                username=username,
                password_hash=password_hash
            )
            
            session.add(nuevo_usuario)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error al registrar usuario: {e}")
            return False
        finally:
            session.close()

    def iniciar_sesion(self, username: str, password: str):
        """Autentica un usuario y carga sus relaciones"""
        session = self.session_service.get_session()
        try:
            # Cargar usuario con sus relaciones usando joinedload
            usuario = session.query(Persona).options(
                joinedload(Persona.telefonos),
                joinedload(Persona.emails)
            ).filter_by(username=username).first()
            
            if usuario and verify_password(password, usuario.password_hash):
                return usuario
            return None
        except Exception as e:
            print(f"❌ Error al iniciar sesión: {e}")
            return None
        finally:
            session.close()