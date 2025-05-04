"""
Optimizaciones específicas para Mac con chip M2.
"""

import os
import sys
import platform
import subprocess
from typing import Dict, List, Tuple, Any

def is_apple_silicon() -> bool:
    """Detecta si el sistema es un Mac con Apple Silicon (M1, M2, etc.)."""
    return (
        platform.system() == "Darwin" and 
        platform.machine() == "arm64"
    )

def get_device_info() -> Dict[str, Any]:
    """Obtiene información detallada sobre el dispositivo."""
    info = {
        "platform": platform.system(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "is_apple_silicon": is_apple_silicon()
    }
    
    if is_apple_silicon():
        # Obtener información específica de Apple Silicon
        try:
            # Obtener modelo de Mac
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"], 
                capture_output=True, 
                text=True
            )
            info["processor"] = result.stdout.strip()
            
            # Obtener memoria RAM
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"], 
                capture_output=True, 
                text=True
            )
            info["memory_bytes"] = int(result.stdout.strip())
            info["memory_gb"] = round(info["memory_bytes"] / (1024**3), 1)
        except Exception as e:
            print(f"Error al obtener información del dispositivo: {e}")
    
    return info

def get_pytorch_status() -> Dict[str, Any]:
    """Verifica el estado de PyTorch y si está optimizado para MPS."""
    status = {
        "installed": False,
        "version": None,
        "mps_available": False,
        "optimized_for_m2": False
    }
    
    try:
        import torch
        status["installed"] = True
        status["version"] = torch.__version__
        status["mps_available"] = hasattr(torch, 'mps') and hasattr(torch.mps, 'is_available') and torch.mps.is_available()
        
        # Verificar si está usando la versión optimizada para M2
        if "nightly" in torch.__version__ or float(torch.__version__.split('+')[0]) >= 1.12:
            status["optimized_for_m2"] = True
    except ImportError:
        pass
    
    return status

def get_optimization_recommendations() -> List[str]:
    """Proporciona recomendaciones para optimizar el entorno para M2."""
    recommendations = []
    
    if not is_apple_silicon():
        recommendations.append("Este sistema no es Apple Silicon, no se requieren optimizaciones específicas.")
        return recommendations
    
    # Verificar PyTorch
    pytorch_status = get_pytorch_status()
    if not pytorch_status["installed"]:
        recommendations.append(
            "Instalar PyTorch optimizado para M2: "
            "pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu"
        )
    elif not pytorch_status["optimized_for_m2"]:
        recommendations.append(
            "Actualizar PyTorch a la versión optimizada para M2: "
            "pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu"
        )
    
    # Verificar configuración de Python
    if sys.version_info < (3, 9):
        recommendations.append("Actualizar a Python 3.9 o superior para mejor rendimiento en M2.")
    
    # Verificar configuración de variables de entorno
    if not os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK"):
        recommendations.append("Establecer PYTORCH_ENABLE_MPS_FALLBACK=1 para mejor compatibilidad.")
    
    return recommendations

def setup_m2_environment() -> bool:
    """Configura el entorno para optimizar el rendimiento en Mac M2."""
    if not is_apple_silicon():
        print("Este sistema no es Apple Silicon, no se aplicarán optimizaciones específicas.")
        return False
    
    # Configurar variables de entorno para PyTorch MPS
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    
    # Configurar paralelismo para NumPy y otros
    os.environ["OMP_NUM_THREADS"] = "8"  # Ajustar según el número de núcleos del M2
    
    # Configurar memoria para operaciones
    os.environ["MALLOC_ARENA_MAX"] = "2"  # Limitar el uso de memoria
    
    print("✅ Entorno optimizado para Mac M2")
    
    # Mostrar recomendaciones adicionales
    recommendations = get_optimization_recommendations()
    if recommendations:
        print("\nRecomendaciones adicionales:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    
    return True

def get_optimal_batch_size() -> int:
    """Determina el tamaño de batch óptimo para operaciones en M2."""
    if not is_apple_silicon():
        return 32  # Valor por defecto para sistemas no M2
    
    # Obtener información del dispositivo
    device_info = get_device_info()
    memory_gb = device_info.get("memory_gb", 8)
    
    # Ajustar batch size según la memoria disponible
    if memory_gb >= 32:
        return 64
    elif memory_gb >= 16:
        return 32
    else:
        return 16

def get_optimal_processes() -> int:
    """Determina el número óptimo de procesos paralelos para M2."""
    if not is_apple_silicon():
        return 4  # Valor por defecto para sistemas no M2
    
    # En M2, normalmente 8 núcleos (4 eficientes + 4 de rendimiento)
    # Usar n_cores - 1 para dejar un núcleo libre para el sistema
    try:
        import multiprocessing
        return max(1, multiprocessing.cpu_count() - 1)
    except:
        return 4  # Valor conservador si no se puede determinar

# Aplicar optimizaciones automáticamente si se importa este módulo
if is_apple_silicon():
    print("Detectado Mac con Apple Silicon. Aplicando optimizaciones automáticas...")
    setup_m2_environment()
