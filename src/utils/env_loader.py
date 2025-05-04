#!/usr/bin/env python3
"""
Utilidad para cargar variables de entorno de archivos .env
Busca en múltiples ubicaciones y aplica optimizaciones para Mac M2
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger("TalentekIA-EnvLoader")

class EnvLoader:
    """Cargador de variables de entorno desde archivos .env"""
    
    def __init__(self):
        self.env_loaded = False
        self.env_path = None
    
    def load_env(self) -> bool:
        """
        Carga variables de entorno desde un archivo .env
        Busca en múltiples ubicaciones
        
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        if self.env_loaded:
            return True
        
        # Posibles ubicaciones del archivo .env
        root_dir = Path(__file__).parent.parent.parent
        possible_paths = [
            root_dir / ".env",
            root_dir / "src" / ".env",
            root_dir / "config" / ".env",
            Path(os.getcwd()) / ".env"
        ]
        
        for path in possible_paths:
            if path.exists():
                self.env_path = path
                break
        
        if not self.env_path:
            # Si no encontramos un archivo .env, crear uno en el directorio src/
            src_env_path = root_dir / "src" / ".env"
            if not src_env_path.parent.exists():
                src_env_path.parent.mkdir(exist_ok=True)
            
            # Copiar el .env de la raíz si existe o crear uno básico
            root_env_path = root_dir / ".env"
            if root_env_path.exists():
                import shutil
                shutil.copy(root_env_path, src_env_path)
                logger.info(f"Copiado archivo .env desde {root_env_path} a {src_env_path}")
            else:
                # Crear un .env básico
                with open(src_env_path, "w") as f:
                    f.write("""# Variables de entorno para TalentekIA
# Optimizado para Mac M2

# API Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
HUGGINGFACE_API_KEY=

# Optimizaciones Mac M2
PYTORCH_ENABLE_MPS_FALLBACK=1
TF_ENABLE_ONEDNN_OPTS=0
PYTORCH_DEVICE=mps
""")
                logger.info(f"Creado nuevo archivo .env en {src_env_path}")
            
            self.env_path = src_env_path
        
        # Cargar las variables de entorno
        try:
            from dotenv import load_dotenv
            load_dotenv(self.env_path)
            logger.info(f"Cargando variables de entorno desde {self.env_path}")
            self.env_loaded = True
            return True
        except ImportError:
            logger.warning("No se pudo importar dotenv. Las variables de entorno no se cargarán desde el archivo .env")
            return False
        except Exception as e:
            logger.error(f"Error al cargar variables de entorno: {str(e)}")
            return False
    
    def get_env(self, key: str, default: Any = None) -> Optional[str]:
        """
        Obtiene una variable de entorno
        
        Args:
            key: Nombre de la variable
            default: Valor por defecto si no existe
            
        Returns:
            Optional[str]: Valor de la variable o el valor por defecto
        """
        if not self.env_loaded:
            self.load_env()
        
        return os.environ.get(key, default)
    
    def set_env(self, key: str, value: str) -> None:
        """
        Establece una variable de entorno
        
        Args:
            key: Nombre de la variable
            value: Valor de la variable
        """
        os.environ[key] = value

# Crear una instancia global para usar en todo el proyecto
env = EnvLoader()

# Cargar variables automáticamente cuando se importa
env.load_env()