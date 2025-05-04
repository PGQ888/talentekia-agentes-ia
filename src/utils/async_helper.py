"""
Utilidades para manejar operaciones asíncronas en TalentekIA
Soluciona problemas específicos con el bucle de eventos de asyncio en Python 3.12 y Streamlit
"""

import os
import sys
import asyncio
import logging
import warnings
from functools import wraps

logger = logging.getLogger("TalentekIA-AsyncHelper")

def is_python_312_or_higher():
    """Detecta si estamos en Python 3.12 o superior"""
    version_info = sys.version_info
    return version_info.major == 3 and version_info.minor >= 12

def streamlit_asyncio_patch():
    """
    Aplica un parche para el problema de 'no running event loop' en Python 3.12 con Streamlit
    Debe llamarse al inicio de la aplicación
    """
    if is_python_312_or_higher():
        # En Python 3.12, asyncio.get_running_loop() falla si no hay un bucle en ejecución
        # Esto causa problemas con Streamlit porque intenta usar get_running_loop()
        # Esta función añade un bucle temporal para evitar el error
        logger.info("Aplicando parche para asyncio en Python 3.12 con Streamlit")
        
        # Método original
        original_get_running_loop = asyncio.get_running_loop
        
        # Sobreescribir el método con nuestra versión
        def patched_get_running_loop():
            try:
                return original_get_running_loop()
            except RuntimeError:
                # Si no hay un bucle en ejecución, crear uno temporal
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                warnings.warn(
                    "Creando un bucle de eventos temporal para compatibilidad con Streamlit en Python 3.12",
                    RuntimeWarning
                )
                return loop
        
        # Aplicar el parche
        asyncio.get_running_loop = patched_get_running_loop
        
        logger.info("Parche para asyncio aplicado correctamente")

def run_async(func):
    """
    Decorador para ejecutar funciones asíncronas de forma segura
    
    Uso:
        @run_async
        async def my_async_function():
            await asyncio.sleep(1)
            return "Done"
            
        result = my_async_function()  # Llamada síncrona a función asíncrona
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Crear un nuevo bucle o usar el existente
        try:
            loop = asyncio.get_running_loop()
            is_new_loop = False
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            is_new_loop = True
        
        try:
            result = loop.run_until_complete(func(*args, **kwargs))
        finally:
            # Cerrar el bucle si lo creamos nosotros
            if is_new_loop:
                loop.close()
                
        return result
    
    return wrapper

# Aplicar el parche automáticamente cuando se importa este módulo
if "streamlit" in sys.modules:
    streamlit_asyncio_patch()