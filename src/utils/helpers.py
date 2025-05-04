"""
Módulo de funciones auxiliares para los agentes de TalentekIA.
Este módulo contiene funciones de utilidad que pueden ser usadas por diferentes agentes.
"""

import os
import pandas as pd
from typing import Dict, List, Any, Optional
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_directory_exists(directory_path: str) -> None:
    """
    Asegura que un directorio exista, creándolo si es necesario.
    
    Args:
        directory_path: Ruta del directorio a verificar/crear
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Directorio creado: {directory_path}")

def save_dataframe(df: pd.DataFrame, file_path: str, index: bool = False) -> None:
    """
    Guarda un DataFrame en un archivo CSV.
    
    Args:
        df: DataFrame a guardar
        file_path: Ruta donde guardar el archivo
        index: Si se debe incluir el índice en el CSV
    """
    ensure_directory_exists(os.path.dirname(file_path))
    df.to_csv(file_path, index=index, encoding='utf-8')
    logger.info(f"DataFrame guardado en: {file_path}")

def load_dataframe(file_path: str) -> Optional[pd.DataFrame]:
    """
    Carga un DataFrame desde un archivo CSV.
    
    Args:
        file_path: Ruta del archivo a cargar
        
    Returns:
        DataFrame cargado o None si el archivo no existe
    """
    if not os.path.exists(file_path):
        logger.warning(f"El archivo no existe: {file_path}")
        return None
    
    return pd.read_csv(file_path, encoding='utf-8')

def format_currency(value: float) -> str:
    """
    Formatea un valor como moneda (€).
    
    Args:
        value: Valor a formatear
        
    Returns:
        Cadena formateada como moneda
    """
    return f"{value:,.2f} €"