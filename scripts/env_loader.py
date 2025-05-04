#!/usr/bin/env python3
"""
Módulo centralizado para cargar y acceder a variables de entorno
Este módulo debe ser importado por todos los agentes y scripts que necesiten
acceder a las variables de entorno configuradas en el archivo .env
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TalentekIA-EnvLoader")

class EnvLoader:
    """Clase para cargar y gestionar variables de entorno"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implementación de patrón Singleton para asegurar una única instancia"""
        if cls._instance is None:
            cls._instance = super(EnvLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa el cargador de entorno si no se ha inicializado ya"""
        if not self._initialized:
            self._load_env()
            self._initialized = True
    
    def _load_env(self):
        """Carga las variables de entorno desde el archivo .env"""
        # Encontrar la ruta del archivo .env (subiendo directorios si es necesario)
        current_dir = Path(__file__).parent
        project_dir = current_dir.parent  # Directorio raíz del proyecto
        env_path = project_dir / '.env'
        
        if env_path.exists():
            logger.info(f"Cargando variables de entorno desde {env_path}")
            load_dotenv(env_path)
            self.env_file_path = env_path
        else:
            logger.warning(f"Archivo .env no encontrado en {env_path}")
            self.env_file_path = None
    
    def get(self, key, default=None):
        """Obtiene una variable de entorno"""
        return os.getenv(key, default)
    
    def get_api_key(self, service):
        """Obtiene una clave de API específica"""
        key_mapping = {
            'openai': 'OPENAI_API_KEY',
            'github': 'GITHUB_TOKEN',
            'huggingface': 'HUGGINGFACE_TOKEN',  # Corregido para coincidir con .env
            'linkedin': 'LINKEDIN_COOKIES',
            'google': 'GOOGLE_CLIENT_SECRET',
            'anythingllm': 'ANYTHINGLLM_API_KEY',  # Corregido para coincidir con .env
            'qdrant': 'QDRANT_API_KEY'
        }
        
        env_var = key_mapping.get(service.lower())
        if not env_var:
            logger.warning(f"Servicio desconocido: {service}")
            return None
        
        value = os.getenv(env_var)
        if not value and service.lower() != 'qdrant':  # Qdrant puede ser vacío
            logger.warning(f"Clave de API no configurada para {service}")
        
        return value
    
    def get_all(self):
        """Devuelve un diccionario con todas las variables de entorno relevantes"""
        # Excluir variables sensibles como claves API de la salida completa
        sensitive_keys = [
            'OPENAI_API_KEY', 'GITHUB_TOKEN', 'HUGGINGFACE_TOKEN', 'LINKEDIN_PASSWORD',
            'GOOGLE_CLIENT_SECRET', 'ANYTHINGLLM_API_KEY'
        ]
        
        result = {}
        for key, value in os.environ.items():
            # Solo incluir variables que parezcan de configuración (mayúsculas)
            if key.isupper() and not key.startswith('_'):
                if key in sensitive_keys:
                    result[key] = f"{value[:5]}...{value[-5:]}" if value and len(value) > 10 else "[CONFIGURADO]"
                else:
                    result[key] = value
                    
        return result
    
    def is_configured(self, service):
        """Verifica si un servicio está configurado correctamente"""
        return bool(self.get_api_key(service))
    
    def get_performance_mode(self):
        """Obtiene el modo de rendimiento configurado"""
        return os.getenv('PERFORMANCE_MODE', 'balanced')
    
    def get_update_frequency(self, agent_name):
        """Obtiene la frecuencia de actualización para un agente específico"""
        key = f"UPDATE_FREQUENCY_{agent_name.upper()}"
        return os.getenv(key, "Daily 09:00")

# Crear una instancia global para uso en toda la aplicación
env = EnvLoader()

# Función de ayuda para acceso rápido
def get_env(key, default=None):
    """Función de ayuda para obtener una variable de entorno"""
    return env.get(key, default)

# Ejemplo de uso
if __name__ == "__main__":
    print("Variables de entorno cargadas:")
    for key, value in env.get_all().items():
        print(f"- {key}: {value}")
    
    print("\nEstado de configuración de servicios:")
    for service in ['openai', 'github', 'linkedin', 'google', 'huggingface', 'anythingllm']:
        status = "✅ Configurado" if env.is_configured(service) else "❌ No configurado"
        print(f"- {service}: {status}")
    
    print(f"\nModo de rendimiento: {env.get_performance_mode()}")
    print(f"Frecuencia de actualización LinkedIn: {env.get_update_frequency('linkedin')}")