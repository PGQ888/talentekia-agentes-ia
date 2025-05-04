"""
Configuración personal para TalentekIA en Mac M2
Este archivo contiene configuraciones específicas para uso personal en Mac con chip M2
"""

import os
import multiprocessing

# Configuración de rendimiento para Mac M2
MAC_M2_CONFIG = {
    # Rendimiento general
    "performance_mode": "balanced",  # Opciones: eco, balanced, performance
    
    # Configuración de modelos
    "default_model": "gpt-4o",  # Modelo principal para consultas
    "fallback_model": "gpt-3.5-turbo",  # Modelo de respaldo
    "local_model_enabled": False,  # Habilitar modelos locales
    
    # Configuración de procesamiento
    "max_parallel_processes": multiprocessing.cpu_count() - 1,
    "batch_size": 8,  # Tamaño de lote para procesamiento de datos
    "memory_limit": "8G",  # Límite de memoria para operaciones intensivas
    
    # Configuración de agentes
    "agent_timeout": 3600,  # Tiempo máximo de ejecución por agente (segundos)
    "auto_retry": True,  # Reintentar automáticamente en caso de error
    "max_retries": 3,  # Número máximo de reintentos
    
    # Configuración de interfaz
    "theme": "light",  # Tema de la interfaz (light, dark, auto)
    "sidebar_collapsed": False,  # Colapsar sidebar por defecto
    "show_debug_info": False,  # Mostrar información de depuración
    
    # Configuración de almacenamiento
    "cache_dir": "~/.cache/talentekia",
    "max_cache_size": "1G",  # Tamaño máximo de caché
    "clean_cache_on_startup": True,  # Limpiar caché al iniciar
    
    # Configuración de notificaciones
    "notifications_enabled": True,
    "notification_sound": True,
    "notification_level": "important",  # all, important, critical
}

def apply_personal_settings():
    """Aplica la configuración personal al entorno"""
    # Configurar variables de entorno
    os.environ["TALENTEKIA_PERFORMANCE_MODE"] = MAC_M2_CONFIG["performance_mode"]
    os.environ["TALENTEKIA_DEFAULT_MODEL"] = MAC_M2_CONFIG["default_model"]
    
    # Configurar límites de recursos
    os.environ["TALENTEKIA_MEMORY_LIMIT"] = MAC_M2_CONFIG["memory_limit"]
    os.environ["TALENTEKIA_MAX_PROCESSES"] = str(MAC_M2_CONFIG["max_parallel_processes"])
    
    # Configurar caché
    if MAC_M2_CONFIG["clean_cache_on_startup"]:
        cache_dir = os.path.expanduser(MAC_M2_CONFIG["cache_dir"])
        if os.path.exists(cache_dir):
            import shutil
            try:
                for item in os.listdir(cache_dir):
                    if item.startswith("temp_"):
                        item_path = os.path.join(cache_dir, item)
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
            except Exception as e:
                print(f"Error al limpiar caché: {e}")
    
    print("✓ Configuración personal aplicada")
    
    return True

# Aplicar configuración al importar el módulo
if __name__ == "__main__":
    apply_personal_settings()