# Makefile para TalentekIA

.PHONY: setup run test clean lint format sync-start sync-stop install-dev docs

# Variables
PYTHON = python3
PIP = pip
STREAMLIT = streamlit
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8

# Configuración
setup:
	@echo "Configurando TalentekIA..."
	$(PYTHON) initialize_system.py

# Ejecución
run:
	@echo "Iniciando la aplicación TalentekIA..."
	$(STREAMLIT) run src/interface/streamlit_app.py

# Pruebas
test:
	@echo "Ejecutando pruebas..."
	$(PYTEST) tests/

# Limpieza
clean:
	@echo "Limpiando archivos temporales..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete

# Formateo y linting
lint:
	@echo "Ejecutando linting..."
	$(FLAKE8) src/ tests/

format:
	@echo "Formateando código..."
	$(BLACK) src/ tests/
	$(ISORT) src/ tests/

# Sincronización automática
sync-start:
	@echo "Iniciando sincronización automática..."
	./start_auto_sync.sh

sync-stop:
	@echo "Deteniendo sincronización automática..."
	./stop_auto_sync.sh

# Desarrollo
install-dev:
	@echo "Instalando dependencias de desarrollo..."
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

# Documentación
docs:
	@echo "Generando documentación..."
	cd docs && sphinx-build -b html . _build

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make setup       - Configurar el sistema"
	@echo "  make run         - Iniciar la aplicación"
	@echo "  make test        - Ejecutar pruebas"
	@echo "  make clean       - Limpiar archivos temporales"
	@echo "  make lint        - Ejecutar linting"
	@echo "  make format      - Formatear código"
	@echo "  make sync-start  - Iniciar sincronización automática"
	@echo "  make sync-stop   - Detener sincronización automática"
	@echo "  make install-dev - Instalar dependencias de desarrollo"
	@echo "  make docs        - Generar documentación"

# Comando por defecto
default: help