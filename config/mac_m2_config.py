"""
Configuraciones específicas para optimizar TalentekIA en Mac M2/M1
Este archivo contiene ajustes y optimizaciones para aprovechar al máximo el chip Apple Silicon
"""
import os
import platform
import logging
logger = logging.getLogger("TalentekIA-M2Config")

# Configuración de optimizaciones para M1/M2
M2_OPTIMIZATIONS = {
    # PyTorch configuraciones
    "PYTORCH_ENABLE_MPS_FALLBACK": "1",
    "PYTORCH_DEVICE": "mps",
    # TensorFlow configuraciones
    "TF_ENABLE_ONEDNN_OPTS": "0",
    "TF_MPS_ALLOW_SOFT_PLACEMENT": "1",
    # Configuraciones de memoria
    "M2_MEMORY_LIMIT": "8192",  # Límite en MB (ajustar según RAM disponible)
    "M2_USE_MEMORY_EFFICIENT_ATTENTION": "1",
    # Configuraciones de rendimiento
    "M2_PERFORMANCE_MODE": "balanced",  # eco, balanced, performance
    "M2_USE_QUANTIZATION": "1",
    "M2_MODEL_PRECISION": "fp16"  # fp16, fp32
}

def is_apple_silicon():
    """Detecta si el sistema es Mac con Apple Silicon (M1/M2)"""
    return platform.system() == "Darwin" and platform.machine() == "arm64"

def apply_m2_optimizations(verbose=True):
    """
    Aplica todas las optimizaciones para Apple Silicon
    Args:
        verbose (bool): Si es True, muestra mensajes de log detallados
    Returns:
        dict: Estado de las optimizaciones aplicadas
    """
    if not is_apple_silicon():
        logger.warning("Este sistema no es Mac con Apple Silicon. No se aplicarán optimizaciones M2.")
        return {"applied": False, "reason": "not_apple_silicon"}
    
    logger.info("Aplicando optimizaciones para Apple Silicon (M1/M2)...")
    
    # Aplicar configuraciones de entorno
    for key, value in M2_OPTIMIZATIONS.items():
        os.environ[key] = value
        if verbose:
            logger.debug(f"Configurando {key}={value}")
    
    # Verificar disponibilidad de MPS para PyTorch
    mps_available = False
    try:
        import torch
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            mps_available = True
            logger.info("PyTorch MPS (Metal Performance Shaders) está disponible")
        else:
            logger.warning("PyTorch MPS no está disponible en este sistema")
    except (ImportError, AttributeError):
        logger.warning("No se pudo verificar MPS: PyTorch no está instalado o es incompatible")
    
    # Verificar optimizaciones para TensorFlow
    tf_optimized = False
    try:
        import tensorflow as tf
        if hasattr(tf, 'config') and hasattr(tf.config, 'list_physical_devices'):
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                tf_optimized = True
                logger.info(f"TensorFlow detectó {len(gpus)} dispositivos GPU")
            else:
                logger.warning("TensorFlow no detectó dispositivos GPU")
    except (ImportError, AttributeError):
        logger.warning("No se pudo verificar TensorFlow: no está instalado o es incompatible")
    
    return {
        "applied": True,
        "mps_available": mps_available,
        "tf_optimized": tf_optimized,
        "env_vars": {k: os.environ.get(k) for k in M2_OPTIMIZATIONS.keys()}
    }

def get_recommended_packages():
    """
    Retorna lista de paquetes recomendados para Mac M2
    Returns:
        list: Lista de paquetes recomendados para instalación
    """
    return [
        "tensorflow-macos",
        "tensorflow-metal",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "torchaudio>=2.0.0",
        "accelerate>=0.20.0"
    ]

def get_optimization_status():
    """
    Obtiene el estado actual de las optimizaciones
    Returns:
        dict: Estado de las optimizaciones
    """
    status = {
        "is_apple_silicon": is_apple_silicon(),
        "env_vars": {}
    }
    
    # Verificar variables de entorno
    for key in M2_OPTIMIZATIONS.keys():
        status["env_vars"][key] = os.environ.get(key, "no configurado")
    
    # Verificar PyTorch
    try:
        import torch
        status["pytorch"] = {
            "version": torch.__version__,
            "mps_available": hasattr(torch.backends, 'mps') and torch.backends.mps.is_available(),
            "mps_current_device": torch.device("mps") if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available() else None
        }
    except ImportError:
        status["pytorch"] = {"installed": False}
    
    # Verificar TensorFlow
    try:
        import tensorflow as tf
        gpus = []
        if hasattr(tf, 'config') and hasattr(tf.config, 'list_physical_devices'):
            gpus = tf.config.list_physical_devices('GPU')
        status["tensorflow"] = {
            "version": tf.__version__,
            "gpus_detected": len(gpus) > 0,
            "num_gpus": len(gpus)
        }
    except ImportError:
        status["tensorflow"] = {"installed": False}
    
    return status

# Aplicar optimizaciones automáticamente si se importa este módulo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = apply_m2_optimizations()
    print("=== Estado de Optimizaciones para Mac M2 ===")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    if result["applied"]:
        print("\n¡Optimizaciones para Mac M2 aplicadas correctamente!")
    else:
        print("\nNo se aplicaron optimizaciones. Este sistema no es Mac con Apple Silicon.")