"""
Pruebas para el módulo de carga de variables de entorno
"""
import os
import pytest
from scripts.env_loader import env, get_env

def test_env_loader_singleton(test_env):
    """Prueba que el EnvLoader sea un singleton"""
    from scripts.env_loader import EnvLoader
    
    # Crear dos instancias y verificar que sean la misma
    loader1 = EnvLoader()
    loader2 = EnvLoader()
    assert loader1 is loader2
    
    # Verificar que la instancia global es la misma
    assert env is loader1

def test_get_env_function(test_env):
    """Prueba la función auxiliar get_env"""
    # Establecer una variable de entorno temporal
    os.environ['TEST_VAR'] = 'test_value'
    
    # Verificar que get_env la obtiene correctamente
    assert get_env('TEST_VAR') == 'test_value'
    
    # Verificar que get_env devuelve el valor por defecto
    assert get_env('NON_EXISTENT_VAR', 'default') == 'default'

def test_api_key_retrieval(test_env):
    """Prueba la obtención de claves API"""
    # Establecer una clave API temporal
    os.environ['OPENAI_API_KEY'] = 'test_openai_key'
    
    # Verificar que se puede obtener la clave
    assert test_env.get_api_key('openai') == 'test_openai_key'
    
    # Verificar que un servicio desconocido devuelve None
    assert test_env.get_api_key('unknown_service') is None

def test_performance_mode(test_env):
    """Prueba la obtención del modo de rendimiento"""
    # Establecer un modo de rendimiento temporal
    os.environ['PERFORMANCE_MODE'] = 'eco'
    
    # Verificar que se obtiene correctamente
    assert test_env.get_performance_mode() == 'eco'
    
    # Cambiar el modo y verificar de nuevo
    os.environ['PERFORMANCE_MODE'] = 'performance'
    assert test_env.get_performance_mode() == 'performance'