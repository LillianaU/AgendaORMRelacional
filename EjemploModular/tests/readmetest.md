# Guía de Pruebas - Agenda Digital 🧪

## ¿Por qué son importantes las pruebas?

Las pruebas son fundamentales en este proyecto porque:
- 🔍 Garantizan que la gestión de contactos funcione correctamente
- 🛡️ Previenen errores en las operaciones CRUD
- 🔒 Aseguran la integridad de los datos
- 🔧 Facilitan el mantenimiento del código
- ⚠️ Permiten detectar problemas antes de que lleguen a producción

## Métodos de Ejecución de Pruebas

### 1. pytest (Recomendado) 🌟

```bash
# Instalar pytest
pip install pytest

# Ejecutar todas las pruebas con reporte detallado
pytest tests/ -v
```

#### ¿Qué hace `pytest tests/`?
- 🔍 Busca automáticamente archivos test_*.py o *_test.py
- ⚙️ Ejecuta todas las funciones test_*
- 📊 Muestra resumen detallado de resultados
- ⏱️ Reporta tiempo de ejecución
- ❌ Señala exactamente dónde fallan las pruebas

### 2. Runner Personalizado 🛠️

```bash
# Ejecutar todas las pruebas
python test_runner.py

# Ejecutar pruebas específicas
python tests/test_modelos.py    # Solo pruebas de modelos
python tests/test_cruds.py      # Solo pruebas CRUD
```

## Estructura de las Pruebas 📋

### 1. Pruebas de Modelos
- ✅ Validación de campos obligatorios
- 📧 Formato de emails
- 📱 Formato de teléfonos
- 🔗 Relaciones entre modelos

### 2. Pruebas CRUD
- ➕ Create: Creación de registros
- 📖 Read: Lectura de datos
- 📝 Update: Actualización de registros
- ❌ Delete: Eliminación segura

### 3. Pruebas de Integridad
- 🤝 Consistencia en relaciones
- 🎯 Casos límite
- 🔄 Validación de datos únicos
- ⚡ Manejo de errores

## Configuración del Entorno

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Conceptos POO Implementados 🎓

- **HERENCIA**: `Persona` hereda de `Usuario`
- **COMPOSICIÓN**: `Persona` contiene `Login`
- **AGREGACIÓN**: `Persona` tiene múltiples `Teléfono`/`Email`
- **ASOCIACIÓN**: Relaciones entre tablas (`persona_id`)
- **SINGLETON**: `Database` mantiene conexión única

## Buenas Prácticas ⭐

1. 🔄 Ejecutar pruebas antes de cada commit
2. 📈 Mantener pruebas actualizadas
3. 📊 Revisar cobertura de código
4. 📝 Documentar nuevos casos
5. 🔍 Mantener pruebas independientes
6. 🐛 Verificar fallos antes de corregir

## Interpretación de Resultados 📊

- ✅ Verde: Prueba exitosa
- ❌ Rojo: Prueba fallida
- ⚠️ Amarillo: Prueba con advertencias
- 📈 Resumen de cobertura al final