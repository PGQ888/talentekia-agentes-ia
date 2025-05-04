#!/usr/bin/env python3
"""
Script de migración para la unificación del sistema TalentekIA
Este script migra los agentes existentes a la nueva estructura unificada
"""

import os
import sys
import shutil
import logging
from pathlib import Path
import toml
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"migracion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    ]
)

logger = logging.getLogger("TalentekIA-Migración")

# Definir rutas
SOURCE_ROOT = Path(__file__).parent.parent.parent  # Directorio raíz actual
TARGET_ROOT = Path(__file__).parent.parent  # Directorio del sistema unificado

# Estructura de directorios a crear
DIRECTORIES = [
    "agents/linkedin",
    "agents/finanzas",
    "agents/auto_improve",
    "agents/estrategia",
    "agents/email",
    "agents/resumen",
    "data/linkedin",
    "data/finanzas",
    "data/estrategia",
    "data/email",
    "data/automejora",
    "data/resumen",
    "logs",
    "utils",
    "scripts"
]

# Mapeo de agentes (origen -> destino)
AGENT_MAPPING = {
    "src/agents/linkedin_agent.py": "agents/linkedin/linkedin_agent.py",
    "src/agents/estrategia_comercial_agent.py": "agents/estrategia/estrategia_comercial_agent.py",
    "src/agents/finanzas_personales_agent.py": "agents/finanzas/finanzas_personales_agent.py",
    "src/agents/automejora_agent.py": "agents/auto_improve/automejora_agent.py",
    "src/agents/email_automation_agent.py": "agents/email/email_automation_agent.py",
    "src/agents/resumen_semanal_agent.py": "agents/resumen/resumen_semanal_agent.py",
    "src/agents/base_agent.py": "agents/base_agent.py",
    "src/agents/agent_manager.py": "agents/agent_manager.py",
    "src/utils/env_loader.py": "utils/env_loader.py",
    "src/utils/async_helper.py": "utils/async_helper.py"
}

def create_directory_structure():
    """Crea la estructura de directorios necesaria"""
    logger.info("Creando estructura de directorios...")
    
    for directory in DIRECTORIES:
        target_dir = TARGET_ROOT / directory
        if not target_dir.exists():
            target_dir.mkdir(parents=True)
            logger.info(f"Creado directorio: {target_dir}")
        else:
            logger.info(f"El directorio ya existe: {target_dir}")

def migrate_agents():
    """Migra los archivos de los agentes a la nueva estructura"""
    logger.info("Migrando archivos de agentes...")
    
    for source_path, target_path in AGENT_MAPPING.items():
        source_file = SOURCE_ROOT / source_path
        target_file = TARGET_ROOT / target_path
        
        if source_file.exists():
            # Asegurar que el directorio destino existe
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copiar el archivo
            shutil.copy2(source_file, target_file)
            logger.info(f"Copiado: {source_file} -> {target_file}")
        else:
            logger.warning(f"Archivo de origen no encontrado: {source_file}")

def adjust_imports():
    """Ajusta las importaciones en los archivos migrados"""
    logger.info("Ajustando importaciones en archivos migrados...")
    
    for _, target_path in AGENT_MAPPING.items():
        file_path = TARGET_ROOT / target_path
        if not file_path.exists():
            logger.warning(f"No se encontró el archivo para ajustar: {file_path}")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Ajustar importaciones
        content = content.replace('from src.agents.base_agent', 'from agents.base_agent')
        content = content.replace('from src.utils.env_loader', 'from utils.env_loader')
        content = content.replace('from src.utils.async_helper', 'from utils.async_helper')
        
        # Para importaciones relativas entre agentes
        content = content.replace('from src.agents.', 'from agents.')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        logger.info(f"Ajustadas importaciones en: {file_path}")

def create_agent_config_files():
    """Crea archivos de configuración individuales para cada agente basado en el TOML principal"""
    logger.info("Creando archivos de configuración individuales para cada agente...")
    
    # Leer configuración principal
    config_path = TARGET_ROOT / "config" / "talentek_agentes_config.toml"
    if not config_path.exists():
        logger.error(f"No se encontró el archivo de configuración principal: {config_path}")
        return
    
    # Cargar configuración TOML
    try:
        config = toml.load(config_path)
    except Exception as e:
        logger.error(f"Error al cargar la configuración TOML: {str(e)}")
        return
    
    # Extraer configuración de cada agente
    for key, value in config.items():
        if key.startswith('agente_'):
            agent_id = key.replace('agente_', '')
            agent_config = value
            
            # Añadir información global necesaria
            agent_config['id'] = agent_id
            agent_config['entorno'] = config.get('entorno', {})
            agent_config['rutas'] = config.get('rutas', {})
            
            # Determinar la ruta de destino para el archivo de configuración
            if agent_id == 'linkedin':
                config_dir = TARGET_ROOT / "agents" / "linkedin" / "config"
            elif agent_id == 'estrategia_comercial':
                config_dir = TARGET_ROOT / "agents" / "estrategia" / "config"
            elif agent_id == 'finanzas_personales':
                config_dir = TARGET_ROOT / "agents" / "finanzas" / "config"
            elif agent_id == 'automejora':
                config_dir = TARGET_ROOT / "agents" / "auto_improve" / "config"
            elif agent_id == 'email_automation':
                config_dir = TARGET_ROOT / "agents" / "email" / "config"
            elif agent_id == 'resumen_semanal':
                config_dir = TARGET_ROOT / "agents" / "resumen" / "config"
            else:
                continue
            
            # Crear directorio de configuración si no existe
            config_dir.mkdir(parents=True, exist_ok=True)
            
            # Guardar configuración como JSON
            config_file = config_dir / f"{agent_id}_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(agent_config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Creado archivo de configuración: {config_file}")

def migrate_data():
    """Migra los datos existentes a la nueva estructura"""
    logger.info("Migrando datos...")
    
    # Directorios de datos a migrar
    data_dirs = [
        ('data/linkedin', 'data/linkedin'),
        ('data/finanzas', 'data/finanzas'),
        ('data/estrategia', 'data/estrategia'),
        ('data/email', 'data/email'),
        ('data/automejora', 'data/automejora'),
        ('data/resumen', 'data/resumen')
    ]
    
    for source_dir, target_dir in data_dirs:
        source_path = SOURCE_ROOT / source_dir
        target_path = TARGET_ROOT / target_dir
        
        if source_path.exists() and source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Copiar archivos (no directorios completos para evitar copiar cosas no deseadas)
            for item in source_path.glob('*'):
                if item.is_file():
                    shutil.copy2(item, target_path / item.name)
                    logger.info(f"Copiado: {item} -> {target_path / item.name}")
        else:
            logger.info(f"Directorio de datos no existe o está vacío: {source_path}")

def create_init_files():
    """Crea los archivos __init__.py necesarios para importaciones"""
    logger.info("Creando archivos __init__.py...")
    
    init_paths = [
        "agents",
        "agents/linkedin",
        "agents/finanzas",
        "agents/auto_improve",
        "agents/estrategia",
        "agents/email",
        "agents/resumen",
        "utils"
    ]
    
    for path in init_paths:
        init_file = TARGET_ROOT / path / "__init__.py"
        
        # Crear archivo vacío si no existe
        if not init_file.exists():
            init_file.write_text("# Archivo generado automáticamente para importaciones\n")
            logger.info(f"Creado archivo: {init_file}")

def create_requirements_file():
    """Crea un archivo requirements.txt unificado"""
    logger.info("Creando archivo requirements.txt unificado...")
    
    # Lista de dependencias
    dependencies = [
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "toml==0.10.2",
        "pydantic==2.3.0",
        "aiohttp==3.8.5",
        "beautifulsoup4==4.12.2",
        "markdown==3.4.4",
        "pillow==9.5.0",
        "openpyxl==3.1.2",
        "python-linkedin-v2==0.9.4",
        "setuptools==68.0.0",
        "pytest==7.4.0"
    ]
    
    # Guardar archivo
    requirements_file = TARGET_ROOT / "requirements.txt"
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write("# Dependencias del sistema TalentekIA\n")
        f.write("# Generado automáticamente por el script de migración\n\n")
        
        for dep in dependencies:
            f.write(f"{dep}\n")
    
    logger.info(f"Creado archivo: {requirements_file}")

def create_env_example():
    """Crea un archivo .env.example como plantilla"""
    logger.info("Creando archivo .env.example...")
    
    env_content = """# Variables de entorno para TalentekIA
# Copia este archivo como .env y completa los valores

# Claves de API
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
LINKEDIN_API_KEY=your_linkedin_key

# Configuración de correo
EMAIL_USERNAME=your_email@example.com
EMAIL_PASSWORD=your_email_password
EMAIL_SMTP=smtp.example.com
EMAIL_PORT=587

# Configuración del sistema
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development
"""
    
    env_file = TARGET_ROOT / ".env.example"
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    logger.info(f"Creado archivo: {env_file}")

def main():
    """Función principal del script de migración"""
    print("\n" + "=" * 60)
    print("  TALENTEK IA - MIGRACIÓN A ESTRUCTURA UNIFICADA")
    print("=" * 60)
    
    logger.info("Iniciando migración a estructura unificada...")
    
    try:
        # 1. Crear estructura de directorios
        create_directory_structure()
        
        # 2. Migrar agentes
        migrate_agents()
        
        # 3. Ajustar importaciones
        adjust_imports()
        
        # 4. Crear archivos de configuración individuales
        create_agent_config_files()
        
        # 5. Migrar datos
        migrate_data()
        
        # 6. Crear archivos __init__.py
        create_init_files()
        
        # 7. Crear requirements.txt
        create_requirements_file()
        
        # 8. Crear .env.example
        create_env_example()
        
        logger.info("Migración completada con éxito")
        print("\n" + "=" * 60)
        print("  MIGRACIÓN COMPLETADA CON ÉXITO")
        print("=" * 60)
        print("\nLa estructura unificada se ha creado correctamente.")
        print("Puedes ejecutar el sistema con:")
        print("  python TalentekSystemUnified/launch_talentek_system.py")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error durante la migración: {str(e)}", exc_info=True)
        print("\n" + "=" * 60)
        print("  ERROR EN LA MIGRACIÓN")
        print("=" * 60)
        print(f"\nSe produjo un error: {str(e)}")
        print("Revisa el archivo de log para más detalles.")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())