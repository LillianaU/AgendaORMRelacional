# 📱 Agenda Digital - Sistema de Gestión de Contactos  

_Un sistema completo de gestión de contactos desarrollado en Python con arquitectura monolítica, programación orientada a objetos (POO), base de datos MySQL y una interfaz de consola._  

---

## 🚀 Comenzando  

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.  

Mira **Despliegue 📦** para conocer cómo ejecutar el sistema.  

---

## 📋 Requisitos del Sistema  

- Python 3.8 o superior  
- MySQL Server 8.0 o superior  
- pip (gestor de paquetes de Python)  

---

## 🔧 Instalación  

### 1️⃣ Clonar o Descargar el Proyecto  
```bash
git clone <url-del-repositorio>
cd AgendaORMRelacional
```

### 2️⃣ Crear y Activar el Entorno Virtual  
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias  
```bash
pip install -r requirements.txt
```

**Dependencias principales:**  
- `SQLAlchemy==2.0.23`  
- `mysql-connector-python==8.1.0`  
- `cryptography==41.0.7`  

### 4️⃣ Configurar la Base de Datos  
Crea la base de datos en MySQL:  
```sql
CREATE DATABASE agenda_digital;
```

Edita el archivo `config/database.py` con tus credenciales:  
```python
self.username = "tu_usuario_mysql"
self.password = "tu_password_mysql"
self.database = "agenda_digital"
```

### 5️⃣ Ejecutar la Aplicación  
```bash
python main.py
```

---

## 🎯 Uso del Sistema  

### 🔑 Primer Inicio  
- Si no hay usuarios registrados, el sistema solicitará crear un usuario administrador.  
- Se almacenan las credenciales de manera segura con hash SHA-256.  

### 🧭 Funcionalidades Principales  

#### 👤 Mi Perfil  
- Ver información personal  
- Listar teléfonos y correos asociados  
- Actualizar datos personales  

#### 📝 Crear Nuevo Contacto  
- Registrar nuevos usuarios  
- Validación de `username` único  

#### 📋 Listar Todos los Contactos  
- Muestra nombre, apellidos, teléfonos y emails  

#### ✏️ Actualizar Contacto  
- Modificar datos personales, username o contraseña  

#### 🗑️ Eliminar Contacto  
- Eliminar por ID o nombre  
- Confirmación antes de eliminar  
- No se permite auto-eliminación  

#### 📞 Gestionar Teléfonos  
- Agregar, listar o eliminar números asociados  

#### 📧 Gestionar Emails  
- Agregar, listar o eliminar correos asociados  

---

## 🏗️ Arquitectura del Proyecto  
# 🏗️ Arquitectura del Proyecto: Agenda Digital ORM Relacional

Este proyecto implementa una **arquitectura monolítica modular** en Python con **ORM SQLAlchemy**, siguiendo el enfoque de **arquitectura en capas**.  
Permite la gestión completa de contactos, teléfonos y correos electrónicos en una base de datos relacional (MySQL).

---

## 🧩 Tipo de Arquitectura

### 🧱 **Arquitectura Monolítica Modular**
El sistema está compuesto por un solo ejecutable (`main.py`) que integra todas las funcionalidades: autenticación, lógica de negocio, persistencia y presentación.

**Ventajas:**
- Sencillez en la implementación y despliegue.  
- Menor complejidad de comunicación entre componentes.  
- Ideal para entornos educativos o proyectos medianos.  

---

## ⚙️ **Arquitectura en Capas (Layered Architecture)**

El proyecto se estructura en capas con responsabilidades bien definidas:

| Capa | Carpeta | Responsabilidad |
|------|----------|----------------|
| **Presentación (UI)** | `interfaces/` | Interacción con el usuario (interfaz de consola). |
| **Servicios / Lógica de Negocio** | `services/` | Contiene la lógica de negocio y operaciones CRUD. |
| **Modelo / Datos (ORM)** | `models/` | Define las clases que representan las tablas de la base de datos. |
| **Configuración / Persistencia** | `config/` | Configura la conexión con la base de datos (SQLAlchemy + MySQL). |
| **Utilidades (Helpers)** | `utils/` | Funciones auxiliares como encriptación de contraseñas. |

---

## 🧠 **Paradigma de Desarrollo: Programación Orientada a Objetos (POO)**

Cada tabla y servicio se implementa como **clases** con métodos específicos, lo que promueve:
- **Encapsulación** de lógica.  
- **Reutilización** de código.  
- **Mantenibilidad** y escalabilidad del proyecto.  

---

## 🗂️ **Estructura del Proyecto**

```
AgendaORMRelacional/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── config/
│   ├── __init__.py
│   └── database.py         # Configuración DB
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── persona.py
│   ├── telefono.py
│   └── email.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── contact_service.py
│   └── session_service.py
├── interfaces/
│   ├── __init__.py
│   └── console_ui.py
└── utils/
    ├── __init__.py
    └── security.py
```

**Diagrama de Flujo:**  
```
Consola → ConsoleUI → Services → Models → Database
    ↓          ↓          ↓         ↓        ↓
Interfaz   Presentación  Lógica   Datos  Persistencia
```

---

## 🧩 Base de Datos  

### Tabla `personas`  
```sql
CREATE TABLE personas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(200) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
```

### Tabla `telefonos`  
```sql
CREATE TABLE telefonos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    persona_id INT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
);
```

### Tabla `emails`  
```sql
CREATE TABLE emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    persona_id INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
);
```

---

## 🛡️ Seguridad  

- Hash de contraseñas con SHA-256  
- Validación de entrada  
- Control de sesiones  
- Protección contra auto-eliminación  

---

## 🐛 Troubleshooting  

### ❌ Error de conexión a MySQL  
- Verifica que el servicio esté activo  
- Confirma credenciales  
- Asegura que la base de datos exista  

### ⚠️ Dependencias no encontradas  
```bash
pip install --force-reinstall -r requirements.txt
```

### 🧩 Importaciones  
- Asegura que todos los `__init__.py` existan  
- Limpia caché de Python (`*.pyc`)  

---

## 🧠 Funcionalidades Futuras  

- Búsqueda avanzada de contactos  
- Exportación a CSV/Excel  
- Interfaz web con Flask o Django  
- API REST  
- Backups automáticos  
- Fotos de perfil  

---

## 🖇️ Contribuyendo  

1. Haz un Fork del repositorio  
2. Crea una rama:  
   ```bash
   git checkout -b feature/NuevaFuncionalidad
   ```
3. Haz commit de tus cambios  
4. Haz push a tu rama  
5. Abre un Pull Request  

---

## 🧰 Construido con  

- [Python](https://www.python.org/)  
- [SQLAlchemy](https://www.sqlalchemy.org/)  
- [MySQL](https://www.mysql.com/)  
- [Cryptography](https://pypi.org/project/cryptography/)  

---

## 📄 Licencia  

Este proyecto está bajo una licencia de uso **educativo y demostrativo**.  

---

## ✨ Autores  

**Lilliana Uribe** — _Desarrollo y Arquitectura_  
📧 [Contacto profesional opcional o GitHub]  

---

## 🎁 Agradecimientos  

- 💬 A la comunidad del SENA por su inspiración  
- ☕ A todos los que apoyan proyectos educativos  
- 📢 Difunde este proyecto si te fue útil  

---

⌨️ con ❤️ por **Lilliana Uribe** 😊  
