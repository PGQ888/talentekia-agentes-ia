.PHONY: clean clean-build clean-pyc clean-test coverage deps dev-deps docs help install lint test test-all

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help: ## Muestra este mensaje de ayuda
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## Elimina todos los archivos generados

clean-build: ## Elimina archivos de construcción
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## Elimina archivos de Python compilados
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Elimina archivos de prueba y cobertura
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

deps: ## Instala dependencias de producción
	pip install -e .

dev-deps: ## Instala dependencias de desarrollo
	pip install -e ".[dev,docs]"
	pip install pre-commit
	pre-commit install

m2-deps: ## Instala dependencias específicas para Mac M2
	pip install -e ".[m2]"

lint: ## Verifica el estilo con flake8, black e isort
	flake8 src tests
	black --check src tests
	isort --check-only --profile black src tests

format: ## Formatea el código con black e isort
	black src tests
	isort --profile black src tests

test: ## Ejecuta las pruebas
	pytest

test-all: ## Ejecuta las pruebas con todos los entornos de tox
	tox

coverage: ## Verifica la cobertura del código
	pytest --cov=src tests/
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## Genera la documentación HTML
	rm -f docs/source/api/src.rst
	rm -f docs/source/api/modules.rst
	sphinx-apidoc -o docs/source/api src
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/build/html/index.html

servedocs: docs ## Compila la documentación y la sirve localmente
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## Empaqueta y sube una versión
	twine upload dist/*

dist: clean ## Construye el paquete
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## Instala el paquete en el entorno activo
	pip install -e .

venv: ## Crea un entorno virtual
	python -m venv venv
	@echo "Ejecuta 'source venv/bin/activate' para activar el entorno virtual"

run: ## Ejecuta el sistema TalentekIA
	./start_talentek.sh

monitor: ## Ejecuta el monitor de rendimiento para Mac M2
	./scripts/monitor_m2.py --continuous

setup-m2: ## Configura el entorno para Mac M2
	export PYTORCH_ENABLE_MPS_FALLBACK=1
	export TF_ENABLE_ONEDNN_OPTS=0
	@echo "Variables de entorno configuradas para Mac M2"