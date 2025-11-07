import os
import sys

from config.database import db_config, Base
from services.session_service import SessionService
from services.auth_service import AuthService
from services.contact_service import ContactService
from interfaces.console_ui import ConsoleUI
from models.persona import Persona

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

        # Modo demo: permite mostrar el menú sin autenticación.
        # Habilítalo pasando el argumento --demo o estableciendo la variable de entorno AGENDA_DEMO=1.
        demo_flag = os.environ.get("AGENDA_DEMO") == '1' or '--demo' in sys.argv[1:]
        if demo_flag:
            # Intentar usar el primer usuario existente como usuario actual; si no hay ninguno,
            # crear un objeto Persona temporal (no persistido) para evitar errores de atributo.
            contactos = contact_service.obtener_todos_los_contactos()
            if contactos:
                console_ui.usuario_actual = contactos[0]
                print("🔎 Modo demo: usando el primer usuario encontrado para demostrar la UI.")
            else:
                console_ui.usuario_actual = Persona(nombre='Demo', apellido='Usuario', username='demo', password_hash='')
                print("🔎 Modo demo: no hay usuarios en la BD. Usando usuario temporal de demostración.")

            # Mostrar el menú sin pasar por la autenticación
            console_ui.mostrar_menu_principal()
        else:
            console_ui.ejecutar()
        
    except Exception as e:
        print(f"❌ Error fatal en la aplicación: {e}")

if __name__ == "__main__":
    main()