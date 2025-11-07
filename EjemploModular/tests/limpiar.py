# limpiar_bd.py - Limpia todas las tablas de la base de datos
import os
import sys
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def limpiar_tablas():
    """Ejecuta DELETE en todas las tablas en el orden correcto"""
    
    conn = None
    cursor = None
    
    try:
        # Conectar a MySQL
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        print("=" * 60)
        print("🗑️  LIMPIANDO BASE DE DATOS")
        print("=" * 60)
        
        # Orden correcto: primero hijos, luego padre
        tablas = [
            ("telefonos", "DELETE FROM telefonos"),
            ("emails", "DELETE FROM emails"),
            ("personas", "DELETE FROM personas")
        ]
        
        for nombre_tabla, query in tablas:
            cursor.execute(query)
            filas_afectadas = cursor.rowcount
            print(f"✅ {nombre_tabla}: {filas_afectadas} registros eliminados")
        
        # Confirmar cambios
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ TODAS LAS TABLAS LIMPIADAS EXITOSAMENTE")
        print("=" * 60)
        
    except mysql.connector.Error as e:
        print(f"❌ ERROR DE MYSQL: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)
        
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    # Confirmación de seguridad
    print("⚠️  ESTE SCRIPT ELIMINARÁ TODOS LOS DATOS DE LA BASE DE DATOS")
    confirmacion = input("¿Estás seguro? Escribe 'SI' para continuar: ")
    
    if confirmacion.upper() == "SI":
        limpiar_tablas()
    else:
        print("Operación cancelada.")