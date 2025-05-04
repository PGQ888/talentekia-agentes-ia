#!/usr/bin/env python3
"""
Script para analizar el código de TalentekAI Unified y detectar posibles mejoras.
Este script analiza el código fuente, detecta problemas y genera un reporte
con sugerencias de mejora.
"""

import os
import re
import sys
import json
import logging
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'auto_improvement.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('auto_improvement')

# Configuración
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "auto_improvement_config.json")
REPORT_FILE = os.path.join(PROJECT_ROOT, "reports", "auto_improvement_report.md")

# Patrones para detectar problemas de rendimiento
PERFORMANCE_PATTERNS = [
    {
        "name": "Concatenación ineficiente de strings",
        "pattern": r"(s|str|string|text|result|output|html|xml|json|data)\s*\+=\s*",
        "suggestion": "Usa ''.join() en lugar de concatenación de strings en loops",
        "extensions": [".py", ".js", ".ts"]
    },
    {
        "name": "Función regular dentro de loop",
        "pattern": r"for\s+.*?:\s*.*?function\s*\(",
        "suggestion": "Define funciones fuera de loops para evitar recrearlas en cada iteración",
        "extensions": [".js", ".ts"]
    },
    {
        "name": "Posible fuga de memoria en addEventListener",
        "pattern": r"addEventListener\s*\(",
        "suggestion": "Asegúrate de eliminar event listeners con removeEventListener cuando ya no sean necesarios",
        "extensions": [".js", ".ts"]
    },
    {
        "name": "Uso ineficiente de listas",
        "pattern": r"for\s+.*?\s+in\s+range\s*\(\s*len\s*\(\s*.*?\s*\)\s*\)",
        "suggestion": "Considera usar generadores o list comprehensions para operaciones con grandes conjuntos de datos",
        "extensions": [".py"]
    }
]

def load_config() -> Dict[str, Any]:
    """Carga la configuración del script."""
    config_dir = os.path.dirname(CONFIG_FILE)
    os.makedirs(config_dir, exist_ok=True)
    
    default_config = {
        "email_notifications": False,
        "email_to": "",
        "smtp_server": "",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_password": "",
        "run_frequency": "weekly",
        "analyze_dependencies": True,
        "analyze_code_quality": True,
        "analyze_performance": True,
        "auto_apply_safe_fixes": False,
        "ignored_directories": ["node_modules", "dist", ".git", "venv"],
        "custom_rules": []
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

def analyze_performance(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analiza el código en busca de problemas de rendimiento.
    
    Args:
        config: Configuración del análisis
        
    Returns:
        Lista de problemas encontrados
    """
    issues = []
    ignored_dirs = set(config.get("ignored_directories", []))
    
    # Combinar patrones predefinidos y personalizados
    patterns = PERFORMANCE_PATTERNS.copy()
    patterns.extend(config.get("custom_rules", []))
    
    # Recorrer todos los archivos del proyecto
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Excluir directorios ignorados
        dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith('.')]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, PROJECT_ROOT)
            
            # Verificar extensión del archivo
            _, ext = os.path.splitext(filename)
            if not ext:
                continue
                
            # Analizar archivo según los patrones
            for pattern in patterns:
                if ext not in pattern.get("extensions", []):
                    continue
                    
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    matches = re.finditer(pattern["pattern"], content)
                    match_count = sum(1 for _ in matches)
                    
                    if match_count > 0:
                        issues.append({
                            "file": rel_path,
                            "issue": pattern["name"],
                            "count": match_count,
                            "suggestion": pattern["suggestion"]
                        })
                except Exception as e:
                    logger.warning(f"Error al analizar {rel_path}: {str(e)}")
    
    return issues

def generate_report(performance_issues: List[Dict[str, Any]]) -> str:
    """
    Genera un reporte en formato Markdown con los problemas encontrados.
    
    Args:
        performance_issues: Lista de problemas de rendimiento
        
    Returns:
        Contenido del reporte en formato Markdown
    """
    # Agrupar problemas por archivo
    issues_by_file = {}
    for issue in performance_issues:
        file = issue["file"]
        if file not in issues_by_file:
            issues_by_file[file] = []
        issues_by_file[file].append(issue)
    
    # Generar reporte
    report_lines = []
    
    # Agregar problemas de rendimiento
    for file, issues in issues_by_file.items():
        for issue in issues:
            report_lines.append(f"- **{file}**: {issue['issue']} ({issue['count']} ocurrencias)")
            report_lines.append(f"  - Sugerencia: {issue['suggestion']}")
            report_lines.append("")
    
    # Agregar resumen
    report_lines.append("## Resumen de Mejoras Sugeridas")
    report_lines.append("")
    report_lines.append(f"- **Problemas de rendimiento**: {len(performance_issues)} problemas encontrados")
    report_lines.append("")
    
    # Agregar comandos para aplicar mejoras
    report_lines.append("## Comandos para aplicar mejoras")
    report_lines.append("")
    report_lines.append("```bash")
    # Aquí se podrían agregar comandos específicos para aplicar mejoras automáticamente
    report_lines.append("```")
    
    return "\n".join(report_lines)

def send_email_notification(config: Dict[str, Any], report_content: str) -> bool:
    """
    Envía una notificación por correo electrónico con el reporte.
    
    Args:
        config: Configuración del script
        report_content: Contenido del reporte
        
    Returns:
        True si se envió correctamente, False en caso contrario
    """
    if not config.get("email_notifications", False):
        return False
        
    email_to = config.get("email_to")
    smtp_server = config.get("smtp_server")
    smtp_port = config.get("smtp_port", 587)
    smtp_user = config.get("smtp_user")
    smtp_password = config.get("smtp_password")
    
    if not all([email_to, smtp_server, smtp_user, smtp_password]):
        logger.warning("Configuración de correo incompleta. No se enviará notificación.")
        return False
    
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email_to
        msg['Subject'] = f"TalentekAI Unified - Reporte de Auto-Mejora ({datetime.datetime.now().strftime('%Y-%m-%d')})"
        
        msg.attach(MIMEText(report_content, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Notificación enviada a {email_to}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar notificación: {str(e)}")
        return False

def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description="Analiza el código y detecta posibles mejoras.")
    parser.add_argument("--no-report", action="store_true", help="No generar reporte")
    parser.add_argument("--no-email", action="store_true", help="No enviar notificación por correo")
    args = parser.parse_args()
    
    # Crear directorios necesarios
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, "logs"), exist_ok=True)
    
    print("Iniciando análisis de auto-mejora...")
    
    # Cargar configuración
    config = load_config()
    
    # Analizar rendimiento
    performance_issues = []
    if config.get("analyze_performance", True):
        performance_issues = analyze_performance(config)
    
    # Generar reporte
    if not args.no_report:
        report_content = generate_report(performance_issues)
        with open(REPORT_FILE, 'w') as f:
            f.write(report_content)
        print(f"Reporte generado en {REPORT_FILE}")
    
    # Enviar notificación por correo
    if config.get("email_notifications", False) and not args.no_email:
        send_email_notification(config, report_content)
    
    print("Análisis de auto-mejora completado.")

if __name__ == "__main__":
    main()