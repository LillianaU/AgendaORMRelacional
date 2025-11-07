# Importamos la clase Database que maneja la conexión a la base de datos
from models.database import Database
# Importamos el modelo Email que representa la estructura de datos de email
from models.email import Email

class EmailCRUD:
    """
    Clase que maneja las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para la entidad Email en la base de datos.
    """
    
    def __init__(self):
        """
        Constructor: Inicializa una instancia de Database para manejar la conexión
        """
        # Creamos una instancia de Database (patrón Singleton)
        self.db = Database()
    
    def crear(self, email: Email) -> int:
        """
        Crea un nuevo registro de email en la base de datos.
        
        Args:
            email (Email): Objeto Email con los datos a insertar
            
        Returns:
            int: ID del nuevo registro creado
        """
        # Obtiene una conexión activa a la base de datos
        conn = self.db.get_connection()
        
        # Crea un cursor para ejecutar comandos SQL
        cursor = conn.cursor()
        
        # Ejecuta el comando SQL INSERT con los valores del email
        # %s son placeholders que previenen inyección SQL
        cursor.execute(
            "INSERT INTO emails (persona_id, email) VALUES (%s, %s)",
            (email.persona_id, email.direccion)  # Tupla con los valores a insertar
        )
        
        # Obtiene el ID del registro recién creado
        email.id = cursor.lastrowid
        
        # Confirma los cambios en la base de datos
        conn.commit()
        
        # Cierra el cursor para liberar recursos
        cursor.close()
        
        # Retorna el ID del nuevo email creado
        return email.id