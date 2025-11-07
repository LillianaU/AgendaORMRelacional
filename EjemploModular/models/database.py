import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class Database:
    """Clase Singleton para gestionar la conexión a MySQL"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance
    
    def get_connection(self):
        """Composición: esta clase se compone de una conexión que no puede existir sin ella"""
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME'),
                    charset='utf8mb4'
                )
                print("✅ Conexión a MySQL establecida")
            except Error as e:
                print(f"❌ Error de conexión: {e}")
                raise
        return self._connection
    
    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("🔌 Conexión cerrada")