from typing import Optional, List
from models.database import Database
from models.persona import Persona
# ↓↓↓ IMPORTACIONES FALTANTES ↓↓↓
from models.telefono import Telefono
from models.email import Email

class PersonaCRUD:
    """ASOCIACIÓN: Esta clase se asocia con Persona y Database"""
    
    def __init__(self):
        self.db = Database()
    
    def crear(self, persona: Persona) -> int:
        """Crea una persona y sus datos relacionados"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insertar persona
            query = """
                INSERT INTO personas (nombre, apellido, username, password_hash)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                persona.nombre,
                persona.apellido,
                persona.username,
                persona.password_hash
            ))
            persona.id = cursor.lastrowid
            
            # Insertar teléfonos (AGREGACIÓN)
            for telefono in persona.telefonos:
                cursor.execute(
                    "INSERT INTO telefonos (persona_id, telefono) VALUES (%s, %s)",
                    (persona.id, telefono.numero)
                )
            
            # Insertar emails (AGREGACIÓN)
            for email in persona.emails:
                cursor.execute(
                    "INSERT INTO emails (persona_id, email) VALUES (%s, %s)",
                    (persona.id, email.direccion)
                )
            
            conn.commit()
            return persona.id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def login(self, username: str, password: str) -> Optional[Persona]:
        """Realiza login usando la composición de Login dentro de Persona"""
        
        # ↓↓↓ CORRECCIÓN: Usar context manager para el cursor ↓↓↓
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Buscar usuario
                cursor.execute(
                    "SELECT * FROM personas WHERE username = %s",
                    (username,)
                )
                row = cursor.fetchone()
                
                if row:
                    # Crear objeto persona
                    persona = Persona(
                        row['nombre'],
                        row['apellido'],
                        row['username'],
                        ""  # Password temporal
                    )
                    persona.id = row['id']
                    persona.password_hash = row['password_hash']
                    
                    # Usar COMPOSICIÓN para autenticar
                    if persona._login.authenticate(password):
                        # Cargar datos relacionados (AGREGACIÓN)
                        self._cargar_telefonos(persona)
                        self._cargar_emails(persona)
                        return persona
                
                return None
    
    def _cargar_telefonos(self, persona: Persona):
        """Carga los teléfonos asociados (ASOCIACIÓN)"""
        # ↓↓↓ CORRECCIÓN: Usar context manager ↓↓↓
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT id, telefono FROM telefonos WHERE persona_id = %s",
                    (persona.id,)
                )
                for row in cursor:
                    telefono = Telefono(row['telefono'], persona.id)
                    telefono.id = row['id']
                    persona._telefonos.append(telefono)
    
    def _cargar_emails(self, persona: Persona):
        """Carga los emails asociados (ASOCIACIÓN)"""
        # ↓↓↓ CORRECCIÓN: Usar context manager ↓↓↓
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT id, email FROM emails WHERE persona_id = %s",
                    (persona.id,)
                )
                for row in cursor:
                    email = Email(row['email'], persona.id)
                    email.id = row['id']
                    persona._emails.append(email)
    
    def obtener_por_id(self, id: int) -> Optional[Persona]:
        """Obtiene una persona completa con sus relaciones"""
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM personas WHERE id = %s", (id,))
                row = cursor.fetchone()
                
                if row:
                    persona = Persona(
                        row['nombre'],
                        row['apellido'],
                        row['username'],
                        ""
                    )
                    persona.id = row['id']
                    persona.password_hash = row['password_hash']
                    
                    self._cargar_telefonos(persona)
                    self._cargar_emails(persona)
                    return persona
                
                return None