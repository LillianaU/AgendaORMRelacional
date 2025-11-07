@echo off
REM Script de ejecución de tests - corregido y portable
REM Se sitúa en el directorio padre (raíz del proyecto EjemploModular)
pushd "%~dp0.."

echo LIMPIANDO CACHÉ...
rmdir /S /Q "models\__pycache__" 2>nul
rmdir /S /Q "crud\__pycache__" 2>nul
rmdir /S /Q "tests\__pycache__" 2>nul
del /S /Q *.pyc 2>nul

echo EJECUTANDO TESTS...
REM Si pytest está disponible, lo usamos (mejor reporte). Si no, fallback al runner del proyecto.
where pytest >nul 2>nul
if %errorlevel%==0 (
	echo Usando pytest
	python -m pytest -v
) else (
	echo pytest no encontrado, usando test_runner.py
	python test_runner.py
)

echo.
echo FIN DE TESTS
echo ============================
echo TODOS LOS TESTS EJECUTADOS
echo ============================
pause
popd