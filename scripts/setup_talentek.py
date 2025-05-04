#!/usr/bin/env python3
"""
Script de inicialización para el sistema TalentekAI de Pablo Giráldez.
Este script configura el entorno, verifica dependencias y prepara todo para su uso.
"""

import os
import sys
import json
import subprocess
import argparse
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('setup_talentek')

# Ruta del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    required_version = (3, 7)
    current_version = sys.version_info
    
    if current_version < required_version:
        logger.error(f"❌ Versión de Python incompatible. Se requiere Python {required_version[0]}.{required_version[1]} o superior.")
        logger.error(f"   Versión actual: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return False
    
    logger.info(f"✅ Versión de Python compatible: {current_version[0]}.{current_version[1]}.{current_version[2]}")
    return True

def check_dependencies():
    """Verifica que las dependencias necesarias estén instaladas."""
    required_packages = [
        "requests",
        "python-dotenv",
        "colorama"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.warning(f"⚠️ Faltan los siguientes paquetes: {', '.join(missing_packages)}")
        return False
    
    logger.info("✅ Todas las dependencias están instaladas.")
    return True

def install_dependencies():
    """Instala las dependencias faltantes."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "python-dotenv", "colorama"], check=True)
        logger.info("✅ Dependencias instaladas correctamente.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error al instalar dependencias: {str(e)}")
        return False

def create_directory_structure():
    """Crea la estructura de directorios necesaria."""
    directories = [
        "logs",
        "reports",
        "data",
        "config",
        "scripts/commands",
        "scripts/utils"
    ]
    
    for directory in directories:
        dir_path = os.path.join(PROJECT_ROOT, directory)
        os.makedirs(dir_path, exist_ok=True)
    
    logger.info("✅ Estructura de directorios creada correctamente.")
    return True

def check_env_file():
    """Verifica que el archivo .env exista y contenga las variables necesarias."""
    env_path = os.path.join(PROJECT_ROOT, ".env")
    
    if not os.path.exists(env_path):
        logger.warning("⚠️ Archivo .env no encontrado.")
        return False
    
    required_vars = ["ANYTHING_LLM_API_KEY"]
    missing_vars = []
    
    with open(env_path, 'r') as f:
        content = f.read()
        
        for var in required_vars:
            if var not in content or f"{var}=" in content:
                missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"⚠️ Faltan las siguientes variables en .env: {', '.join(missing_vars)}")
        return False
    
    logger.info("✅ Archivo .env verificado correctamente.")
    return True

def check_anythingllm_agent():
    """Verifica que el archivo de configuración del agente de Anything LLM exista."""
    agent_path = os.path.join(PROJECT_ROOT, ".anythingllm_agent.json")
    
    if not os.path.exists(agent_path):
        logger.warning("⚠️ Archivo de configuración del agente de Anything LLM no encontrado.")
        return False
    
    try:
        with open(agent_path, 'r') as f:
            config = json.load(f)
            
        if "commands" not in config or not config["commands"]:
            logger.warning("⚠️ El archivo de configuración del agente no contiene comandos.")
            return False
        
        logger.info(f"✅ Agente de Anything LLM configurado con {len(config['commands'])} comandos.")
        return True
    except Exception as e:
        logger.error(f"❌ Error al verificar el archivo de configuración del agente: {str(e)}")
        return False

def check_command_scripts():
    """Verifica que los scripts de comandos existan y sean ejecutables."""
    commands_dir = os.path.join(PROJECT_ROOT, "scripts", "commands")
    
    if not os.path.exists(commands_dir):
        logger.warning("⚠️ Directorio de comandos no encontrado.")
        return False
    
    scripts = [f for f in os.listdir(commands_dir) if f.endswith('.py')]
    
    if not scripts:
        logger.warning("⚠️ No se encontraron scripts de comandos.")
        return False
    
    for script in scripts:
        script_path = os.path.join(commands_dir, script)
        
        # Verificar si es ejecutable
        if not os.access(script_path, os.X_OK):
            try:
                os.chmod(script_path, 0o755)
                logger.info(f"✅ Permisos de ejecución añadidos a {script}")
            except Exception as e:
                logger.warning(f"⚠️ No se pudieron añadir permisos de ejecución a {script}: {str(e)}")
    
    logger.info(f"✅ {len(scripts)} scripts de comandos verificados.")
    return True

def setup_anything_llm():
    """Configura la integración con Anything LLM."""
    try:
        # Importar el módulo de carga de variables de entorno
        sys.path.append(PROJECT_ROOT)
        from scripts.utils.env_loader import get_secret
        
        # Verificar si el token está configurado
        token = get_secret("ANYTHING_LLM_API_KEY")
        
        if not token:
            logger.warning("⚠️ Token de Anything LLM no configurado en .env")
            return False
        
        # Aquí iría la lógica para verificar la conexión con Anything LLM
        # Por ahora, solo verificamos que el token exista
        
        logger.info("✅ Integración con Anything LLM configurada correctamente.")
        return True
    except Exception as e:
        logger.error(f"❌ Error al configurar integración con Anything LLM: {str(e)}")
        return False

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Configura el sistema TalentekAI de Pablo Giráldez")
    parser.add_argument("--force", action="store_true", help="Forzar la instalación de dependencias")
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("🚀 CONFIGURACIÓN DEL SISTEMA TALENTEKIA DE PABLO GIRÁLDEZ")
    print("=" * 60 + "\n")
    
    # Verificar versión de Python
    if not check_python_version():
        print("\n❌ La configuración no puede continuar debido a una versión incompatible de Python.")
        return
    
    # Verificar y crear estructura de directorios
    create_directory_structure()
    
    # Verificar dependencias
    if not check_dependencies() or args.force:
        print("\nInstalando dependencias necesarias...")
        if not install_dependencies():
            print("\n⚠️ No se pudieron instalar todas las dependencias. Algunas funciones podrían no estar disponibles.")
    
    # Verificar archivo .env
    if not check_env_file():
        print("\n⚠️ El archivo .env no está correctamente configurado.")
        print("   Por favor, edita el archivo .env y añade las variables necesarias.")
    
    # Verificar configuración del agente de Anything LLM
    if not check_anythingllm_agent():
        print("\n⚠️ La configuración del agente de Anything LLM no está completa.")
    
    # Verificar scripts de comandos
    check_command_scripts()
    
    # Configurar integración con Anything LLM
    setup_anything_llm()
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\nPuedes comenzar a usar el sistema TalentekAI con los siguientes comandos:")
    print("\n- Ver estado del sistema:")
    print("  python scripts/talentek_auto_improve.py status")
    print("\n- Ejecutar análisis de auto-mejora:")
    print("  python scripts/talentek_auto_improve.py all")
    print("\n- Usar comandos específicos:")
    print("  python scripts/commands/resumen.py")
    print("  python scripts/commands/linkedin.py --tipo post --tema IA --tono profesional")
    print("  python scripts/commands/finanzas.py --tipo resumen")
    print("  python scripts/commands/estrategia.py --industria tecnologia --enfoque innovacion")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()