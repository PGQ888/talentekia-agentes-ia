#!/usr/bin/env python3
"""
Script para sincronización automática con GitHub y automejora del sistema
Utiliza las variables de entorno configuradas en el archivo .env
"""
import os
import subprocess
import time
import logging
from datetime import datetime
import schedule
from dotenv import load_dotenv
import sys
import platform

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

# Cargar variables de entorno desde el archivo .env
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_dir, '.env')

if os.path.exists(env_path):
    logger.info(f"Cargando variables de entorno desde {env_path}")
    load_dotenv(env_path)
else:
    logger.error(f"Archivo .env no encontrado en {env_path}")
    sys.exit(1)

# Configuración desde variables de entorno
AUTO_SYNC = os.getenv("AUTO_SYNC", "false").lower() == "true"
SYNC_INTERVAL_HOURS = int(os.getenv("SYNC_INTERVAL_HOURS", "12"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_URL = os.getenv("REPO_URL", "https://github.com/PGQ888/talentekia-agentes-ia.git")
MAC_MODEL = os.getenv("MAC_MODEL", "")
USER_NAME = os.getenv("USER_NAME", "Usuario")

# Verificar configuración
logger.info(f"Configuración cargada:")
logger.info(f"- Usuario: {USER_NAME}")
logger.info(f"- Sistema: {platform.system()} {platform.release()}")
logger.info(f"- Modelo Mac: {MAC_MODEL}")
logger.info(f"- Auto sincronización: {'Activada' if AUTO_SYNC else 'Desactivada'}")
logger.info(f"- Intervalo de sincronización: {SYNC_INTERVAL_HOURS} horas")
logger.info(f"- Repositorio: {REPO_URL}")
logger.info(f"- Token GitHub configurado: {'Sí' if GITHUB_TOKEN else 'No'}")

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
        
        # Añadir todos los cambios (excepto .env que contiene información sensible)
        success, output = run_command("git add --all -- ':!.env'", cwd=project_dir)
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
        logger.info("URL remota configurada con token de autenticación")
    else:
        logger.warning("No se encontró token de GitHub. La sincronización podría fallar si se requiere autenticación.")
    
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
    
    # Directorio del proyecto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Actualizar dependencias
    requirements_file = os.path.join(project_dir, "requirements.txt")
    if os.path.exists(requirements_file):
        logger.info("Actualizando dependencias...")
        success, output = run_command("pip install -U -r requirements.txt", cwd=project_dir)
        if not success:
            logger.error(f"Error al actualizar dependencias: {output}")
        else:
            logger.info("Dependencias actualizadas correctamente")
    
    # 2. Verificar y crear directorios necesarios
    for dir_name in ["data", "logs", "docs", "config"]:
        dir_path = os.path.join(project_dir, dir_name)
        if not os.path.exists(dir_path):
            logger.info(f"Creando directorio: {dir_name}")
            os.makedirs(dir_path, exist_ok=True)
    
    # 3. Verificar permisos de los scripts
    for script in ["start_auto_sync.sh", "stop_auto_sync.sh"]:
        script_path = os.path.join(project_dir, script)
        if os.path.exists(script_path):
            logger.info(f"Verificando permisos de {script}")
            run_command(f"chmod +x {script_path}", cwd=project_dir)
    
    # 4. Optimizar para el modelo de Mac especificado
    if MAC_MODEL:
        logger.info(f"Optimizando para Mac {MAC_MODEL}...")
        # Aquí podrías añadir optimizaciones específicas para el modelo de Mac
    
    logger.info("Proceso de automejora completado")

def check_system_health():
    """Verifica el estado del sistema"""
    logger.info("Verificando estado del sistema...")
    
    # Verificar espacio en disco
    success, output = run_command("df -h .")
    if success:
        logger.info(f"Espacio en disco: {output.strip()}")
    
    # Verificar uso de memoria
    success, output = run_command("ps -o pid,%cpu,%mem,command -p $$")
    if success:
        logger.info(f"Uso de recursos: {output.strip()}")
    
    # Verificar conexión a internet
    success, output = run_command("ping -c 1 github.com")
    if success:
        logger.info("Conexión a internet: OK")
    else:
        logger.warning("Conexión a internet: Problemas detectados")
    
    logger.info("Verificación de estado del sistema completada")

def main():
    """Función principal"""
    logger.info(f"Iniciando servicio de sincronización automática para {USER_NAME}")
    
    if not AUTO_SYNC:
        logger.info("Sincronización automática desactivada en .env")
        logger.info("Para activarla, establece AUTO_SYNC=true en el archivo .env")
        return
    
    # Ejecutar funciones inmediatamente al inicio
    check_system_health()
    sync_with_github()
    auto_improve()
    
    # Programar tareas periódicas
    schedule.every(SYNC_INTERVAL_HOURS).hours.do(sync_with_github)
    schedule.every().monday.at("07:00").do(auto_improve)
    schedule.every().day.at("09:00").do(check_system_health)
    
    logger.info(f"Tareas programadas:")
    logger.info(f"- Sincronización: cada {SYNC_INTERVAL_HOURS} horas")
    logger.info(f"- Automejora: lunes a las 07:00")
    logger.info(f"- Verificación de salud: diariamente a las 09:00")
    
    # Bucle principal
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
    except KeyboardInterrupt:
        logger.info("Servicio detenido manualmente")
    except Exception as e:
        logger.error(f"Error en el bucle principal: {str(e)}")
        raise

if __name__ == "__main__":
    main()