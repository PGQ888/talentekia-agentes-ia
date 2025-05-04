#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para optimizar TalentekIA en Mac con Apple Silicon (M1/M2/M3)

Este script configura automáticamente el entorno para obtener el mejor rendimiento
en dispositivos Mac con Apple Silicon y muestra información detallada del sistema.
"""

import os
import sys
import platform
import psutil
import argparse
from datetime import datetime

# Añadir el directorio raíz al path para importar módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.utils.m2_optimizer import M2Optimizer
except ImportError:
    print("Error: No se pudo importar el módulo M2Optimizer")
    print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
    sys.exit(1)

# Colores para la salida
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_banner():
    """Muestra un banner con información del sistema."""
    print(f"{BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗████████╗     ║")
    print("║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║╚══██╔══╝     ║")
    print("║      ██║   ███████║██║     █████╗  ██╔██╗ ██║   ██║        ║")
    print("║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║   ██║        ║")
    print("║      ██║   ██║  ██║███████╗███████╗██║ ╚████║   ██║        ║")
    print("║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝        ║")
    print("║                                                            ║")
    print("║                  Optimizador para M2                       ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

    # Fecha y hora actual
    print(f"{YELLOW}Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{YELLOW}Sistema: {platform.system()} {platform.release()} ({platform.machine()}){RESET}")
    print("--------------------------------------------------------")


def print_system_info():
    """Muestra información detallada del sistema."""
    print(f"\n{BLUE}=== INFORMACIÓN DEL SISTEMA ==={RESET}")
    
    # CPU
    print(f"\n{YELLOW}CPU:{RESET}")
    print(f"  Procesador: {platform.processor()}")
    print(f"  Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"  Núcleos lógicos: {psutil.cpu_count(logical=True)}")
    
    # Memoria
    mem = psutil.virtual_memory()
    print(f"\n{YELLOW}Memoria:{RESET}")
    print(f"  Total: {mem.total / (1024**3):.2f} GB")
    print(f"  Disponible: {mem.available / (1024**3):.2f} GB")
    print(f"  Usada: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    
    # Python
    print(f"\n{YELLOW}Python:{RESET}")
    print(f"  Versión: {platform.python_version()}")
    print(f"  Implementación: {platform.python_implementation()}")
    print(f"  Ruta: {sys.executable}")
    
    # Entorno virtual
    venv = os.environ.get('VIRTUAL_ENV')
    if venv:
        print(f"  Entorno virtual: {os.path.basename(venv)}")
    else:
        print(f"  Entorno virtual: {RED}No detectado{RESET}")


def export_env_file(optimizer, output_file=".env.optimized"):
    """Exporta las variables de entorno optimizadas a un archivo.
    
    Args:
        optimizer: Instancia de M2Optimizer
        output_file: Ruta del archivo de salida
    """
    if not optimizer.optimizations_applied:
        optimizer.optimize()
    
    with open(output_file, "w") as f:
        f.write("# TalentekIA - Variables de entorno optimizadas para Mac M1/M2/M3\n")
        f.write(f"# Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Agrupar variables por categoría
        categories = {
            "# Variables de entorno para optimización de rendimiento": 
                ["PYTORCH_ENABLE_MPS_FALLBACK", "TF_ENABLE_ONEDNN_OPTS", "XLA_FLAGS"],
            "# Configuración de memoria y caché": 
                ["PYTORCH_CUDA_ALLOC_CONF", "TF_FORCE_GPU_ALLOW_GROWTH", 
                 "TRANSFORMERS_CACHE", "SENTENCE_TRANSFORMERS_HOME"],
            "# Configuración de paralelismo": 
                ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", 
                 "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"],
            "# Configuración de logging": 
                ["TF_CPP_MIN_LOG_LEVEL", "TOKENIZERS_PARALLELISM"],
            "# Configuración específica de TalentekIA": 
                ["TALENTEK_"]
        }
        
        for category, prefixes in categories.items():
            f.write(f"{category}\n")
            for key, value in optimizer.env_vars.items():
                if any(key.startswith(p) for p in prefixes) or any(p in key for p in prefixes):
                    f.write(f"{key}={value}\n")
            f.write("\n")
    
    print(f"\n{GREEN}Variables de entorno exportadas a {output_file}{RESET}")
    print(f"Para usarlas en tu terminal, ejecuta: {YELLOW}source {output_file}{RESET}")


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Optimizador de TalentekIA para Mac con Apple Silicon (M1/M2/M3)"
    )
    parser.add_argument(
        "--export", 
        action="store_true", 
        help="Exportar variables de entorno a un archivo .env.optimized"
    )
    parser.add_argument(
        "--apply", 
        action="store_true", 
        help="Aplicar optimizaciones al entorno actual"
    )
    parser.add_argument(
        "--info", 
        action="store_true", 
        help="Mostrar información detallada del sistema"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Crear instancia del optimizador
    optimizer = M2Optimizer()
    
    # Verificar si es un Mac con Apple Silicon
    if not optimizer.is_apple_silicon:
        print(f"{RED}Este sistema no es un Mac con Apple Silicon (M1/M2/M3).{RESET}")
        print(f"{YELLOW}Las optimizaciones específicas para M2 no están disponibles.{RESET}")
        return 1
    
    # Mostrar información del sistema si se solicita
    if args.info:
        print_system_info()
    
    # Aplicar optimizaciones
    if args.apply:
        optimizer.optimize()
        print(f"\n{GREEN}Optimizaciones aplicadas correctamente al entorno actual.{RESET}")
    
    # Exportar variables de entorno
    if args.export:
        export_env_file(optimizer)
    
    # Si no se especificó ninguna acción, mostrar estado
    if not (args.info or args.apply or args.export):
        optimizer.optimize()
        optimizer.print_status()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())