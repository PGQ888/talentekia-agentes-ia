"""
Configuración de agentes para el sistema TalentekIA
Este módulo define los agentes disponibles y sus configuraciones
"""
import os
import json
from pathlib import Path

def get_all_agents():
    """Devuelve la configuración de todos los agentes"""
    agents = {
        "linkedin": {
            "name": "LinkedIn Pro",
            "icon": "🔍",
            "description": "Este agente escanea LinkedIn en busca de oportunidades de trabajo y candidatos potenciales.",
            "update_frequency": "Daily 09:00",
            "output_files": {
                "csv": "linkedin_ofertas.csv",
                "markdown": "linkedin_ofertas.md"
            }
        },
        "estrategia": {
            "name": "Estrategia Comercial",
            "icon": "📊",
            "description": "Este agente analiza tendencias del mercado y genera estrategias comerciales personalizadas.",
            "update_frequency": "Monday 08:00",
            "output_files": {
                "csv": "estrategia_comercial.csv",
                "markdown": "estrategia_comercial.md"
            }
        },
        "finanzas": {
            "name": "Finanzas Personales",
            "icon": "💵",
            "description": "Este agente analiza tus finanzas y te proporciona recomendaciones personalizadas.",
            "update_frequency": "Monday 07:00",
            "output_files": {
                "csv": "finanzas_personales.csv",
                "markdown": "finanzas_personales.md"
            }
        },
        "automejora": {
            "name": "Auto Mejora",
            "icon": "⚙️",
            "description": "Este agente analiza tu rendimiento y te proporciona recomendaciones para mejorar.",
            "update_frequency": "Monday 07:00",
            "output_files": {
                "csv": "auto_mejora.csv",
                "markdown": "auto_mejora.md"
            }
        }
    }
    
    return agents

def get_agent_config(agent_id):
    """Devuelve la configuración de un agente específico"""
    agents = get_all_agents()
    return agents.get(agent_id)

def save_agent_config(agent_id, config):
    """Guarda la configuración de un agente específico"""
    # En una implementación real, esto podría guardar en un archivo JSON
    # Por ahora, simplemente devolvemos True para simular éxito
    return True