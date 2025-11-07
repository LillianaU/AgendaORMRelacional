from services.auth_service import AuthService
from services.contact_service import ContactService
from services.session_service import SessionService
from models.persona import Persona
from models.telefono import Telefono
from models.email import Email

class ConsoleUI:
    def __init__(self, auth_service, contact_service, session_service):
        self.auth_service = auth_service
        self.contact_service = contact_service
        self.session_service = session_service
        self.usuario_actual = None

    def ejecutar(self):
        """Método principal que inicia la aplicación"""
        # Mostrar el encabezado y ofrecer un menú de autenticación explícito
        print("=== AGENDA DIGITAL ===")

        while True:
            print("\n" + "="*40)
            print("      BIENVENIDO A AGENDA DIGITAL")
            print("="*40)
            print("1. 😎 Ingresar")
            print("2. 👉 Registrarse")
            print("3. 👣Salir")

            opcion = input("\nSeleccione una opción (1-3): ").strip()

            if opcion == '1':
                # Intentar inicio de sesión
                if self.iniciar_sesion():
                    # Mostrar el menú principal sólo si el inicio fue exitoso
                    self.mostrar_menu_principal()
                    break
                else:
                    # Volver al menú de autenticación
                    continue
            elif opcion == '2':
                # Registrar un nuevo contacto y luego volver al menú de autenticación
                self.crear_nuevo_contacto()
                input("\nPresione Enter para volver al menú de inicio...")
                continue
            elif opcion == '3':
                print("\n👋 Saliendo...")
                break
            else:
                print("❌ Opción no válida. Por favor seleccione 1-3.")

    def autenticar_usuario(self):
        """Maneja el proceso de autenticación"""
        if not self.auth_service.hay_usuarios_registrados():
            print("No hay usuarios registrados. Creando usuario administrador...")
            self.registrar_primer_usuario()
        else:
            self.iniciar_sesion()

    def registrar_primer_usuario(self):
        """Registra el primer usuario administrador"""
        print("\n--- REGISTRO DE USUARIO ADMINISTRADOR ---")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if self.auth_service.registrar_usuario(nombre, apellido, username, password):
            print("✅ Usuario registrado exitosamente")
            self.usuario_actual = self.auth_service.iniciar_sesion(username, password)
        else:
            print("❌ Error al registrar usuario")

    def iniciar_sesion(self):
        """Maneja el inicio de sesión"""
        intentos = 0
        while intentos < 3:
            print(f"\n--- INICIO DE SESIÓN (Intento {intentos + 1}/3) ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            self.usuario_actual = self.auth_service.iniciar_sesion(username, password)
            
            if self.usuario_actual:
                print(f"✅ Bienvenido, {self.usuario_actual.nombre}!")
                return True
            else:
                print("❌ Credenciales incorrectas")
                intentos += 1
        
        print("❌ Demasiados intentos fallidos. Saliendo...")
        return False

    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación"""
        while True:
            # Mostrar el menú exactamente como fue solicitado
            print("\n=== AGENDA DIGITAL ===")
            print("1. 👤  Mi Perfil")
            print("2. 📝  Crear Nuevo Contacto")
            print("3. 📋  Listar Todos los Contactos")
            print("4. ✏️   Actualizar Contacto")
            print("5. 🗑️   Eliminar Contacto")
            print("6. 📞  Gestionar Teléfonos")
            print("7. 📧  Gestionar Emails")
            print("8. 🔒  Cerrar Sesión")
            print("9. 🚪  Salir")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == '1':
                self.mostrar_perfil()
            elif opcion == '2':
                self.crear_nuevo_contacto()
            elif opcion == '3':
                self.listar_todos_los_contactos()
            elif opcion == '4':
                self.actualizar_contacto()
            elif opcion == '5':
                self.eliminar_contacto()
            elif opcion == '6':
                self.gestionar_telefonos()
            elif opcion == '7':
                self.gestionar_emails()
            elif opcion == '8':
                self.cerrar_sesion()
                break
            elif opcion == '9':
                print("¡Hasta pronto! 👋")
                exit()
            else:
                print("❌ Opción no válida. Por favor, seleccione 1-9.")

    def mostrar_perfil(self):
        """Muestra el perfil del usuario actual"""
        if self.usuario_actual:
            # Recargar el usuario actual con todas sus relaciones
            usuario_actualizado = self.contact_service.obtener_contacto_por_id(self.usuario_actual.id)
            
            print(f"\n" + "="*30)
            print("         MI PERFIL")
            print("="*30)
            print(f"🆔 ID: {usuario_actualizado.id}")
            print(f"👤 Nombre: {usuario_actualizado.nombre}")
            print(f"👤 Apellido: {usuario_actualizado.apellido}")
            print(f"👤 Username: {usuario_actualizado.username}")
            
            # Mostrar teléfonos
            if usuario_actualizado.telefonos:
                print("\n📞 Teléfonos:")
                for i, telefono in enumerate(usuario_actualizado.telefonos, 1):
                    print(f"   {i}. {telefono.telefono}")
            else:
                print("\n📞 Teléfonos: No registrados")
            
            # Mostrar emails
            if usuario_actualizado.emails:
                print("\n📧 Emails:")
                for i, email in enumerate(usuario_actualizado.emails, 1):
                    print(f"   {i}. {email.email}")
            else:
                print("\n📧 Emails: No registrados")
                
        else:
            print("❌ No hay usuario autenticado.")

    def crear_nuevo_contacto(self):
        """Crea un nuevo contacto (usuario) en el sistema"""
        print("\n" + "="*30)
        print("     CREAR NUEVO CONTACTO")
        print("="*30)
        
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if not nombre or not apellido or not username or not password:
            print("❌ Todos los campos son obligatorios.")
            return
        
        if self.contact_service.crear_contacto(nombre, apellido, username, password):
            print("✅ Contacto creado exitosamente.")
            # Intentar iniciar sesión automáticamente con las credenciales recién creadas
            usuario = self.auth_service.iniciar_sesion(username, password)
            if usuario:
                self.usuario_actual = usuario
                print("✅ Sesión iniciada automáticamente. Redirigiendo al menú principal...")
                self.mostrar_menu_principal()
            else:
                print("ℹ️ No se pudo iniciar sesión automáticamente. Por favor, elija 'Ingresar' en el menú y use sus credenciales.")
        else:
            print("❌ Error al crear el contacto. El username puede estar en uso.")

    def listar_todos_los_contactos(self):
        """Lista todos los contactos con sus teléfonos y emails"""
        print("\n" + "="*50)
        print("           LISTA DE CONTACTOS")
        print("="*50)
        
        contactos = self.contact_service.obtener_todos_los_contactos()
        
        if not contactos:
            print("📭 No hay contactos en la agenda.")
            return
        
        for contacto in contactos:
            print(f"\n--- CONTACTO ID: {contacto.id} ---")
            print(f"👤 Nombre: {contacto.nombre} {contacto.apellido}")
            print(f"👤 Username: {contacto.username}")
            
            # Mostrar teléfonos
            if contacto.telefonos:
                print("📞 Teléfonos:")
                for telefono in contacto.telefonos:
                    print(f"   - {telefono.telefono}")
            else:
                print("📞 Teléfonos: No registrados")
            
            # Mostrar emails
            if contacto.emails:
                print("📧 Emails:")
                for email in contacto.emails:
                    print(f"   - {email.email}")
            else:
                print("📧 Emails: No registrados")
            
            print("-" * 40)

    def actualizar_contacto(self):
        """Actualiza la información de un contacto"""
        print("\n" + "="*30)
        print("     ACTUALIZAR CONTACTO")
        print("="*30)
        
        contacto_id = input("Ingrese el ID del contacto a actualizar: ").strip()
        
        if not contacto_id.isdigit():
            print("❌ Error: El ID debe ser un número.")
            return
        
        contacto = self.contact_service.obtener_contacto_por_id(int(contacto_id))
        
        if not contacto:
            print(f"❌ No se encontró ningún contacto con ID {contacto_id}")
            return
        
        print(f"\n📋 Contacto encontrado:")
        print(f"🆔 ID: {contacto.id}")
        print(f"👤 Nombre actual: {contacto.nombre}")
        print(f"👤 Apellido actual: {contacto.apellido}")
        print(f"👤 Username actual: {contacto.username}")
        
        print("\nIngrese los nuevos valores (deje en blanco para no cambiar):")
        
        nuevo_nombre = input("Nuevo nombre: ").strip()
        nuevo_apellido = input("Nuevo apellido: ").strip()
        nuevo_username = input("Nuevo username: ").strip()
        nueva_password = input("Nueva password: ").strip()
        
        # Si todos los campos están vacíos
        if not nuevo_nombre and not nuevo_apellido and not nuevo_username and not nueva_password:
            print("ℹ️  No se realizaron cambios.")
            return
        
        if self.contact_service.actualizar_contacto(
            contacto.id, 
            nuevo_nombre if nuevo_nombre else None,
            nuevo_apellido if nuevo_apellido else None,
            nuevo_username if nuevo_username else None,
            nueva_password if nueva_password else None
        ):
            print("✅ Contacto actualizado exitosamente.")
        else:
            print("❌ Error al actualizar el contacto.")

    def eliminar_contacto(self):
        """Menú para eliminar contactos"""
        print("\n" + "="*30)
        print("      ELIMINAR CONTACTO")
        print("="*30)
        print("1. 🆔 Eliminar por ID")
        print("2. 🔤 Eliminar por nombre")
        print("3. ↩️  Volver al menú principal")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            self.eliminar_por_id()
        elif opcion == '2':
            self.eliminar_por_nombre()
        elif opcion == '3':
            return
        else:
            print("❌ Opción no válida.")

    def eliminar_por_id(self):
        """Elimina un contacto por ID"""
        try:
            contacto_id = input("Ingrese el ID del contacto a eliminar: ").strip()
            
            if not contacto_id.isdigit():
                print("❌ Error: El ID debe ser un número.")
                return
            
            contacto_id = int(contacto_id)
            
            # No permitir eliminar el usuario actual
            if contacto_id == self.usuario_actual.id:
                print("❌ No puedes eliminar tu propio usuario.")
                return
            
            contacto = self.contact_service.obtener_contacto_por_id(contacto_id)
            
            if not contacto:
                print(f"❌ No se encontró ningún contacto con ID {contacto_id}")
                return
            
            print(f"\n📋 Contacto encontrado:")
            print(f"🆔 ID: {contacto.id}")
            print(f"👤 Nombre: {contacto.nombre} {contacto.apellido}")
            print(f"👤 Username: {contacto.username}")
            
            confirmar = input("\n⚠️  ¿Está seguro de que desea eliminar este contacto? (s/n): ").strip().lower()
            
            if confirmar == 's':
                if self.contact_service.eliminar_contacto_por_id(contacto_id):
                    print("✅ Contacto eliminado exitosamente.")
                else:
                    print("❌ Error al eliminar el contacto.")
            else:
                print("✅ Operación cancelada.")
                
        except ValueError:
            print("❌ Error: El ID debe ser un número válido.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    def eliminar_por_nombre(self):
        """Elimina contactos por nombre"""
        nombre = input("Ingrese el nombre (o parte del nombre) del contacto a eliminar: ").strip()
        
        if not nombre:
            print("❌ Error: Debe ingresar un nombre.")
            return
        
        contactos = self.contact_service.buscar_contacto_por_nombre(nombre)
        
        if not contactos:
            print(f"🔍 No se encontraron contactos con nombre que contenga '{nombre}'")
            return
        
        # Filtrar para no incluir el usuario actual
        contactos = [c for c in contactos if c.id != self.usuario_actual.id]
        
        if not contactos:
            print("ℹ️  No se pueden eliminar otros contactos con el mismo nombre que el usuario actual.")
            return
        
        print(f"\n🔍 Se encontraron {len(contactos)} contacto(s) que coinciden:")
        for contacto in contactos:
            print(f"🆔 ID: {contacto.id} - 👤 Nombre: {contacto.nombre} {contacto.apellido}")
        
        print("\n🗑️  Opciones:")
        print("1. Eliminar TODOS los contactos listados")
        print("2. Eliminar por ID específico")
        print("3. Cancelar")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            confirmar = input("⚠️  ¿Está seguro de eliminar TODOS estos contactos? (s/n): ").strip().lower()
            if confirmar == 's':
                eliminados = 0
                for contacto in contactos:
                    if self.contact_service.eliminar_contacto_por_id(contacto.id):
                        eliminados += 1
                print(f"✅ Se eliminaron {eliminados} contacto(s).")
            else:
                print("✅ Operación cancelada.")
                
        elif opcion == '2':
            self.eliminar_por_id()
        elif opcion == '3':
            print("✅ Operación cancelada.")
        else:
            print("❌ Opción no válida.")

    def gestionar_telefonos(self):
        """Gestiona los teléfonos del usuario actual"""
        print("\n" + "="*30)
        print("     GESTIONAR TELÉFONOS")
        print("="*30)
        print("1. 📞 Agregar teléfono")
        print("2. 📋 Ver mis teléfonos")
        print("3. 🗑️  Eliminar teléfono")
        print("4. ↩️  Volver")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            self.agregar_telefono()
        elif opcion == '2':
            self.mostrar_telefonos()
        elif opcion == '3':
            self.eliminar_telefono()
        elif opcion == '4':
            return
        else:
            print("❌ Opción no válida.")

    def agregar_telefono(self):
        """Agrega un teléfono al usuario actual"""
        if not self.usuario_actual:
            print("❌ No hay usuario autenticado.")
            return
            
        telefono = input("Ingrese el número de teléfono: ").strip()
        if telefono:
            if self.contact_service.agregar_telefono(self.usuario_actual.id, telefono):
                print("✅ Teléfono agregado exitosamente.")
            else:
                print("❌ Error al agregar el teléfono.")
        else:
            print("❌ El teléfono no puede estar vacío.")

    def mostrar_telefonos(self):
        """Muestra los teléfonos del usuario actual"""
        usuario = self.contact_service.obtener_contacto_por_id(self.usuario_actual.id)
        if usuario and usuario.telefonos:
            print("\n📞 Mis teléfonos:")
            for i, telefono in enumerate(usuario.telefonos, 1):
                print(f"   {i}. {telefono.telefono} (ID: {telefono.id})")
        else:
            print("📞 No tienes teléfonos registrados.")

    def eliminar_telefono(self):
        """Elimina un teléfono del usuario actual"""
        usuario = self.contact_service.obtener_contacto_por_id(self.usuario_actual.id)
        if not usuario or not usuario.telefonos:
            print("📞 No tienes teléfonos para eliminar.")
            return
            
        self.mostrar_telefonos()
        
        try:
            telefono_id = input("\nIngrese el ID del teléfono a eliminar: ").strip()
            if not telefono_id.isdigit():
                print("❌ El ID debe ser un número.")
                return
                
            if self.contact_service.eliminar_telefono(int(telefono_id)):
                print("✅ Teléfono eliminado exitosamente.")
            else:
                print("❌ Error al eliminar el teléfono.")
        except ValueError:
            print("❌ ID inválido.")

    def gestionar_emails(self):
        """Gestiona los emails del usuario actual"""
        print("\n" + "="*30)
        print("      GESTIONAR EMAILS")
        print("="*30)
        print("1. 📧 Agregar email")
        print("2. 📋 Ver mis emails")
        print("3. 🗑️  Eliminar email")
        print("4. ↩️  Volver")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            self.agregar_email()
        elif opcion == '2':
            self.mostrar_emails()
        elif opcion == '3':
            self.eliminar_email()
        elif opcion == '4':
            return
        else:
            print("❌ Opción no válida.")

    def agregar_email(self):
        """Agrega un email al usuario actual"""
        if not self.usuario_actual:
            print("❌ No hay usuario autenticado.")
            return
            
        email = input("Ingrese el email: ").strip()
        if email:
            if self.contact_service.agregar_email(self.usuario_actual.id, email):
                print("✅ Email agregado exitosamente.")
            else:
                print("❌ Error al agregar el email.")
        else:
            print("❌ El email no puede estar vacío.")

    def mostrar_emails(self):
        """Muestra los emails del usuario actual"""
        usuario = self.contact_service.obtener_contacto_por_id(self.usuario_actual.id)
        if usuario and usuario.emails:
            print("\n📧 Mis emails:")
            for i, email in enumerate(usuario.emails, 1):
                print(f"   {i}. {email.email} (ID: {email.id})")
        else:
            print("📧 No tienes emails registrados.")

    def eliminar_email(self):
        """Elimina un email del usuario actual"""
        usuario = self.contact_service.obtener_contacto_por_id(self.usuario_actual.id)
        if not usuario or not usuario.emails:
            print("📧 No tienes emails para eliminar.")
            return
            
        self.mostrar_emails()
        
        try:
            email_id = input("\nIngrese el ID del email a eliminar: ").strip()
            if not email_id.isdigit():
                print("❌ El ID debe ser un número.")
                return
                
            if self.contact_service.eliminar_email(int(email_id)):
                print("✅ Email eliminado exitosamente.")
            else:
                print("❌ Error al eliminar el email.")
        except ValueError:
            print("❌ ID inválido.")

    def cerrar_sesion(self):
        """Cierra la sesión del usuario"""
        self.usuario_actual = None
        print("✅ Sesión cerrada correctamente")