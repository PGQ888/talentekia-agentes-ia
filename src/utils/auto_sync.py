#!/usr/bin/env python3
"""
Script de sincronización automática para el sistema Talentek IA.
Este script se ejecuta como un servicio en segundo plano y se encarga de:
1. Sincronizar el repositorio local con el remoto
2. Ejecutar los agentes según su programación
"""

import os
import sys
import time
import json
import subprocess
import schedule
from datetime import datetime
import logging
# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sync_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("auto_sync")

# Añadir los directorios necesarios al path de Python
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_dir = os.path.join(project_dir, "scripts")
agents_dir = os.path.join(project_dir, "agents")
sys.path.append(scripts_dir)
sys.path.append(agents_dir)

# Importar módulos necesarios
try:
    from scripts.env_loader import env
    GITHUB_TOKEN = env.get("GITHUB_TOKEN", "")
    GITHUB_REPO = env.get("GITHUB_REPO", "")
except ImportError:
    GITHUB_TOKEN = ""
    GITHUB_REPO = ""
    logger.error("No se pudo cargar el módulo de entorno")
try:
    from agents.config import get_all_agents
except ImportError:
    logger.error("No se pudo cargar la configuración de agentes")
    def get_all_agents():
        return {}

def ejecutar_comando(comando):
    """Ejecuta un comando del sistema y devuelve el resultado"""
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        return resultado.returncode == 0, resultado.stdout
    except Exception as e:
        return False, str(e)

def sincronizar_repositorio():
    """Sincroniza el repositorio local con el remoto"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        logger.warning("No se ha configurado el token de GitHub o el repositorio")
        return False

    logger.info("Sincronizando repositorio...")
    
    # Configurar credenciales
    os.environ["GIT_ASKPASS"] = "echo"
    os.environ["GIT_USERNAME"] = "auto-sync"
    os.environ["GIT_PASSWORD"] = GITHUB_TOKEN
    
    # Pull cambios del remoto
    success, output = ejecutar_comando("git pull origin main")
    if not success:
        logger.error(f"Error al hacer pull: {output}")
        return False
    
    # Commit cambios locales
    ejecutar_comando("git add .")
    ejecutar_comando('git commit -m "Auto-sync: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '"')
    
    # Push cambios al remoto
    success, output = ejecutar_comando("git push origin main")
    if not success:
        logger.error(f"Error al hacer push: {output}")
        return False
    
    logger.info("Sincronización completada")
    return True

def ejecutar_agente(agent_id):
    """Ejecuta un agente específico"""
    logger.info(f"Ejecutando agente {agent_id}...")
    
    agent_script = os.path.join(agents_dir, f"{agent_id}_pro.py")
    if not os.path.exists(agent_script):
        agent_script = os.path.join(agents_dir, f"{agent_id}_agent.py")
    
    if os.path.exists(agent_script):
        success, output = ejecutar_comando(f"python {agent_script}")
        if success:
            logger.info(f"Agente {agent_id} ejecutado correctamente")
        else:
            logger.error(f"Error al ejecutar el agente {agent_id}: {output}")
        return success
    else:
        logger.error(f"Script del agente {agent_id} no encontrado")
        return False

def programar_tareas():
    """Programa las tareas de los agentes según su configuración"""
    logger.info("Programando tareas...")
    
    # Limpiar tareas existentes
    schedule.clear()
    
    # Programar sincronización cada hora
    schedule.every(1).hours.do(sincronizar_repositorio)
    
    # Obtener todos los agentes y programar sus tareas
    agents = get_all_agents()
    for agent_id, agent_data in agents.items():
        update_frequency = agent_data.get("update_frequency", "").lower()
        
        if "daily" in update_frequency:
            # Formato: "Daily HH:MM"
            try:
                time_part = update_frequency.split(" ")[1]
                hour, minute = time_part.split(":")
                schedule.every().day.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                logger.info(f"Agente {agent_id} programado diariamente a las {hour}:{minute}")
            except:
                logger.error(f"Formato de frecuencia incorrecto para {agent_id}: {update_frequency}")
        
        elif any(day in update_frequency.lower() for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
            # Formato: "DayOfWeek HH:MM"
            try:
                day_part = update_frequency.split(" ")[0].lower()
                time_part = update_frequency.split(" ")[1]
                hour, minute = time_part.split(":")
                
                if "monday" in day_part:
                    schedule.every().monday.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                elif "tuesday" in day_part:
                    schedule.every().tuesday.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                elif "wednesday" in day_part:
                    schedule.every().wednesday.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                elif "thursday" in day_part:
                    schedule.every().thursday.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                elif "friday" in day_part:
                    schedule.every().friday.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                elif "saturday" in day_part:
                    schedule.every().saturday.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                elif "sunday" in day_part:
                    schedule.every().sunday.at(f"{hour}:{minute}").do(ejecutar_agente, agent_id)
                
                logger.info(f"Agente {agent_id} programado para {day_part} a las {hour}:{minute}")
            except:
                logger.error(f"Formato de frecuencia incorrecto para {agent_id}: {update_frequency}")
def main():
    """Función principal del servicio de sincronización"""
    logger.info("Iniciando servicio de sincronización automática...")
    
    # Programar tareas iniciales
    programar_tareas()
    
    # Bucle principal
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Comprobar cada minuto
        except KeyboardInterrupt:
            logger.info("Servicio de sincronización detenido manualmente")
            break
        except Exception as e:
            logger.error(f"Error en el servicio de sincronización: {str(e)}")
            time.sleep(300)  # Esperar 5 minutos antes de reintentar

if __name__ == "__main__":
    main()
