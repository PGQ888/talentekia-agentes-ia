"""
Utilidad para optimizar TalentekIA en Mac con chip M2/M1
Detecta automáticamente y aplica optimizaciones para mejorar el rendimiento
"""
import os
import sys
import logging
import importlib.util
from pathlib import Path

# Configurar logger
logger = logging.getLogger("TalentekIA-M2Optimizer")

def setup_m2_environment():
    """
    Configura automáticamente el entorno para Mac M2/M1
    Returns:
        dict: Resultado de la configuración
    """
    # Determinar ruta del módulo de configuración
    root_dir = Path(__file__).parent.parent.parent
    config_path = root_dir / "config" / "mac_m2_config.py"
    
    if not config_path.exists():
        logger.warning(f"Archivo de configuración M2 no encontrado en {config_path}")
        return {"status": "error", "message": "Archivo de configuración no encontrado"}
    
    # Cargar dinámicamente el módulo de configuración
    try:
        spec = importlib.util.spec_from_file_location("mac_m2_config", config_path)
        m2_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m2_config)
        
        # Verificar si estamos en Mac M2/M1
        if not m2_config.is_apple_silicon():
            logger.info("No se detectó Mac con Apple Silicon. No se aplicarán optimizaciones.")
            return {"status": "skipped", "message": "No es Mac M2/M1"}
        
        # Aplicar optimizaciones
        result = m2_config.apply_m2_optimizations()
        
        # Verificar paquetes recomendados
        recommended_packages = m2_config.get_recommended_packages()
        missing_packages = []
        
        for package in recommended_packages:
            package_name = package.split('>=')[0]
            try:
                importlib.import_module(package_name)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.warning(f"Paquetes recomendados no instalados: {', '.join(missing_packages)}")
            logger.info("Instala los paquetes con: pip install " + " ".join(missing_packages))
        
        return {
            "status": "success", 
            "optimizations": result,
            "missing_packages": missing_packages
        }
    
    except Exception as e:
        logger.error(f"Error al aplicar optimizaciones M2: {str(e)}", exc_info=True)
        return {"status": "error", "message": str(e)}

def get_device_info():
    """
    Obtiene información detallada sobre el dispositivo optimizado
    Returns:
        dict: Información del dispositivo
    """
    info = {
        "system": os.uname().sysname,
        "node": os.uname().nodename,
        "release": os.uname().release,
        "machine": os.uname().machine
    }
    
    # Información detallada para Mac
    if info["system"] == "Darwin":
        try:
            # Obtener modelo exacto
            import subprocess
            model = subprocess.check_output(["sysctl", "-n", "hw.model"]).decode("utf-8").strip()
            info["model"] = model
            
            # Obtener memoria
            memory = subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode("utf-8").strip()
            info["memory"] = int(memory) // (1024 * 1024 * 1024)  # Convertir a GB
            
            # Verificar si es Apple Silicon
            if info["machine"] == "arm64":
                info["processor_type"] = "Apple Silicon"
                
                # Detectar si es M1 o M2
                if "Mac" in model:
                    if any(x in model for x in ["Mac14", "Mac13"]):
                        info["chip"] = "M2"
                    elif any(x in model for x in ["Mac12", "Mac11", "Mac10"]):
                        info["chip"] = "M1"
                    else:
                        info["chip"] = "Desconocido (Apple Silicon)"
        
        except Exception as e:
            logger.error(f"Error al obtener información detallada: {str(e)}")
    
    return info

def get_pytorch_status():
    """
    Verifica el estado de PyTorch y su configuración para M2
    Returns:
        dict: Estado de PyTorch
    """
    status = {"installed": False}
    
    try:
        import torch
        status = {
            "installed": True,
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available() if hasattr(torch, 'cuda') else False,
            "default_device": str(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        }
        
        # Verificar MPS (Metal Performance Shaders)
        if hasattr(torch.backends, 'mps'):
            status["mps_built"] = torch.backends.mps.is_built()
            status["mps_available"] = torch.backends.mps.is_available()
            
            if torch.backends.mps.is_available():
                status["default_device"] = "mps"
                status["recommended_device"] = "torch.device('mps')"
    
    except ImportError:
        pass
    
    return status

def get_optimization_recommendations():
    """
    Genera recomendaciones específicas para Mac M2
    Returns:
        list: Recomendaciones para optimizar el rendimiento
    """
    recommendations = [
        "Instala la versión más reciente de PyTorch compatible con MPS",
        "Usa tensorflow-macos y tensorflow-metal para TensorFlow optimizado",
        "Establece el tamaño de batch adecuado para evitar problemas de memoria",
        "Usa modelos cuantizados cuando sea posible",
        "Activa Memory-Efficient Attention para modelos grandes"
    ]
    
    # Recomendaciones específicas según paquetes instalados
    try:
        import torch
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            recommendations.append("Usa 'device = torch.device(\"mps\")' para PyTorch")
    except ImportError:
        pass
    
    try:
        import tensorflow
        recommendations.append("Configura TensorFlow con tf.config.experimental.set_visible_devices")
    except ImportError:
        pass
    
    return recommendations

if __name__ == "__main__":
    # Configurar logging para uso como script
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Ejecutar configuración
    print("=== TalentekIA M2 Optimizer ===")
    result = setup_m2_environment()
    print(f"Resultado: {result['status']}")
    
    # Mostrar información del dispositivo
    device_info = get_device_info()
    print(f"\nDispositivo: {device_info.get('system')} {device_info.get('machine')}")
    
    if device_info.get('processor_type') == "Apple Silicon":
        print(f"Chip detectado: {device_info.get('chip', 'Apple Silicon')}")
        print(f"Modelo: {device_info.get('model', 'Desconocido')}")
        print(f"Memoria: {device_info.get('memory', 'Desconocido')} GB")
    
    # Mostrar estado de frameworks
    pytorch_status = get_pytorch_status()
    if pytorch_status["installed"]:
        print(f"\nPyTorch {pytorch_status['version']}")
        print(f"MPS disponible: {pytorch_status.get('mps_available', False)}")
        print(f"Dispositivo recomendado: {pytorch_status.get('recommended_device', 'cpu')}")
    
    # Mostrar recomendaciones
    print("\nRecomendaciones:")
    for i, rec in enumerate(get_optimization_recommendations(), 1):
        print(f"{i}. {rec}")
    else:
        print("Este sistema no es Mac con Apple Silicon.")