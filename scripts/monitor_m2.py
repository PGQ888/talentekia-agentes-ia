#!/usr/bin/env python3
"""
Script para monitorear el rendimiento en Mac M2
Este script muestra información sobre el uso de CPU, RAM y GPU (si está disponible)
"""

import psutil
import platform
import time
import os
import subprocess
from datetime import datetime

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# Colores para la salida
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def get_size(bytes, suffix="B"):
    """
    Escala los bytes a su representación legible por humanos
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def is_apple_silicon():
    """
    Detecta si el sistema es Apple Silicon (M1/M2)
    """
    return platform.system() == "Darwin" and platform.machine() == "arm64"

def get_metal_info():
    """
    Intenta obtener información sobre Metal en macOS
    """
    try:
        # Este comando solo funciona en macOS
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType"], 
            capture_output=True, 
            text=True
        )
        return result.stdout
    except:
        return "No se pudo obtener información de Metal"

def monitor_once():
    """
    Muestra una instantánea del uso de recursos del sistema
    """
    print(f"{BLUE}===== Monitoreo de Sistema TalentekIA ====={RESET}")
    print(f"{BLUE}Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    
    # Información del sistema
    print(f"\n{YELLOW}Información del Sistema:{RESET}")
    uname = platform.uname()
    print(f"Sistema: {uname.system}")
    print(f"Nombre del equipo: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Versión: {uname.version}")
    print(f"Máquina: {uname.machine}")
    print(f"Procesador: {uname.processor}")
    
    # CPU
    print(f"\n{YELLOW}Información de CPU:{RESET}")
    print(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"Núcleos totales: {psutil.cpu_count(logical=True)}")
    
    # Uso de CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    color = GREEN if cpu_percent < 50 else YELLOW if cpu_percent < 80 else RED
    print(f"Uso de CPU: {color}{cpu_percent}%{RESET}")
    
    # Memoria RAM
    print(f"\n{YELLOW}Información de Memoria RAM:{RESET}")
    svmem = psutil.virtual_memory()
    color = GREEN if svmem.percent < 50 else YELLOW if svmem.percent < 80 else RED
    print(f"Total: {get_size(svmem.total)}")
    print(f"Disponible: {get_size(svmem.available)}")
    print(f"Usada: {get_size(svmem.used)} ({color}{svmem.percent}%{RESET})")
    
    # GPU
    if GPU_AVAILABLE:
        print(f"\n{YELLOW}Información de GPU:{RESET}")
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                for i, gpu in enumerate(gpus):
                    print(f"GPU {i}: {gpu.name}")
                    color = GREEN if gpu.load < 0.5 else YELLOW if gpu.load < 0.8 else RED
                    print(f"Uso de GPU: {color}{gpu.load*100:.1f}%{RESET}")
                    print(f"Memoria total: {gpu.memoryTotal}MB")
                    print(f"Memoria usada: {gpu.memoryUsed}MB")
                    print(f"Temperatura: {gpu.temperature}°C")
            else:
                print("No se detectaron GPUs compatibles con GPUtil")
        except Exception as e:
            print(f"Error al obtener información de GPU: {e}")
    
    # Información específica de Apple Silicon
    if is_apple_silicon():
        print(f"\n{YELLOW}Información de Apple Silicon:{RESET}")
        print(f"{GREEN}Detectado Apple Silicon (M1/M2){RESET}")
        print("Variables de entorno para optimización:")
        print(f"PYTORCH_ENABLE_MPS_FALLBACK: {os.environ.get('PYTORCH_ENABLE_MPS_FALLBACK', 'No configurado')}")
        print(f"TF_ENABLE_ONEDNN_OPTS: {os.environ.get('TF_ENABLE_ONEDNN_OPTS', 'No configurado')}")
        
        # Intentar obtener información de Metal
        print("\nInformación de Metal (resumen):")
        metal_info = get_metal_info()
        # Extraer solo las líneas relevantes
        for line in metal_info.split('\n'):
            if any(keyword in line for keyword in ["Metal:", "Vendor", "Device", "VRAM", "Apple M"]):
                print(f"  {line.strip()}")

def monitor_continuous(interval=2, duration=None):
    """
    Monitorea continuamente el sistema
    
    Args:
        interval: Intervalo entre mediciones en segundos
        duration: Duración total del monitoreo en segundos (None para infinito)
    """
    start_time = time.time()
    count = 0
    
    try:
        while True:
            if count > 0:
                os.system('clear' if os.name == 'posix' else 'cls')
            
            monitor_once()
            count += 1
            
            if duration and time.time() - start_time >= duration:
                break
                
            print(f"\n{BLUE}Presiona Ctrl+C para detener el monitoreo...{RESET}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Monitoreo detenido por el usuario{RESET}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor de rendimiento para TalentekIA en Mac M2")
    parser.add_argument("-c", "--continuous", action="store_true", help="Monitoreo continuo")
    parser.add_argument("-i", "--interval", type=int, default=2, help="Intervalo entre mediciones (segundos)")
    parser.add_argument("-d", "--duration", type=int, help="Duración total del monitoreo (segundos)")
    
    args = parser.parse_args()
    
    if args.continuous:
        monitor_continuous(interval=args.interval, duration=args.duration)
    else:
        monitor_once()