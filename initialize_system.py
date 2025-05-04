#!/usr/bin/env python3
"""
Script de inicialización del sistema TalentekIA
Este script configura el entorno de trabajo, verifica dependencias y prepara el sistema para su uso.
"""

import os
import sys
import json
import subprocess
import platform
import shutil
from datetime import datetime

def print_banner():
    """Muestra el banner de bienvenida"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗████████╗     ║
    ║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║╚══██╔══╝     ║
    ║      ██║   ███████║██║     █████╗  ██╔██╗ ██║   ██║        ║
    ║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║   ██║        ║
    ║      ██║   ██║  ██║███████╗███████╗██║ ╚████║   ██║        ║
    ║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝        ║
    ║                                                            ║
    ║                      TalentekIA                            ║
    ║                                                            ║
    ║           Sistema de Agentes de IA Personalizados          ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"Inicializando sistema... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sistema: {platform.system()} {platform.release()} ({platform.machine()})")
    print("-" * 60)

def run_command(command):
    """Ejecuta un comando en la terminal y devuelve el resultado"""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_directories():
    """Configura la estructura de directorios del proyecto"""
    print("Configurando estructura de directorios...")
    
    # Directorios principales
    directories = [
        "src/agents",
        "src/interface",
        "src/utils",
        "data/input",
        "data/output",
        "docs",
        "tests",
        "config"
    ]
    
    # Crear directorios si no existen
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directorio {directory} verificado")
    
    # Crear archivos .gitkeep para mantener la estructura en git
    for directory in ["data/input", "data/output"]:
        gitkeep_file = os.path.join(directory, ".gitkeep")
        if not os.path.exists(gitkeep_file):
            with open(gitkeep_file, 'w') as f:
                pass
    
    print("✓ Estructura de directorios configurada correctamente")

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("\nVerificando dependencias...")
    
    # Verificar pip
    success, output = run_command("pip --version")
    if not success:
        print("❌ Error: pip no está instalado o no está en el PATH")
        return False
    
    # Verificar dependencias desde requirements.txt
    if os.path.exists("requirements.txt"):
        print("Instalando dependencias desde requirements.txt...")
        success, output = run_command("pip install -r requirements.txt")
        if not success:
            print(f"❌ Error al instalar dependencias: {output}")
            return False
        print("✓ Dependencias instaladas correctamente")
    else:
        print("❌ Error: No se encontró el archivo requirements.txt")
        return False
    
    # Verificar dependencias específicas
    critical_packages = ["streamlit", "pandas", "numpy", "openai", "langchain"]
    for package in critical_packages:
        success, _ = run_command(f"pip show {package}")
        if not success:
            print(f"❌ Error: El paquete {package} no está instalado correctamente")
            return False
        print(f"✓ {package} instalado correctamente")
    
    # Verificar dependencias adicionales
    required_packages = [
        "torch",
        "transformers",
        "sklearn",
        "matplotlib"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package}")
    
    if missing_packages:
        print("\nFaltan dependencias. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
        print("Dependencias instaladas correctamente.")
    else:
        print("Todas las dependencias requeridas están instaladas.")
    
    return True

def check_environment():
    """Verifica la configuración del entorno"""
    print("\nVerificando configuración del entorno...")
    
    # Detectar sistema operativo
    operating_system = platform.system()
    print(f"Sistema operativo detectado: {operating_system}")
    
    # Detectar arquitectura
    architecture = platform.machine()
    print(f"Arquitectura detectada: {architecture}")
    
    # Verificaciones específicas para MacOS con chip M1/M2
    if operating_system == "Darwin" and architecture in ["arm64"]:
        print("Detectado MacOS con Apple Silicon (M1/M2)")
        optimize_for_apple_silicon()
    
    # Verificar archivo .env
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✓ Archivo .env creado a partir de .env.example")
            print("⚠️ Por favor, edita el archivo .env con tus claves API")
        else:
            print("❌ Error: No se encontró el archivo .env ni .env.example")
            # Crear un archivo .env básico
            with open(".env", "w") as f:
                f.write("""# Configuración de TalentekIA
# API Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
HUGGINGFACE_API_KEY=

# Configuración de rendimiento
PERFORMANCE_MODE=balanced  # eco, balanced, performance

# Configuración de notificaciones
ENABLE_EMAIL_NOTIFICATIONS=false
NOTIFICATION_EMAIL=

# Configuración de base de datos
DATABASE_PATH=data/talentek.db
""")
            print("✓ Archivo .env básico creado. Por favor, edítalo con tus claves API")
    else:
        print("✓ Archivo .env encontrado")
    
    # Verificar archivo de configuración
    config_path = "config/settings.json"
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        default_config = {
            "api_keys": {
                "openai": "",
                "anthropic": "",
                "huggingface": ""
            },
            "performance_mode": "balanced",
            "update_frequency": {
                "linkedin_agent": "daily",
                "estrategia_comercial": "weekly",
                "finanzas_personales": "monthly"
            },
            "notifications": {
                "email": "",
                "enable_email": False,
                "enable_desktop": True
            }
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        print(f"✓ Archivo de configuración {config_path} creado con valores predeterminados")
    else:
        print(f"✓ Archivo de configuración {config_path} encontrado")
    
    return True

def optimize_for_apple_silicon():
    """Aplica optimizaciones específicas para Apple Silicon (M1/M2)"""
    print("Aplicando optimizaciones para Apple Silicon (M1/M2)...")
    
    # Configurar variables de entorno para optimizar el rendimiento
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    
    # Verificar si se tienen instaladas las versiones optimizadas de las bibliotecas
    try:
        import torch
        if torch.backends.mps.is_available():
            print("✓ MPS (Metal Performance Shaders) disponible para PyTorch")
        else:
            print("⚠️ MPS no disponible. Se recomienda actualizar PyTorch a una versión compatible con Apple Silicon")
    except (ImportError, AttributeError):
        print("⚠️ PyTorch no está instalado o no es compatible con MPS")
    
    # Sugerir configuraciones adicionales
    print("\nRecomendaciones adicionales para optimización en Apple Silicon:")
    print("- Use 'pip install -U tensorflow-macos tensorflow-metal' para TensorFlow optimizado")
    print("- Utilice modelos ligeros o cuantificados cuando sea posible")
    print("- Considere activar la característica de memoria compartida para mayor rendimiento")

def check_api_keys():
    """Verifica que las claves API necesarias estén configuradas"""
    print("\nVerificando claves API...")
    
    # Cargar variables de entorno desde .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("❌ Error: No se pudo cargar el módulo dotenv")
        return False
    
    # Verificar claves API críticas
    api_keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "HUGGINGFACE_API_KEY": os.getenv("HUGGINGFACE_API_KEY")
    }
    
    missing_keys = [key for key, value in api_keys.items() if not value]
    
    if missing_keys:
        print(f"⚠️ Advertencia: Las siguientes claves API no están configuradas: {', '.join(missing_keys)}")
        print("Algunas funcionalidades pueden no estar disponibles.")
    else:
        print("✓ Todas las claves API están configuradas")
    
    return len(missing_keys) == 0

def main():
    """Función principal"""
    print_banner()
    
    # Configurar estructura de directorios
    setup_directories()
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ Error: No se pudieron verificar todas las dependencias.")
        print("Por favor, instala las dependencias manualmente con: pip install -r requirements.txt")
        return False
    
    # Verificar configuración del entorno
    if not check_environment():
        print("\n❌ Error: No se pudo configurar correctamente el entorno.")
        return False
    
    # Verificar claves API
    api_keys_ok = check_api_keys()
    if not api_keys_ok:
        print("\n⚠️ Advertencia: Algunas claves API no están configuradas.")
        print("Por favor, edita el archivo .env con tus claves API.")
    
    print("\n" + "=" * 60)
    print("✅ Inicialización completada.")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Instrucciones finales
    print("\nPara iniciar la aplicación, ejecuta:")
    print("streamlit run src/interface/streamlit_app.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)