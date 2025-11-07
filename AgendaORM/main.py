from config.database import db_config, Base
from services.session_service import SessionService
from services.auth_service import AuthService
from services.contact_service import ContactService
from interfaces.console_ui import ConsoleUI

def inicializar_base_datos():
    """Crear tablas si no existen"""
    try:
        Base.metadata.create_all(db_config.get_engine())
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        raise

def main():
    try:
        # Inicializar base de datos
        inicializar_base_datos()
        
        # Configurar servicios
        session_service = SessionService()
        auth_service = AuthService(session_service)
        contact_service = ContactService(session_service)
        
        # Iniciar interfaz de usuario
        console_ui = ConsoleUI(auth_service, contact_service, session_service)
        console_ui.ejecutar()
        
    except Exception as e:
        print(f"❌ Error fatal en la aplicación: {e}")

if __name__ == "__main__":
    main()