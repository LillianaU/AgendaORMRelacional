# Guía de Ejecución de Pruebas

Esta guía explica cómo ejecutar las pruebas del proyecto AgendaORMRelacional correctamente.

## Requisitos Previos

1. Asegúrate de tener Python instalado (versión 3.6 o superior)
2. Instala las dependencias del proyecto:
   ```cmd
   pip install pytest
   ```

## Estructura de las Pruebas

El proyecto contiene varios archivos de prueba:
- `test_cruds.py`: Pruebas de operaciones CRUD (Create, Read, Update, Delete)
- `test_modelos.py`: Pruebas de los modelos de datos
- `test_completo_cruds.py`: Suite completa de pruebas CRUD

## Cómo Ejecutar las Pruebas

### 1. Desde el Directorio Principal

Para ejecutar las pruebas, debes estar en el directorio `EjemploModular`. Puedes usar estos comandos:

```cmd
cd c:\Users\LILLYU\Documents\GitHub\AgendaORMRelacional\EjemploModular

# Ejecutar todas las pruebas
python -m pytest tests/

# Ejecutar un archivo específico
python -m pytest tests/test_cruds.py

# Ejecutar con más detalles
python -m pytest tests/test_cruds.py -v

# Ejecutar una prueba específica
python -m pytest tests/test_cruds.py::test_crud_persona
```

### 2. Usando el Script Batch

También puedes usar el script batch incluido:

```cmd
cd tests
testFull.bat
```

## Tipos de Pruebas

1. **Pruebas CRUD** (`test_cruds.py`):
   - test_crud_persona: Prueba creación y lectura de personas
   - test_crud_telefono: Prueba creación de teléfonos
   - test_crud_email: Prueba creación de emails
   - test_login: Prueba autenticación

2. **Pruebas de Modelos** (`test_modelos.py`):
   - Pruebas de las clases modelo
   - Validación de relaciones entre modelos

## Solución de Problemas

Si encuentras errores de importación:

1. Verifica que estés en el directorio correcto (`EjemploModular`)
2. Asegúrate de que existan los archivos `__init__.py` en:
   - `EjemploModular/`
   - `EjemploModular/models/`
   - `EjemploModular/crud/`
   - `EjemploModular/tests/`
   - `EjemploModular/test_runner.py`
   - `test_telefono_crud.py`
   - `test_telefono_modelo.py`



## Consejos Adicionales

- Ejecuta las pruebas regularmente durante el desarrollo
- Revisa los mensajes de error con atención
- Mantén la base de datos en un estado limpio antes de las pruebas
- Usa los scripts de limpieza si es necesario (`tests/limpiar.py`)

## Estructura de Directorios

```
EjemploModular/
├── crud/
│   ├── __init__.py
│   ├── persona_crud.py
│   ├── telefono_crud.py
│   └── email_crud.py
├── models/
│   ├── __init__.py
│   ├── persona.py
│   ├── telefono.py
│   └── email.py
├── tests/
│   ├── __init__.py
│   ├── test_cruds.py
│   ├── test_modelos.py
│   └── test_completo_cruds.py
└── __init__.py
```

python tests/test_completo_cruds.py

# activar base dedatos para pruebas
Opción 3: Desactivar temporalmente la restricción (solo para pruebas)

⚠️ No recomendado en producción, pero útil para depurar:

´´´sql
SET FOREIGN_KEY_CHECKS = 0;
-- realizar pruebas
SET FOREIGN_KEY_CHECKS = 1;´´´


# otra forma ejecutar prueba
´´´c:\Users\LILLYU\Documents\GitHub\AgendaORMRelacional\EjemploModular\tests>cd c:\Users\LILLYU\Documents\GitHub\AgendaORMRelacional\EjemploModular\tests && python test_telefono_crud.py´´´