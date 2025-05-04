"""
Configuración para pruebas del proyecto TalentekIA
Este archivo contiene configuraciones y fixtures para pytest
"""
import os
import sys
import pytest
from pathlib import Path

# Añadir el directorio raíz al path para poder importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importar después de configurar el path
from scripts.env_loader import env

@pytest.fixture
def test_env():
    """Fixture que proporciona un entorno de prueba"""
    # Guardar variables de entorno originales
    original_env = {}
    for key in os.environ:
        original_env[key] = os.environ[key]
    
    # Configurar variables de entorno para pruebas
    os.environ['ENVIRONMENT'] = 'test'
    os.environ['DEBUG'] = 'true'
    os.environ['DATA_DIR'] = './tests/data'
    os.environ['LOGS_DIR'] = './tests/logs'
    
    yield env  # Proporcionar el objeto env para las pruebas
    
    # Restaurar variables de entorno originales
    for key in original_env:
        os.environ[key] = original_env[key]

@pytest.fixture
def test_config():
    """Fixture que proporciona una configuración de prueba"""
    return {
        'test_mode': True,
        'api_mock': True,
        'skip_external_calls': True
    }