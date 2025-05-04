"""
Gestor de variables de entorno para el sistema de agentes Talentek.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

class EnvLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvLoader, cls).__new__(cls)
            cls._instance._load_env()
        return cls._instance
    
    def _load_env(self) -> None:
        """Carga las variables de entorno desde el archivo .env."""
        # Buscar .env en varias ubicaciones posibles
        env_paths = [
            Path(".env"),
            Path(os.path.expanduser("~/.talentek/.env")),
            Path("/etc/talentek/.env")
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                print(f"Variables de entorno cargadas desde {env_path}")
                break
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene una variable de entorno."""
        return os.environ.get(key, default)
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Obtiene una clave API para un servicio específico."""
        key_name = f"{service.upper()}_API_KEY"
        return self.get(key_name)
    
    def get_performance_mode(self) -> str:
        """Obtiene el modo de rendimiento configurado."""
        return self.get("PERFORMANCE_MODE", "balanced")
    
    def get_all(self) -> Dict[str, str]:
        """Obtiene todas las variables de entorno."""
        return dict(os.environ)
    
    def is_configured(self, service: str) -> bool:
        """Verifica si un servicio está configurado con su API key."""
        key = self.get_api_key(service)
        return key is not None and key != ""
    
    def get_update_frequency(self, agent_name: str) -> str:
        """Obtiene la frecuencia de actualización para un agente específico."""
        key = f"{agent_name.upper()}_UPDATE_FREQUENCY"
        return self.get(key, "daily")

# Instancia global para uso en toda la aplicación
env_loader = EnvLoader()

def get_env(key: str, default: Any = None) -> Any:
    """Función de conveniencia para obtener una variable de entorno."""
    return env_loader.get(key, default)
