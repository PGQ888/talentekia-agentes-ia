#!/usr/bin/env python3
"""
Script para sincronización automática con GitHub y automejora del sistema
"""
import os
import subprocess
import time
import logging
from datetime import datetime
import schedule
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auto_sync.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TalentekIA-AutoSync")

# Cargar variables de entorno
load_dotenv()

# Configuración
AUTO_SYNC = os.getenv("AUTO_SYNC", "false").lower() == "true"
SYNC_INTERVAL_HOURS = int(os.getenv("SYNC_INTERVAL_HOURS", "24"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_URL = os.getenv("REPO_URL", "https://github.com/PGQ888/talentekia-agentes-ia.git")

def run_command(command, cwd=None):
    """Ejecuta un comando y devuelve el resultado"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def sync_with_github():
    """Sincroniza el repositorio local con GitHub"""
    logger.info("Iniciando sincronización con GitHub...")
    
    # Directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Verificar si hay cambios para commit
    success, output = run_command("git status --porcelain", cwd=project_dir)
    if not success:
        logger.error(f"Error al verificar estado del repositorio: {output}")
        return
    
    if output.strip():
        # Hay cambios, hacer commit
        logger.info("Detectados cambios locales, preparando commit...")
        
        # Añadir todos los cambios
        success, output = run_command("git add .", cwd=project_dir)
        if not success:
            logger.error(f"Error al añadir cambios: {output}")
            return
        
        # Crear commit con timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"Actualización automática - {timestamp}"
        success, output = run_command(f'git commit -m "{commit_msg}"', cwd=project_dir)
        if not success:
            logger.error(f"Error al crear commit: {output}")
            return
        
        logger.info(f"Commit creado: {commit_msg}")
    else:
        logger.info("No hay cambios locales para commit")
    
    # Configurar credenciales para GitHub si hay token disponible
    if GITHUB_TOKEN:
        # Usar el token para autenticación
        repo_url_with_token = REPO_URL.replace("https://", f"https://{GITHUB_TOKEN}@")
        success, output = run_command(f"git remote set-url origin {repo_url_with_token}", cwd=project_dir)
        if not success:
            logger.error(f"Error al configurar URL remota: {output}")
            return
    
    # Pull para obtener cambios remotos
    logger.info("Obteniendo cambios remotos...")
    success, output = run_command("git pull origin main --rebase", cwd=project_dir)
    if not success:
        logger.error(f"Error al hacer pull: {output}")
        # Intentar resolver conflictos automáticamente
        run_command("git rebase --abort", cwd=project_dir)
        logger.info("Rebase abortado, continuando con push")
    
    # Push para enviar cambios locales
    logger.info("Enviando cambios locales...")
    success, output = run_command("git push origin main", cwd=project_dir)
    if not success:
        logger.error(f"Error al hacer push: {output}")
        return
    
    logger.info("Sincronización con GitHub completada exitosamente")

def auto_improve():
    """Realiza mejoras automáticas en el sistema"""
    logger.info("Iniciando proceso de automejora...")
    
    # Aquí puedes implementar lógica para mejorar automáticamente el sistema
    # Por ejemplo:
    # 1. Analizar logs para detectar errores comunes
    # 2. Optimizar consultas o algoritmos
    # 3. Actualizar dependencias
    
    # Por ahora, solo actualizamos las dependencias
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    requirements_file = os.path.join(project_dir, "requirements.txt")
    
    if os.path.exists(requirements_file):
        logger.info("Actualizando dependencias...")
        success, output = run_command("pip install -U -r requirements.txt", cwd=project_dir)
        if not success:
            logger.error(f"Error al actualizar dependencias: {output}")
            return
        logger.info("Dependencias actualizadas correctamente")
    
    logger.info("Proceso de automejora completado")

def main():
    """Función principal"""
    logger.info("Iniciando servicio de sincronización automática")
    
    if not AUTO_SYNC:
        logger.info("Sincronización automática desactivada en .env")
        return
    
    # Ejecutar sincronización inmediatamente al inicio
    sync_with_github()
    auto_improve()
    
    # Programar sincronización periódica
    schedule.every(SYNC_INTERVAL_HOURS).hours.do(sync_with_github)
    schedule.every().monday.at("07:00").do(auto_improve)
    
    logger.info(f"Sincronización programada cada {SYNC_INTERVAL_HOURS} horas")
    logger.info("Automejora programada cada lunes a las 07:00")
    
    # Bucle principal
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto

if __name__ == "__main__":
    main()