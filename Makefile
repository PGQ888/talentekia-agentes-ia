# Makefile para TalentekIA - Optimizado para Mac M2

.PHONY: setup dev build run clean test lint docs

# Variables
DOCKER_IMAGE = talentekia:latest
DOCKER_RUN = docker run --platform linux/arm64 -it --rm -p 8000:8000 -v $(PWD):/app

# Configuración inicial del entorno
setup:
	@echo "Configurando entorno de desarrollo..."
	@chmod +x dev.sh
	@./dev.sh

# Activar entorno de desarrollo
dev:
	@echo "Activando entorno de desarrollo..."
	@source dev.sh

# Construir imagen Docker
build:
	@echo "Construyendo imagen Docker..."
	@docker build --platform linux/arm64 -t $(DOCKER_IMAGE) .

# Ejecutar contenedor Docker
run:
	@echo "Ejecutando contenedor Docker..."
	@$(DOCKER_RUN) $(DOCKER_IMAGE)

# Ejecutar shell en contenedor Docker
shell:
	@echo "Iniciando shell en contenedor Docker..."
	@$(DOCKER_RUN) $(DOCKER_IMAGE) bash

# Limpiar archivos temporales y cachés
clean:
	@echo "Limpiando archivos temporales y cachés..."
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".DS_Store" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "*.egg" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -exec rm -rf {} +
	@rm -rf build/
	@rm -rf dist/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/

# Ejecutar tests
test:
	@echo "Ejecutando tests..."
	@python -m pytest tests/ -v

# Ejecutar linting
lint:
	@echo "Ejecutando linting..."
	@python -m flake8 src/ tests/
	@python -m black --check src/ tests/

# Formatear código automáticamente
format:
	@echo "Formateando código..."
	@python -m black src/ tests/
	@python -m isort src/ tests/

# Generar documentación
docs:
	@echo "Generando documentación..."
	@cd docs && make html

# Mostrar ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make setup    - Configurar entorno de desarrollo"
	@echo "  make dev      - Activar entorno de desarrollo"
	@echo "  make build    - Construir imagen Docker"
	@echo "  make run      - Ejecutar contenedor Docker"
	@echo "  make shell    - Iniciar shell en contenedor Docker"
	@echo "  make clean    - Limpiar archivos temporales y cachés"
	@echo "  make test     - Ejecutar tests"
	@echo "  make lint     - Ejecutar linting"
	@echo "  make format   - Formatear código automáticamente"
	@echo "  make docs     - Generar documentación"
	@echo "  make help     - Mostrar esta ayuda"