#!/usr/bin/env python3
"""
Script de sincronización con GitHub para TalentekIA
Este script gestiona la sincronización automática del repositorio con GitHub
"""

import os
import sys
import subprocess
import time
import logging
import toml
from datetime import datetime
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"logs/github_sync_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)

logger = logging.getLogger("TalentekIA-GitHub-Sync")

def load_config():
    """Carga la configuración desde el archivo TOML"""
    try:
        config_path = Path("config/talentek_config.toml")
        if not config_path.exists():
            logger.error(f"Archivo de configuración no encontrado: {config_path}")
            return None
        
        config = toml.load(config_path)
        return config.get("sincronizacion", {})
    except Exception as e:
        logger.error(f"Error al cargar la configuración: {str(e)}")
        return None

def run_command(command):
    """Ejecuta un comando en la terminal y devuelve el resultado"""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def check_git_status():
    """Verifica el estado actual del repositorio Git"""
    logger.info("Verificando estado de Git...")
    
    # Verificar que estamos en un repositorio Git
    success, output = run_command("git rev-parse --is-inside-work-tree")
    if not success or output != "true":
        logger.error("No estamos en un repositorio Git válido")
        return False, "No es un repositorio Git"
    
    # Verificar rama actual
    success, branch = run_command("git branch --show-current")
    if not success:
        logger.error(f"Error al obtener la rama actual: {branch}")
        return False, branch
    
    # Verificar cambios pendientes
    success, status = run_command("git status --porcelain")
    has_changes = bool(status)
    
    return True, {
        "branch": branch,
        "has_changes": has_changes,
        "status": status
    }

def commit_changes(auto_commit=True):
    """Realiza commit de los cambios pendientes"""
    if not auto_commit:
        logger.info("Auto-commit desactivado, omitiendo commit")
        return True, "Auto-commit desactivado"
    
    logger.info("Realizando commit de cambios...")
    
    # Añadir todos los cambios
    success, output = run_command("git add .")
    if not success:
        logger.error(f"Error al añadir cambios: {output}")
        return False, output
    
    # Verificar si hay cambios para hacer commit
    success, status = run_command("git status --porcelain")
    if not status:
        logger.info("No hay cambios para hacer commit")
        return True, "No hay cambios"
    
    # Realizar commit con timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Actualización automática: {timestamp}"
    success, output = run_command(f'git commit -m "{commit_msg}"')
    if not success:
        logger.error(f"Error al hacer commit: {output}")
        return False, output
    
    logger.info(f"Commit realizado: {commit_msg}")
    return True, output

def sync_with_remote(repository=None):
    """Sincroniza con el repositorio remoto"""
    logger.info("Sincronizando con repositorio remoto...")
    
    # Verificar si existe un remoto configurado
    success, remote = run_command("git remote -v")
    if not success or not remote:
        if not repository:
            logger.error("No hay repositorio remoto configurado")
            return False, "No hay repositorio remoto"
        
        # Configurar repositorio remoto si se proporciona
        logger.info(f"Configurando repositorio remoto: {repository}")
        success, output = run_command(f"git remote add origin {repository}")
        if not success:
            logger.error(f"Error al configurar repositorio remoto: {output}")
            return False, output
    
    # Obtener cambios del remoto
    logger.info("Obteniendo cambios del repositorio remoto...")
    success, output = run_command("git pull --no-rebase")
    if not success:
        if "CONFLICT" in output:
            logger.warning("Conflictos detectados durante el pull")
            # Aquí podrías implementar una estrategia para resolver conflictos
            # Por ahora, simplemente abortamos el merge
            run_command("git merge --abort")
            return False, "Conflictos detectados"
        else:
            logger.error(f"Error al obtener cambios: {output}")
            return False, output
    
    # Enviar cambios al remoto
    logger.info("Enviando cambios al repositorio remoto...")
    success, output = run_command("git push origin")
    if not success:
        logger.error(f"Error al enviar cambios: {output}")
        return False, output
    
    logger.info("Sincronización completada con éxito")
    return True, output

def sync_repository():
    """Función principal para sincronizar el repositorio"""
    logger.info("Iniciando sincronización del repositorio...")
    
    # Cargar configuración
    config = load_config()
    if not config:
        return False
    
    # Verificar si la sincronización está activada
    if not config.get("activada", False):
        logger.info("Sincronización desactivada en la configuración")
        return True
    
    # Verificar estado de Git
    success, status = check_git_status()
    if not success:
        return False
    
    # Realizar commit si hay cambios
    if status["has_changes"]:
        success, output = commit_changes(config.get("auto_commit", True))
        if not success:
            return False
    
    # Sincronizar con remoto
    success, output = sync_with_remote(config.get("repositorio"))
    if not success:
        return False
    
    return True

def start_sync_daemon(interval=3600):
    """Inicia un demonio de sincronización que se ejecuta periódicamente"""
    logger.info(f"Iniciando demonio de sincronización (intervalo: {interval} segundos)")
    
    try:
        while True:
            success = sync_repository()
            if success:
                logger.info(f"Sincronización exitosa. Esperando {interval} segundos para la próxima sincronización...")
            else:
                logger.error(f"Error en la sincronización. Reintentando en {interval} segundos...")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Demonio de sincronización detenido por el usuario")
    except Exception as e:
        logger.error(f"Error en el demonio de sincronización: {str(e)}")
        return False
    
    return True

def main():
    """Función principal"""
    print(f"TalentekIA - Sincronización con GitHub - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        # Cargar configuración
        config = load_config()
        if not config:
            sys.exit(1)
        
        # Iniciar demonio de sincronización
        interval = config.get("intervalo", 3600)  # Por defecto, cada hora
        success = start_sync_daemon(interval)
    else:
        # Ejecutar una sincronización única
        success = sync_repository()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()