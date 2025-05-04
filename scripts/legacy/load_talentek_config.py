#!/usr/bin/env python3
"""
Script para cargar y procesar la configuración de agentes de TalentekIA desde TOML
Este script integra la configuración TOML con el sistema TalentekIA existente
"""
import os
import sys
import toml
import logging
from pathlib import Path
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TalentekIA-ConfigLoader")

def print_banner():
    """Muestra el banner de inicio de la aplicación"""
    banner = """
╔════════════════════════════════════════════════════╗
║                                                    ║
║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗      ║
║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║      ║
║      ██║   ███████║██║     █████╗  ██╔██╗ ██║      ║
║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║      ║
║      ██║   ██║  ██║███████╗███████╗██║ ╚████║      ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝      ║
║                                                    ║
║           Cargador de Configuración TOML           ║
║                                                    ║
║          Optimizado para Apple Silicon             ║
║                                                    ║
╚════════════════════════════════════════════════════╝
"""
    print(banner)

def load_toml_config(config_path):
    """Carga la configuración desde un archivo TOML"""
    try:
        logger.info(f"Cargando configuración desde {config_path}")
        config = toml.load(config_path)
        return config
    except Exception as e:
        logger.error(f"Error al cargar la configuración TOML: {str(e)}")
        return None

def validate_config(config):
    """Valida la estructura básica de la configuración"""
    required_sections = ["entorno", "agente_linkedin"]
    for section in required_sections:
        if section not in config:
            logger.error(f"Sección requerida '{section}' no encontrada en la configuración")
            return False
    return True

def update_env_from_config(config):
    """Actualiza variables de entorno basadas en la configuración TOML"""
    env_updates = {}
    
    # Actualizar variables de entorno para LinkedIn
    if "agente_linkedin" in config:
        linkedin_config = config["agente_linkedin"]
        if "frecuencia" in linkedin_config:
            freq = linkedin_config["frecuencia"]
            if freq == "diaria":
                env_updates["UPDATE_FREQUENCY_LINKEDIN"] = "Daily 09:00"
            elif freq == "semanal":
                env_updates["UPDATE_FREQUENCY_LINKEDIN"] = "Monday 09:00"
    
    # Actualizar variables de entorno para Finanzas
    if "agente_finanzas" in config:
        finanzas_config = config["agente_finanzas"]
        if "frecuencia" in finanzas_config:
            freq = finanzas_config["frecuencia"]
            if freq == "mensual":
                env_updates["UPDATE_FREQUENCY_FINANZAS"] = "1 * * 07:00"
    
    # Actualizar variables de entorno para Auto Mejora
    if "agente_auto_mejora" in config:
        auto_mejora_config = config["agente_auto_mejora"]
        if "frecuencia" in auto_mejora_config:
            freq = auto_mejora_config["frecuencia"]
            if freq == "semanal":
                env_updates["UPDATE_FREQUENCY_AUTOMEJORA"] = "Sunday 22:00"
    
    # Actualizar variables de entorno para Estrategia
    if "agente_estrategia" in config:
        estrategia_config = config["agente_estrategia"]
        if "frecuencia" in estrategia_config:
            freq = estrategia_config["frecuencia"]
            if freq == "por demanda":
                env_updates["UPDATE_FREQUENCY_ESTRATEGIA"] = "on-demand"
    
    # Actualizar entorno
    for key, value in env_updates.items():
        os.environ[key] = value
        logger.info(f"Actualizada variable de entorno: {key}={value}")
    
    return env_updates

def register_agents_in_system(config):
    """Registra los agentes en el sistema TalentekIA"""
    try:
        # Importar el módulo de gestión de agentes
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from src.agents.agent_manager import AgentManager
        
        manager = AgentManager()
        available_agents = manager.get_available_agents()
        
        logger.info(f"Agentes disponibles en el sistema: {', '.join(available_agents)}")
        
        # Verificar si los agentes de la configuración TOML están registrados
        toml_agents = []
        for key in config:
            if key.startswith("agente_"):
                agent_id = key.replace("agente_", "")
                toml_agents.append(agent_id)
        
        for agent_id in toml_agents:
            if agent_id in available_agents:
                logger.info(f"Agente '{agent_id}' ya está registrado en el sistema")
            else:
                logger.warning(f"Agente '{agent_id}' de la configuración TOML no está registrado en el sistema")
        
        return True
    except Exception as e:
        logger.error(f"Error al registrar agentes: {str(e)}")
        return False

def main():
    """Función principal"""
    print_banner()
    
    # Determinar la ruta del archivo de configuración TOML
    config_path = Path("talentek_agentes_config.toml")
    if not config_path.exists():
        logger.error(f"Archivo de configuración no encontrado: {config_path}")
        sys.exit(1)
    
    # Cargar la configuración
    config = load_toml_config(config_path)
    if config is None:
        sys.exit(1)
    
    # Validar la configuración
    if not validate_config(config):
        logger.error("La configuración TOML no es válida")
        sys.exit(1)
    
    # Mostrar información del entorno
    if "entorno" in config:
        entorno = config["entorno"]
        print(f"\nEntorno: {entorno.get('nombre', 'No especificado')}")
        print(f"Chip: {entorno.get('chip', 'No especificado')}")
        print(f"Soporte Mac: {'Sí' if entorno.get('soporte_mac', False) else 'No'}")
    
    # Mostrar información de personalización
    if "personalizacion" in config:
        pers = config["personalizacion"]
        print(f"\nUsuario: {pers.get('usuario', 'No especificado')}")
        print(f"Objetivo: {pers.get('objetivo', 'No especificado')}")
    
    # Mostrar agentes configurados
    print("\nAgentes configurados:")
    for key, value in config.items():
        if key.startswith("agente_"):
            print(f"  - {value.get('nombre', key)}: {value.get('descripcion', 'Sin descripción')}")
    
    # Actualizar variables de entorno
    print("\nActualizando configuración del sistema...")
    env_updates = update_env_from_config(config)
    
    # Registrar agentes en el sistema
    print("\nVerificando registro de agentes...")
    register_agents_in_system(config)
    
    print("\n✅ Configuración TOML cargada y procesada correctamente")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        sys.exit(1)