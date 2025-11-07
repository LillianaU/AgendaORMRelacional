import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DatabaseConfig:
    def __init__(self):
        # Configuración de la base de datos - MODIFICA ESTOS VALORES
        self.host = "localhost"
        self.database = "agenda_digital"
        self.username = "root"  # Cambia por tu usuario de MySQL
        self.password = ""      # Cambia por tu password de MySQL
        
        self.database_url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}/{self.database}"
        
    def get_engine(self):
        """Retorna el motor de la base de datos"""
        try:
            engine = create_engine(self.database_url, echo=True)
            return engine
        except Exception as e:
            print(f"❌ Error al crear el engine: {e}")
            raise
    
    def get_session(self):
        """Retorna una nueva sesión de base de datos"""
        try:
            Session = sessionmaker(bind=self.get_engine())
            return Session()
        except Exception as e:
            print(f"❌ Error al crear sesión: {e}")
            raise

# Crear instancia global de configuración
db_config = DatabaseConfig()

# Base para los modelos
Base = declarative_base()