"""
Configuración global para TalentekIA
Este módulo contiene la configuración centralizada del sistema
"""

import os
import json
from pathlib import Path

# Rutas principales
ROOT_DIR = Path(__file__).parent.parent.absolute()
DATA_DIR = os.path.join(ROOT_DIR, "data")
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")

# Archivo de configuración
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")

def load_config():
    """Carga la configuración desde el archivo settings.json"""
    if not os.path.exists(CONFIG_FILE):
        return create_default_config()
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return create_default_config()

def save_config(config):
    """Guarda la configuración en el archivo settings.json"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar la configuración: {e}")
        return False

def create_default_config():
    """Crea una configuración por defecto"""
    default_config = {
        "api_keys": {
            "openai": "",
            "anthropic": "",
            "huggingface": ""
        },
        "performance_mode": "balanced",
        "update_frequency": {
            "linkedin_agent": "daily",
            "estrategia_comercial": "weekly",
            "finanzas_personales": "monthly",
            "auto_mejora": "weekly"
        },
        "notifications": {
            "email": "",
            "enable_email": False,
            "enable_desktop": True
        },
        "agents": {
            "linkedin_agent": {
                "enabled": True,
                "description": "Analiza ofertas de empleo y tendencias del mercado laboral",
                "parameters": {
                    "max_jobs": 100,
                    "regions": ["España", "Remoto"],
                    "keywords": ["Python", "Data Science", "Machine Learning", "IA"]
                }
            },
            "estrategia_comercial": {
                "enabled": True,
                "description": "Asistente para desarrollo de estrategias de negocio",
                "parameters": {
                    "industry": "Tecnología",
                    "business_size": "PYME",
                    "focus_areas": ["Adquisición de clientes", "Retención", "Expansión"]
                }
            },
            "finanzas_personales": {
                "enabled": True,
                "description": "Gestión y optimización de finanzas personales",
                "parameters": {
                    "income_sources": ["Salario", "Inversiones"],
                    "expense_categories": ["Vivienda", "Alimentación", "Transporte", "Ocio"],
                    "investment_types": ["Acciones", "Fondos indexados", "Criptomonedas"]
                }
            },
            "auto_mejora": {
                "enabled": True,
                "description": "Asistente para desarrollo personal y profesional",
                "parameters": {
                    "focus_areas": ["Productividad", "Aprendizaje", "Bienestar"],
                    "track_habits": True,
                    "set_goals": True
                }
            }
        }
    }
    
    save_config(default_config)
    return default_config

# Cargar configuración al importar el módulo
CONFIG = load_config()

# Funciones de acceso a la configuración
def get_api_key(service):
    """Obtiene una clave API para un servicio específico"""
    return CONFIG.get("api_keys", {}).get(service, "")

def get_performance_mode():
    """Obtiene el modo de rendimiento configurado"""
    return CONFIG.get("performance_mode", "balanced")

def get_agent_config(agent_id):
    """Obtiene la configuración de un agente específico"""
    return CONFIG.get("agents", {}).get(agent_id, {})

def get_all_agents():
    """Obtiene la lista de todos los agentes configurados"""
    return [
        {
            "id": agent_id,
            "enabled": agent_config.get("enabled", False),
            "description": agent_config.get("description", ""),
            "update_frequency": CONFIG.get("update_frequency", {}).get(agent_id, "daily")
        }
        for agent_id, agent_config in CONFIG.get("agents", {}).items()
    ]

def update_agent_config(agent_id, config):
    """Actualiza la configuración de un agente específico"""
    if "agents" not in CONFIG:
        CONFIG["agents"] = {}
    
    CONFIG["agents"][agent_id] = config
    return save_config(CONFIG)