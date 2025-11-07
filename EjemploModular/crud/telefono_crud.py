from models.database import Database
from models.telefono import Telefono

class TelefonoCRUD:
    def __init__(self):
        self.db = Database()
    
    # === CREATE ===
    def crear(self, telefono: Telefono):
        """Crea un nuevo teléfono en la base de datos"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO telefonos (persona_id, telefono) VALUES (%s, %s)",
            (telefono.persona_id, telefono.numero)
        )
        telefono.id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return telefono.id

    # === READ (uno) ===
    def obtener_por_id(self, telefono_id: int):
        """Obtiene un teléfono por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, persona_id, telefono FROM telefonos WHERE id = %s", (telefono_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            tel = Telefono(row["telefono"], row["persona_id"])
            tel.id = row["id"]
            return tel
        return None

    # === READ (todos) ===
    def listar_todos(self):
        """Lista todos los teléfonos registrados"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, persona_id, telefono FROM telefonos")
        telefonos = []
        for row in cursor.fetchall():
            tel = Telefono(row["telefono"], row["persona_id"])
            tel.id = row["id"]
            telefonos.append(tel)
        cursor.close()
        conn.close()
        return telefonos

    # === UPDATE ===
    def actualizar(self, telefono: Telefono):
        """Actualiza el número de un teléfono existente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE telefonos SET telefono = %s WHERE id = %s",
            (telefono.numero, telefono.id)
        )
        conn.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return actualizado

    # === DELETE ===
    def eliminar(self, telefono_id: int):
        """Elimina un teléfono por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM telefonos WHERE id = %s", (telefono_id,))
        conn.commit()
        eliminado = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return eliminado