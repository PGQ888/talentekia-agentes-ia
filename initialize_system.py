#!/usr/bin/env python3
"""
Script de inicialización del sistema TalentekIA
Este script configura el entorno, verifica dependencias y prepara el sistema para su ejecución
"""
import os
import sys
import subprocess
import logging
import platform
from pathlib import Path
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_init.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TalentekIA-Initializer")

def print_banner():
    """Muestra un banner de bienvenida"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗████████╗     ║
    ║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║╚══██╔══╝     ║
    ║      ██║   ███████║██║     █████╗  ██╔██╗ ██║   ██║        ║
    ║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║   ██║        ║
    ║      ██║   ██║  ██║███████╗███████╗██║ ╚████║   ██║        ║
    ║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝        ║
    ║                                                            ║
    ║   Sistema Multiagente de Inteligencia Artificial           ║
    ║   Versión 1.0.0                                            ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_command(command):
    """Ejecuta un comando y devuelve el resultado"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def check_environment():
    """Verifica el entorno de ejecución"""
    logger.info("Verificando entorno de ejecución...")
    
    # Verificar versión de Python
    python_version = platform.python_version()
    logger.info(f"Versión de Python: {python_version}")
    if tuple(map(int, python_version.split('.'))) < (3, 8):
        logger.warning("Se recomienda Python 3.8 o superior")
    
    # Verificar sistema operativo
    system = platform.system()
    release = platform.release()
    logger.info(f"Sistema operativo: {system} {release}")
    
    # Verificar si es un Mac con chip Apple Silicon
    if system == "Darwin":
        processor = platform.processor()
        is_apple_silicon = "arm" in processor.lower()
        logger.info(f"Procesador: {processor} (Apple Silicon: {is_apple_silicon})")
        
        if is_apple_silicon:
            logger.info("Detectado Mac con Apple Silicon - Optimizaciones disponibles")
    
    # Verificar entorno virtual
    in_virtualenv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    logger.info(f"Entorno virtual: {'Activo' if in_virtualenv else 'No activo'}")
    
    if not in_virtualenv:
        logger.warning("Se recomienda usar un entorno virtual para este proyecto")
    
    return True

def check_dependencies():
    """Verifica e instala dependencias"""
    logger.info("Verificando dependencias...")
    
    project_dir = Path(__file__).parent
    requirements_file = project_dir / "requirements.txt"
    
    if not requirements_file.exists():
        logger.error(f"Archivo de requisitos no encontrado: {requirements_file}")
        return False
    
    logger.info("Instalando dependencias...")
    success, output = run_command(f"pip install -r {requirements_file}")
    
    if not success:
        logger.error(f"Error al instalar dependencias: {output}")
        return False
    
    logger.info("Dependencias instaladas correctamente")
    return True

def setup_directories():
    """Configura los directorios necesarios"""
    logger.info("Configurando directorios del sistema...")
    
    project_dir = Path(__file__).parent
    directories = [
        "data",
        "logs",
        "docs",
        "config",
        "agents",
        "models"
    ]
    
    for dir_name in directories:
        dir_path = project_dir / dir_name
        if not dir_path.exists():
            logger.info(f"Creando directorio: {dir_name}")
            dir_path.mkdir(exist_ok=True)
    
    logger.info("Directorios configurados correctamente")
    return True

def check_api_keys():
    """Verifica las claves API configuradas"""
    logger.info("Verificando claves API...")
    
    # Importar el cargador de entorno
    sys.path.append(str(Path(__file__).parent))
    try:
        from scripts.env_loader import env
        
        # Verificar servicios principales
        services = {
            'openai': 'OpenAI API',
            'github': 'GitHub',
            'linkedin': 'LinkedIn',
            'google': 'Google API',
            'huggingface': 'Hugging Face',
            'anythingllm': 'AnythingLLM'
        }
        
        all_configured = True
        for service_key, service_name in services.items():
            if env.is_configured(service_key):
                logger.info(f"✅ {service_name}: Configurado correctamente")
            else:
                logger.warning(f"❌ {service_name}: No configurado")
                all_configured = False
        
        return all_configured
    except ImportError as e:
        logger.error(f"Error al importar el módulo env_loader: {str(e)}")
        return False

def main():
    """Función principal"""
    print_banner()
    logger.info("Iniciando configuración del sistema TalentekIA...")
    
    # Verificar entorno
    if not check_environment():
        logger.error("Verificación del entorno fallida")
        return False
    
    # Configurar directorios
    if not setup_directories():
        logger.error("Configuración de directorios fallida")
        return False
    
    # Verificar dependencias
    if not check_dependencies():
        logger.error("Verificación de dependencias fallida")
        return False
    
    # Verificar claves API
    api_keys_status = check_api_keys()
    if not api_keys_status:
        logger.warning("Algunas claves API no están configuradas")
        print("\n⚠️  ATENCIÓN: Algunas claves API no están configuradas correctamente.")
        print("   Revisa el archivo .env y asegúrate de que todas las claves necesarias estén presentes.\n")
    
    # Todo configurado correctamente
    logger.info("Sistema TalentekIA inicializado correctamente")
    print("\n✅ Sistema TalentekIA inicializado correctamente")
    print("   Para iniciar la aplicación Streamlit, ejecuta:")
    print("   streamlit run streamlit_app_fixed.py\n")
    print("   Para iniciar la sincronización automática, ejecuta:")
    print("   ./start_auto_sync.sh\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)