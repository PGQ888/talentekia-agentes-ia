#!/usr/bin/env python3
"""
Script unificado para el sistema de auto-mejora personalizado de Pablo Giráldez.
Este script combina las funcionalidades de análisis, programación y sincronización
en un único comando fácil de usar.
"""

import os
import sys
import argparse
import subprocess
import logging
import datetime
import json
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'talentek_auto_improve.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('talentek_auto_improve')

# Configuración
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "auto_improvement_config.json")
AUTO_IMPROVEMENT_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "auto_improvement.py")
SCHEDULE_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "schedule_auto_improvement.py")
GIT_SYNC_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "git_sync_improvements.py")

def load_config():
    """Carga la configuración del sistema de auto-mejora."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def run_analysis(args):
    """Ejecuta el análisis de auto-mejora."""
    cmd = [sys.executable, AUTO_IMPROVEMENT_SCRIPT]
    
    # Verificar si los atributos existen antes de usarlos
    if hasattr(args, 'no_report') and args.no_report:
        cmd.append("--no-report")
    if hasattr(args, 'no_email') and args.no_email:
        cmd.append("--no-email")
    
    try:
        result = subprocess.run(cmd, check=True)
        logger.info("Análisis completado exitosamente.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar análisis: {str(e)}")
        return False

def schedule_execution(args):
    """Programa la ejecución automática."""
    cmd = [sys.executable, SCHEDULE_SCRIPT]
    
    # Verificar si los atributos existen antes de usarlos
    if hasattr(args, 'frequency') and args.frequency:
        cmd.extend(["--frequency", args.frequency])
    if hasattr(args, 'remove') and args.remove:
        cmd.append("--remove")
    if hasattr(args, 'run_now') and args.run_now:
        cmd.append("--run-now")
    
    try:
        result = subprocess.run(cmd, check=True)
        logger.info("Programación configurada exitosamente.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al programar ejecución: {str(e)}")
        return False

def sync_with_github(args):
    """Sincroniza las mejoras con GitHub."""
    cmd = [sys.executable, GIT_SYNC_SCRIPT]
    
    # Verificar si los atributos existen antes de usarlos
    if hasattr(args, 'setup') and args.setup:
        cmd.append("--setup")
    if hasattr(args, 'force') and args.force:
        cmd.append("--force")
    if hasattr(args, 'no_push') and args.no_push:
        cmd.append("--no-push")
    if hasattr(args, 'no_pr') and args.no_pr:
        cmd.append("--no-pr")
    
    try:
        result = subprocess.run(cmd, check=True)
        logger.info("Sincronización con GitHub completada.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al sincronizar con GitHub: {str(e)}")
        return False

def show_status():
    """Muestra el estado actual del sistema de auto-mejora."""
    config = load_config()
    
    print("\n=== Estado del Sistema de Auto-Mejora de Pablo Giráldez ===\n")
    
    # Verificar si hay reportes recientes
    reports_dir = os.path.join(PROJECT_ROOT, "reports")
    report_file = os.path.join(reports_dir, "auto_improvement_report.md")
    
    if os.path.exists(report_file):
        report_time = datetime.datetime.fromtimestamp(os.path.getmtime(report_file))
        print(f"📊 Último reporte: {report_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Mostrar resumen del último reporte
        try:
            with open(report_file, 'r') as f:
                content = f.read()
                if "## Resumen de Mejoras Sugeridas" in content:
                    summary = content.split("## Resumen de Mejoras Sugeridas")[1].split("##")[0].strip()
                    print("\n📝 Resumen del último reporte:")
                    print(summary)
        except Exception as e:
            logger.error(f"Error al leer reporte: {str(e)}")
    else:
        print("❌ No se encontraron reportes anteriores.")
    
    # Mostrar configuración actual
    print("\n⚙️ Configuración actual:")
    print(f"   - Frecuencia de ejecución: {config.get('run_frequency', 'weekly')}")
    print(f"   - Notificaciones por email: {config.get('email_notifications', False)}")
    print(f"   - Aplicar correcciones automáticamente: {config.get('auto_apply_safe_fixes', False)}")
    
    # Mostrar áreas de enfoque
    if "focus_areas" in config:
        print("\n🎯 Áreas de enfoque:")
        for area in config.get("focus_areas", []):
            priority = "alta" if config.get("project_priorities", {}).get(area) == "high" else "media"
            print(f"   - {area.capitalize()} (prioridad {priority})")
    
    print("\n=== Comandos disponibles ===\n")
    print("python scripts/talentek_auto_improve.py analyze   # Ejecutar análisis")
    print("python scripts/talentek_auto_improve.py schedule  # Programar ejecución")
    print("python scripts/talentek_auto_improve.py sync      # Sincronizar con GitHub")
    print("python scripts/talentek_auto_improve.py status    # Mostrar este estado")
    print("python scripts/talentek_auto_improve.py all       # Ejecutar todo el proceso\n")

def main():
    """Función principal."""
    # Crear directorios necesarios
    os.makedirs(os.path.join(PROJECT_ROOT, "logs"), exist_ok=True)
    
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description="Sistema de auto-mejora personalizado para Pablo Giráldez")
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # Comando: analyze
    analyze_parser = subparsers.add_parser("analyze", help="Ejecutar análisis de auto-mejora")
    analyze_parser.add_argument("--no-report", action="store_true", help="No generar reporte")
    analyze_parser.add_argument("--no-email", action="store_true", help="No enviar notificación por correo")
    
    # Comando: schedule
    schedule_parser = subparsers.add_parser("schedule", help="Programar ejecución automática")
    schedule_parser.add_argument("--frequency", choices=["daily", "weekly", "monthly"], 
                              help="Frecuencia de ejecución")
    schedule_parser.add_argument("--remove", action="store_true", help="Eliminar tarea programada")
    schedule_parser.add_argument("--run-now", action="store_true", help="Ejecutar ahora")
    
    # Comando: sync
    sync_parser = subparsers.add_parser("sync", help="Sincronizar mejoras con GitHub")
    sync_parser.add_argument("--setup", action="store_true", help="Configurar token de GitHub")
    sync_parser.add_argument("--force", action="store_true", help="Forzar sincronización")
    sync_parser.add_argument("--no-push", action="store_true", help="No enviar cambios")
    sync_parser.add_argument("--no-pr", action="store_true", help="No crear pull request")
    
    # Comando: status
    subparsers.add_parser("status", help="Mostrar estado del sistema")
    
    # Comando: all
    all_parser = subparsers.add_parser("all", help="Ejecutar todo el proceso")
    all_parser.add_argument("--no-email", action="store_true", help="No enviar notificación por correo")
    all_parser.add_argument("--no-pr", action="store_true", help="No crear pull request")
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Ejecutar comando correspondiente
    if args.command == "analyze":
        run_analysis(args)
    elif args.command == "schedule":
        schedule_execution(args)
    elif args.command == "sync":
        sync_with_github(args)
    elif args.command == "status":
        show_status()
    elif args.command == "all":
        # Ejecutar todo el proceso
        print("🚀 Iniciando proceso completo de auto-mejora...")
        
        # Crear un objeto Namespace con los atributos necesarios para run_analysis
        analyze_args = argparse.Namespace()
        if hasattr(args, 'no_email'):
            analyze_args.no_email = args.no_email
        else:
            analyze_args.no_email = False
        analyze_args.no_report = False
        
        # Ejecutar análisis
        if run_analysis(analyze_args):
            # Sincronizar con GitHub si el análisis fue exitoso
            sync_args = argparse.Namespace()
            sync_args.setup = False
            sync_args.force = False
            sync_args.no_push = False
            if hasattr(args, 'no_pr'):
                sync_args.no_pr = args.no_pr
            else:
                sync_args.no_pr = False
            
            sync_with_github(sync_args)
        
        print("✅ Proceso completo finalizado.")
    else:
        # Si no se especifica comando, mostrar estado
        show_status()

if __name__ == "__main__":
    main()