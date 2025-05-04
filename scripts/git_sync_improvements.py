#!/usr/bin/env python3
"""
Script para sincronizar las mejoras del sistema de auto-mejora con GitHub.
Crea una rama, hace commit de los cambios y opcionalmente crea un pull request.
"""

import os
import sys
import json
import argparse
import subprocess
import getpass
import datetime
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'git_sync.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('git_sync')

# Configuración
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "git_sync_config.json")
REPORT_FILE = os.path.join(PROJECT_ROOT, "reports", "auto_improvement_report.md")

def load_config():
    """Carga la configuración de sincronización con GitHub."""
    config_dir = os.path.dirname(CONFIG_FILE)
    os.makedirs(config_dir, exist_ok=True)
    
    default_config = {
        "github_token": "",
        "repo_owner": "PGQ888",
        "repo_name": "talentekia-agentes-ia",
        "create_pull_requests": True,
        "default_branch": "main",
        "auto_merge": False,
        "commit_message_prefix": "[Auto-mejora] ",
        "labels_for_pr": ["auto-improvement", "maintenance"]
    }
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            # Asegurar que todas las claves existan
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
        else:
            config = default_config
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, indent=2, fp=f)
            logger.info(f"Archivo de configuración creado en {CONFIG_FILE}")
        
        return config
    except Exception as e:
        logger.error(f"Error al cargar configuración: {str(e)}")
        return default_config

def setup_github_token():
    """Configura el token de acceso personal de GitHub."""
    config = load_config()
    
    print("Configuración del token de GitHub para sincronización automática")
    print("---------------------------------------------------------------")
    print("Necesitas crear un token de acceso personal en GitHub con permisos 'repo'")
    print("Puedes crear uno en: https://github.com/settings/tokens")
    print()
    
    token = getpass.getpass("Ingresa tu token de acceso personal de GitHub: ")
    
    if token:
        config["github_token"] = token
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, indent=2, fp=f)
        print("✅ Token de GitHub configurado correctamente.")
    else:
        print("❌ No se ingresó ningún token.")

def check_git_repo():
    """Verifica si el directorio actual es un repositorio Git."""
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_for_changes():
    """Verifica si hay cambios en el repositorio."""
    try:
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, check=True)
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al verificar cambios: {str(e)}")
        return False

def create_branch():
    """Crea una nueva rama para las mejoras."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    branch_name = f"auto-improvement-{timestamp}"
    
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        logger.info(f"Rama creada: {branch_name}")
        return branch_name
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al crear rama: {str(e)}")
        return None

def commit_changes(commit_message_prefix):
    """Hace commit de los cambios."""
    try:
        # Añadir todos los archivos
        subprocess.run(["git", "add", "."], check=True)
        
        # Obtener resumen del reporte para el mensaje de commit
        summary = "Mejoras automáticas"
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, 'r') as f:
                content = f.read()
                # Buscar la sección de resumen
                if "## Resumen de Mejoras Sugeridas" in content:
                    summary_section = content.split("## Resumen de Mejoras Sugeridas")[1]
                    summary_lines = [line for line in summary_section.splitlines() if line.strip()]
                    if summary_lines:
                        summary = "\n".join(summary_lines[:3])  # Tomar las primeras 3 líneas
        
        # Hacer commit
        commit_message = f"{commit_message_prefix}Mejoras automáticas\n\n{summary}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        logger.info("Cambios confirmados")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al hacer commit: {str(e)}")
        return False

def push_changes(branch_name):
    """Envía los cambios al repositorio remoto."""
    try:
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
        logger.info(f"Cambios enviados a la rama {branch_name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al enviar cambios: {str(e)}")
        return False

def create_pull_request(config, branch_name):
    """Crea un pull request en GitHub."""
    token = config.get("github_token")
    repo_owner = config.get("repo_owner")
    repo_name = config.get("repo_name")
    default_branch = config.get("default_branch", "main")
    labels = config.get("labels_for_pr", [])
    
    if not token:
        logger.error("No se encontró token de GitHub. Usa --setup para configurarlo.")
        return False
    
    # Obtener resumen del reporte para el título y descripción del PR
    title = f"[Auto-mejora] Mejoras automáticas ({datetime.datetime.now().strftime('%Y-%m-%d')})"
    body = "Este pull request contiene mejoras automáticas detectadas por el sistema de auto-mejora."
    
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r') as f:
            content = f.read()
            body += "\n\n## Resumen del reporte\n\n"
            
            # Añadir resumen si existe
            if "## Resumen de Mejoras Sugeridas" in content:
                summary_section = content.split("## Resumen de Mejoras Sugeridas")[1]
                summary_lines = []
                for line in summary_section.splitlines():
                    if line.strip() and not line.startswith("#"):
                        summary_lines.append(line)
                    if line.startswith("##"):  # Nueva sección
                        break
                if summary_lines:
                    body += "\n".join(summary_lines)
    
    # Crear pull request usando la API de GitHub
    try:
        import requests
        
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "title": title,
            "body": body,
            "head": branch_name,
            "base": default_branch
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            pr_data = response.json()
            pr_number = pr_data["number"]
            pr_url = pr_data["html_url"]
            logger.info(f"Pull request creado: #{pr_number} - {pr_url}")
            
            # Añadir etiquetas si existen
            if labels:
                labels_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/labels"
                requests.post(labels_url, headers=headers, json=labels)
                logger.info(f"Etiquetas añadidas al PR: {', '.join(labels)}")
            
            return True
        else:
            logger.error(f"Error al crear PR: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error al crear pull request: {str(e)}")
        return False

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Sincroniza las mejoras con GitHub.")
    parser.add_argument("--setup", action="store_true", 
                        help="Configura el token de GitHub")
    parser.add_argument("--force", action="store_true", 
                        help="Fuerza la sincronización aunque no haya cambios detectados")
    parser.add_argument("--no-push", action="store_true", 
                        help="No enviar cambios al repositorio remoto")
    parser.add_argument("--no-pr", action="store_true", 
                        help="No crear pull request")
    
    args = parser.parse_args()
    
    # Crear directorio de logs si no existe
    os.makedirs(os.path.join(PROJECT_ROOT, "logs"), exist_ok=True)
    
    # Cargar configuración
    config = load_config()
    
    # Configurar token si se solicitó
    if args.setup:
        setup_github_token()
        return
    
    # Verificar si es un repositorio Git
    if not check_git_repo():
        logger.error("El directorio actual no es un repositorio Git.")
        return
    
    # Verificar si hay cambios
    has_changes = check_for_changes()
    if not has_changes and not args.force:
        logger.info("No hay cambios para sincronizar.")
        return
    
    # Crear rama
    branch_name = create_branch()
    if not branch_name:
        return
    
    # Hacer commit de los cambios
    if not commit_changes(config.get("commit_message_prefix", "[Auto-mejora] ")):
        return
    
    # Enviar cambios si no se desactivó
    if not args.no_push:
        if not push_changes(branch_name):
            return
    
    # Crear pull request si está habilitado y no se desactivó
    if config.get("create_pull_requests", True) and not args.no_pr and not args.no_push:
        create_pull_request(config, branch_name)
    
    logger.info("Sincronización completada.")

if __name__ == "__main__":
    main()