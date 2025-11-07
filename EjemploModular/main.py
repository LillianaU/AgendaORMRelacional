

from models.persona import Persona
from models.telefono import Telefono
from models.email import Email
from crud.persona_crud import PersonaCRUD
from crud.telefono_crud import TelefonoCRUD
from crud.email_crud import EmailCRUD

def mostrar_menu_principal():
    print("\n" + "="*50)
    print("📋 MENÚ PRINCIPAL")
    print("="*50)
    print("1. Registrar nueva persona")
    print("2. Iniciar sesión")
    print("3. Salir")
    return input("Seleccione opción: ")

def mostrar_menu_usuario(persona: Persona):
    print("\n" + "="*50)
    print(f"👤 Bienvenido: {persona.nombre} {persona.apellido}")
    print("="*50)
    print("1. Ver mi información")
    print("2. Agregar teléfono")
    print("3. Agregar email")
    print("4. Cerrar sesión")
    return input("Seleccione opción: ")

def registrar_persona(crud: PersonaCRUD):
    print("\n--- REGISTRO DE NUEVA PERSONA ---")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    username = input("Username: ")
    password = input("Password: ")
    
    persona = Persona(nombre, apellido, username, password)
    
    # Agregar teléfonos (AGREGACIÓN)
    while True:
        tel = input("Teléfono (dejar vacío para terminar): ")
        if not tel:
            break
        persona.agregar_telefono(tel)
    
    # Agregar emails (AGREGACIÓN)
    while True:
        email = input("Email (dejar vacío para terminar): ")
        if not email:
            break
        persona.agregar_email(email)
    
    try:
        persona_id = crud.crear(persona)
        print(f"✅ Persona registrada con ID: {persona_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    crud = PersonaCRUD()
    usuario_actual = None
    
    while True:
        if usuario_actual is None:
            opcion = mostrar_menu_principal()
            
            if opcion == "1":
                registrar_persona(crud)
            
            elif opcion == "2":
                print("\n--- LOGIN ---")
                username = input("Username: ")
                password = input("Password: ")
                
                # Usa COMPOSICIÓN para autenticar
                persona = crud.login(username, password)
                
                if persona:
                    print("✅ Login exitoso!")
                    usuario_actual = persona
                else:
                    print("❌ Credenciales inválidas")
            
            elif opcion == "3":
                print("👋 Hasta luego!")
                break
        
        else:
            # Menú de usuario autenticado
            opcion = mostrar_menu_usuario(usuario_actual)
            
            if opcion == "1":
                print(f"\n📄 Información:")
                print(persona)
                print("Teléfonos:", [t.numero for t in usuario_actual.telefonos])
                print("Emails:", [e.direccion for e in usuario_actual.emails])
            
            elif opcion == "2":
                telefono = input("Nuevo teléfono: ")
                telefono_crud = TelefonoCRUD()
                tel_obj = Telefono(telefono, usuario_actual.id)
                telefono_crud.crear(tel_obj)
                usuario_actual.agregar_telefono(telefono)
                print("✅ Teléfono agregado")
            
            elif opcion == "3":
                email_crud = EmailCRUD()
                email = input("Nuevo email: ")
                email_obj = Email(email, usuario_actual.id)
                email_crud.crear(email_obj)
                usuario_actual.agregar_email(email)
                print("✅ Email agregado")
            
            elif opcion == "4":
                usuario_actual = None
                print("🔒 Sesión cerrada")

if __name__ == "__main__":
    # Verificar conexión
    from models.database import Database
    try:
        db = Database()
        db.get_connection()
        main()
    finally:
        db.close_connection()