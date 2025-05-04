#!/usr/bin/env python3
"""
Utilidad para cargar variables de entorno de forma segura.
Este script carga variables desde el archivo .env y proporciona
acceso seguro a credenciales y configuraciones.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('env_loader')

def find_project_root() -> str:
    """
    Encuentra la raíz del proyecto buscando hacia arriba hasta encontrar el archivo .env
    o el directorio .git.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navegar hacia arriba hasta encontrar .env o .git
    while current_dir != os.path.dirname(current_dir):  # Hasta llegar a la raíz del sistema
        if os.path.exists(os.path.join(current_dir, '.env')) or \
           os.path.exists(os.path.join(current_dir, '.git')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # Si no se encuentra, usar el directorio actual
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_env_file(env_path: str) -> Dict[str, str]:
    """
    Carga variables de entorno desde un archivo .env
    
    Args:
        env_path: Ruta al archivo .env
        
    Returns:
        Diccionario con las variables cargadas
    """
    env_vars = {}
    
    if not os.path.exists(env_path):
        logger.warning(f"Archivo .env no encontrado en {env_path}")
        return env_vars
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Eliminar comillas si existen
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    # Expandir variables referenciadas como ${VAR}
                    if '${' in value and '}' in value:
                        var_name = value.split('${')[1].split('}')[0]
                        var_value = os.environ.get(var_name, '')
                        value = value.replace(f'${{{var_name}}}', var_value)
                    
                    env_vars[key] = value
        
        logger.debug(f"Cargadas {len(env_vars)} variables desde {env_path}")
        return env_vars
    except Exception as e:
        logger.error(f"Error al cargar archivo .env: {str(e)}")
        return {}

def get_env(key: str, default: Any = None) -> str:
    """
    Obtiene una variable de entorno, primero del sistema y luego del archivo .env
    
    Args:
        key: Nombre de la variable
        default: Valor por defecto si no se encuentra
        
    Returns:
        Valor de la variable o el valor por defecto
    """
    # Primero buscar en variables de entorno del sistema
    value = os.environ.get(key)
    if value is not None:
        return value
    
    # Si no se encuentra, buscar en el archivo .env cargado
    if not hasattr(get_env, '_env_vars'):
        project_root = find_project_root()
        env_path = os.path.join(project_root, '.env')
        get_env._env_vars = load_env_file(env_path)
    
    return get_env._env_vars.get(key, default)

def get_secret(key: str, default: Any = None) -> str:
    """
    Obtiene una variable secreta (como tokens o contraseñas)
    Esta función es similar a get_env pero añade una capa de seguridad
    para variables sensibles.
    
    Args:
        key: Nombre de la variable secreta
        default: Valor por defecto si no se encuentra
        
    Returns:
        Valor de la variable secreta o el valor por defecto
    """
    value = get_env(key, default)
    
    # Registrar acceso a secreto (sin mostrar el valor)
    if value != default:
        logger.debug(f"Acceso a variable secreta: {key} (valor oculto)")
    else:
        logger.warning(f"Variable secreta no encontrada: {key}")
    
    return value

def is_production() -> bool:
    """Verifica si el entorno actual es de producción."""
    return get_env('TALENTEK_ENV', 'development').lower() == 'production'

def get_project_root() -> str:
    """Obtiene la ruta raíz del proyecto."""
    return get_env('TALENTEK_ROOT', find_project_root())

# Ejemplo de uso
if __name__ == "__main__":
    print(f"Raíz del proyecto: {get_project_root()}")
    print(f"Entorno: {get_env('TALENTEK_ENV', 'development')}")
    print(f"Es producción: {is_production()}")
    
    # No mostrar tokens directamente en logs o salidas
    has_github_token = "Sí" if get_secret('GITHUB_TOKEN') else "No"
    has_anything_llm_token = "Sí" if get_secret('ANYTHING_LLM_API_KEY') else "No"
    
    print(f"Token de GitHub configurado: {has_github_token}")
    print(f"Token de Anything LLM configurado: {has_anything_llm_token}")