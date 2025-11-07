from typing import List, Optional
from models.telefono import Telefono
from models.email import Email
import hashlib

class Usuario:
    """Clase base para demostrar HERENCIA"""
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = self._hash_password(password)
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)


class Persona(Usuario):
    """
    HERENCIA: Hereda de Usuario
    COMPOSICIÓN: Contiene un objeto Login que no existe sin Persona
    AGREGACIÓN: Contiene listas de Teléfono y Email que pueden existir solos
    ASOCIACIÓN: Se asocia con Teléfono y Email a través de persona_id
    """
    def __init__(self, nombre: str, apellido: str, username: str, password: str):
        # Inicializar clase padre
        super().__init__(username, password)
        
        self.id: Optional[int] = None
        self.nombre = nombre
        self.apellido = apellido
        
        # COMPOSICIÓN: Login no puede existir sin Persona
        self._login = self.Login(self.username, self.password_hash)
        
        # AGREGACIÓN: Teléfonos y Emails pueden existir independientemente
        self._telefonos: List[Telefono] = []
        self._emails: List[Email] = []
    
    # Clase interna para COMPOSICIÓN
    class Login:
        def __init__(self, username: str, password_hash: str):
            self._username = username
            self._password_hash = password_hash
            self._is_authenticated = False
        
        def authenticate(self, password: str) -> bool:
            # Delega verificación a Usuario
            from models.persona import Usuario
            temp_user = Usuario(self._username, password)
            self._is_authenticated = temp_user.verificar_password(password)
            return self._is_authenticated
        
        @property
        def is_authenticated(self) -> bool:
            return self._is_authenticated
    
    # Métodos de agregación
    def agregar_telefono(self, telefono: str):
        """ASOCIACIÓN: Agrega un teléfono asociado a esta persona"""
        self._telefonos.append(Telefono(telefono, self.id))
    
    def agregar_email(self, email: str):
        """ASOCIACIÓN: Agrega un email asociado a esta persona"""
        self._emails.append(Email(email, self.id))
    
    # Getters para acceder a las colecciones
    @property
    def telefonos(self) -> List[Telefono]:
        return self._telefonos
    
    @property
    def emails(self) -> List[Email]:
        return self._emails
    
    def __str__(self):
        return f"Persona({self.id}, {self.nombre} {self.apellido}, {self.username})"