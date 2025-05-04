"""
Optimizaciones específicas para Mac con chip M2
Este módulo contiene configuraciones y ajustes para maximizar el rendimiento en Mac con Apple Silicon
"""

import os
import platform
import multiprocessing

# Verificar si estamos en Mac con Apple Silicon
IS_MAC_APPLE_SILICON = (
    platform.system() == "Darwin" and 
    platform.machine() == "arm64"
)

# Configuraciones optimizadas para M2
M2_OPTIMIZATIONS = {
    # Número óptimo de procesos para M2 (deja 2 núcleos libres para el sistema)
    "optimal_processes": max(1, multiprocessing.cpu_count() - 2),
    
    # Configuraciones para frameworks de ML
    "tensorflow": {
        "use_metal": True,
        "memory_growth": True,
        "threads": multiprocessing.cpu_count() - 1
    },
    
    # Configuraciones para PyTorch
    "pytorch": {
        "num_threads": multiprocessing.cpu_count() - 1,
        "use_mps": True  # Metal Performance Shaders
    },
    
    # Configuraciones para OpenAI
    "openai": {
        "batch_size": 5,
        "request_timeout": 60,
        "max_retries": 3
    },
    
    # Configuraciones para procesamiento de datos
    "data_processing": {
        "chunk_size": 10000,  # Tamaño de lotes para procesamiento de datos
        "use_swifter": True,  # Usar swifter para acelerar operaciones de pandas
        "use_modin": False    # Modin puede no ser estable en todos los casos
    }
}

def apply_optimizations():
    """
    Aplica las optimizaciones para Mac M2 al entorno actual
    """
    if not IS_MAC_APPLE_SILICON:
        print("No se detectó Mac con Apple Silicon. No se aplicarán optimizaciones específicas.")
        return False
    
    print("Aplicando optimizaciones para Mac con Apple Silicon (M2)...")
    
    # Configurar variables de entorno para TensorFlow
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "1"
    os.environ["TF_METAL_ENABLED"] = "1" if M2_OPTIMIZATIONS["tensorflow"]["use_metal"] else "0"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Reducir logs
    
    # Configurar variables para PyTorch
    if M2_OPTIMIZATIONS["pytorch"]["use_mps"]:
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    
    # Configurar número de hilos para operaciones paralelas
    os.environ["OMP_NUM_THREADS"] = str(M2_OPTIMIZATIONS["pytorch"]["num_threads"])
    os.environ["MKL_NUM_THREADS"] = str(M2_OPTIMIZATIONS["pytorch"]["num_threads"])
    
    print(f"✓ Optimizaciones aplicadas para Mac M2 ({multiprocessing.cpu_count()} núcleos)")
    return True

def get_optimal_batch_size():
    """
    Devuelve el tamaño de lote óptimo según el dispositivo
    """
    if IS_MAC_APPLE_SILICON:
        return M2_OPTIMIZATIONS["openai"]["batch_size"]
    return 3  # Valor por defecto para otros sistemas

def get_optimal_processes():
    """
    Devuelve el número óptimo de procesos paralelos
    """
    if IS_MAC_APPLE_SILICON:
        return M2_OPTIMIZATIONS["optimal_processes"]
    return max(1, multiprocessing.cpu_count() - 1)