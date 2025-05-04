#!/usr/bin/env python3
"""
Script para lanzar agentes de TalentekIA basado en la configuración TOML
Este script lee la configuración y ejecuta los scripts de los agentes
"""
import os
import sys
import toml
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TalentekIA-AgentLauncher")

def print_banner():
    """Muestra el banner de inicio de la aplicación"""
    banner = """
╔════════════════════════════════════════════════════╗
║                                                    ║
║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗      ║
║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║      ║
║      ██║   ███████║██║     █████╗  ██╔██╗ ██║      ║
║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║      ║
║      ██║   ██║  ██║███████╗███████╗██║ ╚████║      ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝      ║
║                                                    ║
║              Lanzador de Agentes TOML              ║
║                                                    ║
║          Optimizado para Apple Silicon             ║
║                                                    ║
╚════════════════════════════════════════════════════╝
"""
    print(banner)

def cargar_variables_entorno():
    """Carga variables de entorno desde el archivo .env"""
    try:
        # Intentar cargar desde .env en el directorio actual
        env_path = Path('.env')
        if env_path.exists():
            logger.info(f"Cargando variables de entorno desde {env_path}")
            load_dotenv(env_path)
            return True
        else:
            logger.warning("No se encontró archivo .env en el directorio actual")
            return False
    except Exception as e:
        logger.error(f"Error al cargar variables de entorno: {str(e)}")
        return False

def cargar_configuracion(path_toml):
    """Carga la configuración desde un archivo TOML"""
    try:
        logger.info(f"Cargando configuración desde {path_toml}")
        with open(path_toml, "r") as f:
            return toml.load(f)
    except Exception as e:
        logger.error(f"Error al cargar la configuración TOML: {str(e)}")
        return None

def ejecutar_agentes(config, modo_real=False):
    """Ejecuta los agentes definidos en la configuración TOML"""
    # Contador para estadísticas
    total = 0
    exitosos = 0
    fallidos = 0
    
    # Obtener la ruta base para los scripts
    ruta_base = ""
    if "entorno" in config and "ruta_base" in config["entorno"]:
        ruta_base_raw = config["entorno"]["ruta_base"]
        # Expandir ~ a la ruta del home del usuario
        ruta_base = os.path.expanduser(ruta_base_raw)
    
    # Hora de inicio
    tiempo_inicio = datetime.now()
    
    # Procesar cada sección que comienza con "agente_"
    for key, value in config.items():
        if key.startswith("agente_"):
            total += 1
            nombre = value.get("nombre", key)
            script_path = value.get("script", "")
            
            # Si la ruta no es absoluta y tenemos una ruta base, combinarlas
            if script_path and not os.path.isabs(script_path) and ruta_base:
                script_path = os.path.join(ruta_base, script_path)
            
            # Verificar si el script existe
            script_exists = Path(script_path).exists() if script_path else False
            
            print(f"\n{'='*50}")
            print(f"▶️ Ejecutando agente: {nombre}")
            print(f"📄 Script: {script_path}")
            print(f"{'='*50}")
            
            if script_path and script_exists:
                try:
                    # Ejecutar el script
                    logger.info(f"Ejecutando script: {script_path}")
                    start_time = datetime.now()
                    
                    # Preparar entorno para el script
                    env = os.environ.copy()
                    
                    # Añadir parámetros específicos del agente como variables de entorno
                    for param_key, param_value in value.items():
                        if isinstance(param_value, str):  # Solo pasar strings como variables de entorno
                            env_key = f"AGENT_{param_key.upper()}"
                            env[env_key] = param_value
                    
                    # Añadir modo real si está activado
                    if modo_real:
                        env["AGENT_MODE"] = "real"
                    else:
                        env["AGENT_MODE"] = "simulation"
                    
                    # Determinar el comando a ejecutar
                    if script_path.endswith(".py"):
                        result = subprocess.run(["python3", script_path], 
                                              capture_output=True, 
                                              text=True,
                                              env=env)
                    else:
                        result = subprocess.run([script_path], 
                                              capture_output=True, 
                                              text=True,
                                              env=env)
                    
                    # Calcular duración
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    
                    # Verificar resultado
                    if result.returncode == 0:
                        exitosos += 1
                        print(f"✅ Ejecución exitosa en {duration:.2f} segundos")
                        # Mostrar salida del script (limitada a 10 líneas)
                        output_lines = result.stdout.strip().split('\n')
                        if output_lines and output_lines[0]:
                            print("\nSalida del script:")
                            for i, line in enumerate(output_lines[:10]):
                                print(f"  {line}")
                            if len(output_lines) > 10:
                                print(f"  ... y {len(output_lines) - 10} líneas más")
                    else:
                        fallidos += 1
                        print(f"❌ Error en la ejecución (código {result.returncode})")
                        if result.stderr:
                            print("\nError:")
                            for line in result.stderr.strip().split('\n')[:5]:
                                print(f"  {line}")
                
                except Exception as e:
                    fallidos += 1
                    logger.error(f"Error al ejecutar el agente '{nombre}': {str(e)}")
                    print(f"❌ Error: {str(e)}")
            else:
                fallidos += 1
                logger.error(f"No se encontró el script del agente '{nombre}': {script_path}")
                print(f"❌ No se encontró el script: {script_path}")
    
    # Calcular duración total
    tiempo_fin = datetime.now()
    duracion_total = (tiempo_fin - tiempo_inicio).total_seconds()
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print(f"RESUMEN DE EJECUCIÓN")
    print(f"{'='*50}")
    print(f"Total de agentes: {total}")
    print(f"Exitosos: {exitosos}")
    print(f"Fallidos: {fallidos}")
    print(f"Duración total: {duracion_total:.2f} segundos")
    if total > 0:
        print(f"Tiempo promedio: {duracion_total/total:.2f} segundos por agente")
    
    return exitosos, fallidos

def parse_arguments():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description="Lanzador de agentes TalentekIA")
    parser.add_argument("--config", "-c", 
                        default="talentek_agentes_config.toml",
                        help="Ruta al archivo de configuración TOML")
    parser.add_argument("--real", "-r", 
                        action="store_true",
                        help="Ejecutar en modo real (usando APIs reales)")
    return parser.parse_args()

def main():
    """Función principal"""
    # Parsear argumentos
    args = parse_arguments()
    
    print_banner()
    
    # Cargar variables de entorno
    env_loaded = cargar_variables_entorno()
    if env_loaded:
        print("✅ Variables de entorno cargadas correctamente")
    else:
        print("⚠️ No se pudieron cargar las variables de entorno")
    
    # Determinar la ruta del archivo de configuración TOML
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Archivo de configuración no encontrado: {config_path}")
        sys.exit(1)
    
    # Cargar la configuración
    config = cargar_configuracion(config_path)
    if config is None:
        sys.exit(1)
    
    # Mostrar información del entorno
    if "entorno" in config:
        entorno = config["entorno"]
        print(f"\nEntorno: {entorno.get('nombre', 'No especificado')}")
        print(f"Chip: {entorno.get('chip', 'No especificado')}")
        print(f"Soporte Mac: {'Sí' if entorno.get('soporte_mac', False) else 'No'}")
    
    # Mostrar información de personalización
    if "personalizacion" in config:
        pers = config["personalizacion"]
        print(f"Usuario: {pers.get('usuario', 'No especificado')}")
    
    # Mostrar modo de ejecución
    modo_real = args.real
    if modo_real:
        print("\n🔴 MODO REAL: Utilizando APIs y servicios reales")
    else:
        print("\n🔵 MODO SIMULACIÓN: Datos de ejemplo (usa --real para modo real)")
    
    # Ejecutar los agentes
    print("\nIniciando ejecución de agentes...")
    exitosos, fallidos = ejecutar_agentes(config, modo_real)
    
    # Código de salida basado en el éxito de la ejecución
    if fallidos > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario")
        sys.exit(130)  # Código estándar para interrupción por SIGINT
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        sys.exit(1)