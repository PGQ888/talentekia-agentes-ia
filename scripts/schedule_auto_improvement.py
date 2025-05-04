#!/usr/bin/env python3
"""
Script para programar la ejecución automática del análisis de auto-mejora.
Soporta programación en macOS (launchd), Linux (crontab) y Windows (Task Scheduler).
"""

import os
import sys
import argparse
import platform
import subprocess
import datetime
import json
from pathlib import Path

# Configuración
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "auto_improvement_config.json")
AUTO_IMPROVEMENT_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "auto_improvement.py")

def load_config():
    """Carga la configuración del sistema de auto-mejora."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"run_frequency": "weekly"}

def get_frequency_in_seconds(frequency):
    """Convierte la frecuencia en segundos."""
    if frequency == "daily":
        return 86400  # 24 horas
    elif frequency == "weekly":
        return 604800  # 7 días
    elif frequency == "monthly":
        return 2592000  # 30 días
    else:
        return 604800  # Por defecto, semanal

def schedule_macos(frequency, remove=False):
    """Programa la tarea en macOS usando launchd."""
    plist_dir = os.path.expanduser("~/Library/LaunchAgents")
    plist_path = os.path.join(plist_dir, "com.talentekia.auto_improvement.plist")
    
    if remove:
        if os.path.exists(plist_path):
            try:
                subprocess.run(["launchctl", "unload", plist_path], check=True)
                os.remove(plist_path)
                print("✅ Tarea programada eliminada correctamente.")
            except Exception as e:
                print(f"❌ Error al eliminar la tarea programada: {str(e)}")
        else:
            print("ℹ️ No hay tarea programada para eliminar.")
        return
    
    # Crear directorio si no existe
    os.makedirs(plist_dir, exist_ok=True)
    
    # Obtener ruta absoluta del intérprete Python
    python_path = sys.executable
    
    # Crear archivo plist
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.talentekia.auto_improvement</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{AUTO_IMPROVEMENT_SCRIPT}</string>
    </array>
    <key>StartInterval</key>
    <integer>{get_frequency_in_seconds(frequency)}</integer>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>{os.path.join(PROJECT_ROOT, 'logs', 'auto_improvement_launchd.log')}</string>
    <key>StandardErrorPath</key>
    <string>{os.path.join(PROJECT_ROOT, 'logs', 'auto_improvement_launchd_error.log')}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    <key>WorkingDirectory</key>
    <string>{PROJECT_ROOT}</string>
</dict>
</plist>
"""
    
    try:
        # Escribir archivo plist
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        # Cargar tarea
        subprocess.run(["launchctl", "unload", plist_path], check=False, stderr=subprocess.DEVNULL)
        subprocess.run(["launchctl", "load", plist_path], check=True)
        
        print(f"✅ Tarea programada correctamente con frecuencia {frequency}.")
        print(f"   El script se ejecutará cada {get_frequency_in_seconds(frequency) // 3600} horas.")
        print(f"   Los logs se guardarán en {os.path.join(PROJECT_ROOT, 'logs')}.")
    except Exception as e:
        print(f"❌ Error al programar la tarea: {str(e)}")

def schedule_linux(frequency, remove=False):
    """Programa la tarea en Linux usando crontab."""
    # Obtener crontab actual
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current_crontab = result.stdout
    except Exception:
        current_crontab = ""
    
    # Identificador único para nuestra tarea
    task_marker = "# TalentekAI Auto-Improvement"
    
    # Eliminar tarea existente
    new_crontab = []
    for line in current_crontab.splitlines():
        if task_marker not in line:
            new_crontab.append(line)
    
    if remove:
        # Guardar crontab sin nuestra tarea
        with open("/tmp/crontab.tmp", "w") as f:
            f.write("\n".join(new_crontab) + "\n")
        
        try:
            subprocess.run(["crontab", "/tmp/crontab.tmp"], check=True)
            print("✅ Tarea programada eliminada correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar la tarea programada: {str(e)}")
        
        os.remove("/tmp/crontab.tmp")
        return
    
    # Configurar nueva tarea según la frecuencia
    python_path = sys.executable
    if frequency == "daily":
        cron_schedule = "0 0 * * *"  # A medianoche todos los días
    elif frequency == "weekly":
        cron_schedule = "0 0 * * 0"  # A medianoche cada domingo
    else:  # monthly
        cron_schedule = "0 0 1 * *"  # A medianoche el primer día del mes
    
    new_crontab.append(f"{cron_schedule} cd {PROJECT_ROOT} && {python_path} {AUTO_IMPROVEMENT_SCRIPT} {task_marker}")
    
    # Guardar nueva crontab
    with open("/tmp/crontab.tmp", "w") as f:
        f.write("\n".join(new_crontab) + "\n")
    
    try:
        subprocess.run(["crontab", "/tmp/crontab.tmp"], check=True)
        print(f"✅ Tarea programada correctamente con frecuencia {frequency}.")
        print(f"   Programación cron: {cron_schedule}")
    except Exception as e:
        print(f"❌ Error al programar la tarea: {str(e)}")
    
    os.remove("/tmp/crontab.tmp")

def schedule_windows(frequency, remove=False):
    """Programa la tarea en Windows usando Task Scheduler."""
    task_name = "TalentekAI_Auto_Improvement"
    
    if remove:
        try:
            subprocess.run(["schtasks", "/Delete", "/TN", task_name, "/F"], check=True)
            print("✅ Tarea programada eliminada correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar la tarea programada: {str(e)}")
        return
    
    # Configurar frecuencia
    if frequency == "daily":
        schedule_type = "/SC DAILY"
    elif frequency == "weekly":
        schedule_type = "/SC WEEKLY /D SUN"
    else:  # monthly
        schedule_type = "/SC MONTHLY /D 1"
    
    python_path = sys.executable
    command = f'"{python_path}" "{AUTO_IMPROVEMENT_SCRIPT}"'
    
    try:
        subprocess.run([
            "schtasks", "/Create", "/F", "/TN", task_name, 
            "/TR", command, schedule_type, "/ST", "00:00"
        ], check=True)
        
        print(f"✅ Tarea programada correctamente con frecuencia {frequency}.")
    except Exception as e:
        print(f"❌ Error al programar la tarea: {str(e)}")

def run_now():
    """Ejecuta el script de auto-mejora inmediatamente."""
    try:
        subprocess.Popen([sys.executable, AUTO_IMPROVEMENT_SCRIPT])
        print("✅ Ejecutando análisis de auto-mejora...")
    except Exception as e:
        print(f"❌ Error al ejecutar el análisis: {str(e)}")

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Programa la ejecución automática del análisis de auto-mejora.")
    parser.add_argument("--frequency", choices=["daily", "weekly", "monthly"], 
                        help="Frecuencia de ejecución (diaria, semanal o mensual)")
    parser.add_argument("--remove", action="store_true", 
                        help="Elimina la tarea programada")
    parser.add_argument("--run-now", action="store_true", 
                        help="Ejecuta el análisis inmediatamente después de programarlo")
    
    args = parser.parse_args()
    
    # Obtener configuración
    config = load_config()
    frequency = args.frequency or config.get("run_frequency", "weekly")
    
    # Detectar sistema operativo
    system = platform.system()
    
    if system == "Darwin":  # macOS
        schedule_macos(frequency, args.remove)
    elif system == "Linux":
        schedule_linux(frequency, args.remove)
    elif system == "Windows":
        schedule_windows(frequency, args.remove)
    else:
        print(f"❌ Sistema operativo no soportado: {system}")
        return
    
    # Actualizar configuración si se cambió la frecuencia
    if not args.remove and args.frequency and args.frequency != config.get("run_frequency"):
        config["run_frequency"] = args.frequency
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, indent=2, fp=f)
        print(f"✅ Configuración actualizada con frecuencia: {args.frequency}")
    
    # Ejecutar ahora si se solicitó
    if args.run_now and not args.remove:
        run_now()

if __name__ == "__main__":
    main()