#!/usr/bin/env python3
"""
Script de inicio de TalentekIA optimizado para Mac M2
Este script aplica automáticamente optimizaciones para Apple Silicon y lanza la aplicación
"""
import os
import sys
import time
import logging
import platform
import subprocess
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TalentekIA-Launcher")

# Asegurar que estamos en el directorio correcto
os.chdir(Path(__file__).parent)

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
║                  TalentekIA                        ║
║                                                    ║
║          Optimizado para Apple Silicon             ║
║                                                    ║
╚════════════════════════════════════════════════════╝
"""
    print(banner)

def is_apple_silicon():
    """Detecta si es Mac con Apple Silicon"""
    return platform.system() == "Darwin" and platform.machine() == "arm64"

def check_dependencies():
    """Verifica las dependencias críticas"""
    required_modules = ["streamlit", "pandas", "numpy"]
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        logger.error(f"Dependencias faltantes: {', '.join(missing)}")
        logger.info("Instalando dependencias...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            logger.info("Dependencias instaladas correctamente")
        except subprocess.CalledProcessError:
            logger.error("Error al instalar dependencias")
            sys.exit(1)
    
    # Verificar dependencias específicas para M2
    if is_apple_silicon():
        m2_modules = ["tensorflow-macos", "tensorflow-metal", "torch"]
        m2_missing = []
        
        for module in m2_modules:
            base_module = module.split('-')[0]
            try:
                __import__(base_module)
            except ImportError:
                m2_missing.append(module)
        
        if m2_missing:
            logger.warning(f"Algunas optimizaciones para M2 no están disponibles. Paquetes recomendados: {', '.join(m2_missing)}")
            print("\n¿Deseas instalar los paquetes optimizados para M2? (s/n): ", end="")
            response = input().lower()
            if response == "s":
                logger.info("Instalando paquetes optimizados para M2...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", *m2_missing])
                    logger.info("Paquetes para M2 instalados correctamente")
                except subprocess.CalledProcessError:
                    logger.error("Error al instalar paquetes para M2")

def setup_environment():
    """Configura el entorno de ejecución"""
    # Añadir directorio raíz al path
    root_dir = Path(__file__).parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    
    # Aplicar optimizaciones para M2 si corresponde
    if is_apple_silicon():
        logger.info("Detectado Mac con Apple Silicon, aplicando optimizaciones...")
        try:
            from src.utils.m2_optimizer import setup_m2_environment
            result = setup_m2_environment()
            if result["status"] == "success":
                logger.info("Optimizaciones para M2 aplicadas correctamente")
            else:
                logger.warning(f"No se pudieron aplicar todas las optimizaciones: {result.get('message', 'error desconocido')}")
        except ImportError:
            logger.warning("No se pudo cargar el optimizador para M2")

def verify_config():
    """Verifica la configuración del sistema"""
    config_dir = Path(__file__).parent / "config"
    config_file = config_dir / "settings.json"
    
    if not config_dir.exists():
        logger.info("Creando directorio de configuración...")
        config_dir.mkdir(exist_ok=True)
    
    if not config_file.exists():
        logger.info("Archivo de configuración no encontrado, ejecutando inicialización...")
        try:
            subprocess.check_call([sys.executable, "initialize_system.py"])
        except subprocess.CalledProcessError:
            logger.error("Error al inicializar el sistema")
            sys.exit(1)

def launch_application():
    """Lanza la aplicación principal"""
    app_path = Path(__file__).parent / "src" / "interface" / "streamlit_app.py"
    
    if not app_path.exists():
        logger.error(f"Archivo de aplicación no encontrado: {app_path}")
        sys.exit(1)
    
    logger.info("Lanzando aplicación TalentekIA...")
    
    # Ejecutar Streamlit con optimizaciones
    env = os.environ.copy()
    if is_apple_silicon():
        env["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        env["TF_ENABLE_ONEDNN_OPTS"] = "0"
    
    try:
        subprocess.run(["streamlit", "run", str(app_path)], env=env)
    except Exception as e:
        logger.error(f"Error al lanzar la aplicación: {str(e)}")
        sys.exit(1)

def main():
    """Función principal"""
    start_time = time.time()
    
    print_banner()
    print(f"Sistema: {platform.system()} {platform.release()} ({platform.machine()})")
    
    # Verificar si es Mac M2/M1
    if is_apple_silicon():
        print("✅ Detectado Mac con Apple Silicon (M1/M2)")
        print("🚀 Aplicando optimizaciones específicas para rendimiento...\n")
    else:
        print("ℹ️  Este script está optimizado para Mac con Apple Silicon.")
        print("   Se continuará con la configuración estándar.\n")
    
    print("Inicializando TalentekIA...")
    
    # Verificar dependencias
    check_dependencies()
    
    # Configurar entorno
    setup_environment()
    
    # Verificar configuración
    verify_config()
    
    # Calcular tiempo de inicio
    setup_time = time.time() - start_time
    print(f"\n✅ Inicialización completada en {setup_time:.2f} segundos")
    
    # Lanzar aplicación
    print("\nLanzando interfaz de usuario...\n")
    launch_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        sys.exit(1)