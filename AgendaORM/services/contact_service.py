from sqlalchemy.orm import Session, joinedload
from models.persona import Persona
from models.telefono import Telefono
from models.email import Email
from utils.security import hash_password
from typing import List

class ContactService:
    def __init__(self, session_service):
        self.session_service = session_service

    def obtener_todos_los_contactos(self) -> List[Persona]:
        """Obtiene todos los contactos con sus teléfonos y emails"""
        session = self.session_service.get_session()
        try:
            contactos = session.query(Persona).options(
                joinedload(Persona.telefonos),
                joinedload(Persona.emails)
            ).all()
            return contactos
        except Exception as e:
            print(f"❌ Error al obtener contactos: {e}")
            return []
        finally:
            session.close()

    def obtener_contacto_por_id(self, contacto_id: int):
        """Obtiene un contacto específico por ID con sus relaciones"""
        session = self.session_service.get_session()
        try:
            contacto = session.query(Persona).options(
                joinedload(Persona.telefonos),
                joinedload(Persona.emails)
            ).get(contacto_id)
            return contacto
        except Exception as e:
            print(f"❌ Error al obtener contacto: {e}")
            return None
        finally:
            session.close()

    def crear_contacto(self, nombre: str, apellido: str, username: str, password: str) -> bool:
        """Crea un nuevo contacto"""
        session = self.session_service.get_session()
        try:
            # Verificar si el username ya existe
            usuario_existente = session.query(Persona).filter_by(username=username).first()
            if usuario_existente:
                return False
            
            # Crear nuevo usuario
            password_hash = hash_password(password)
            nuevo_contacto = Persona(
                nombre=nombre,
                apellido=apellido,
                username=username,
                password_hash=password_hash
            )
            
            session.add(nuevo_contacto)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error al crear contacto: {e}")
            return False
        finally:
            session.close()

    def actualizar_contacto(self, contacto_id: int, nombre: str = None, apellido: str = None, 
                          username: str = None, password: str = None) -> bool:
        """Actualiza un contacto existente"""
        session = self.session_service.get_session()
        try:
            contacto = session.query(Persona).get(contacto_id)
            if not contacto:
                return False
            
            if nombre is not None:
                contacto.nombre = nombre
            if apellido is not None:
                contacto.apellido = apellido
            if username is not None:
                # Verificar que el nuevo username no esté en uso
                if username != contacto.username:
                    existe = session.query(Persona).filter_by(username=username).first()
                    if existe:
                        return False
                contacto.username = username
            if password is not None:
                contacto.password_hash = hash_password(password)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error al actualizar contacto: {e}")
            return False
        finally:
            session.close()

    def eliminar_contacto_por_id(self, contacto_id: int) -> bool:
        """Elimina un contacto por su ID"""
        session = self.session_service.get_session()
        try:
            contacto = session.query(Persona).get(contacto_id)
            if contacto:
                session.delete(contacto)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Error al eliminar contacto: {e}")
            return False
        finally:
            session.close()

    def buscar_contacto_por_nombre(self, nombre: str) -> List[Persona]:
        """Busca contactos por nombre"""
        session = self.session_service.get_session()
        try:
            contactos = session.query(Persona).options(
                joinedload(Persona.telefonos),
                joinedload(Persona.emails)
            ).filter(
                Persona.nombre.ilike(f"%{nombre}%")
            ).all()
            return contactos
        except Exception as e:
            print(f"❌ Error al buscar contactos: {e}")
            return []
        finally:
            session.close()

    def agregar_telefono(self, persona_id: int, telefono: str) -> bool:
        """Agrega un teléfono a un contacto"""
        session = self.session_service.get_session()
        try:
            nuevo_telefono = Telefono(
                persona_id=persona_id,
                telefono=telefono
            )
            session.add(nuevo_telefono)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"❌ Error al agregar teléfono: {e}")
            return False
        finally:
            session.close()

    def eliminar_telefono(self, telefono_id: int) -> bool:
        """Elimina un teléfono"""
        session = self.session_service.get_session()
        try:
            telefono = session.query(Telefono).get(telefono_id)
            if telefono:
                session.delete(telefono)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Error al eliminar teléfono: {e}")
            return False
        finally:
            session.close()

    def agregar_email(self, persona_id: int, email: str) -> bool:
        """Agrega un email a un contacto"""
        session = self.session_service.get_session()
        try:
            nuevo_email = Email(
                persona_id=persona_id,
                email=email
            )
            session.add(nuevo_email)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"❌ Error al agregar email: {e}")
            return False
        finally:
            session.close()

    def eliminar_email(self, email_id: int) -> bool:
        """Elimina un email"""
        session = self.session_service.get_session()
        try:
            email = session.query(Email).get(email_id)
            if email:
                session.delete(email)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Error al eliminar email: {e}")
            return False
        finally:
            session.close()