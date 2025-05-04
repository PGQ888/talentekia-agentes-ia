"""
Clase base para todos los agentes de IA en el sistema
"""
import os
import logging
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

class BaseAgent:
    """Clase base para todos los agentes de IA en el sistema"""
    def __init__(self, name="BaseAgent", config=None):
        """
        Inicializa un agente base con configuración predeterminada
        Args:
            name (str): Nombre del agente
            config (dict): Configuración del agente
        """
        self.name = name
        self.config = config or {}
        self.is_running = False
        self.last_error = None
        self.initialized = False
        self.completion_tokens = 0
        self.prompt_tokens = 0
        self.total_cost = 0.0
        self.status = "ready"  # Estado del agente: ready, running, error, completed
        self.last_run = None
        
        # Configurar logging
        self.logger = logging.getLogger(f"TalentekIA-{name}")
        self.logger.setLevel(logging.INFO)
        
        # Configurar rutas de salida
        self.output_dir = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs"))
        self.output_dir.mkdir(exist_ok=True)
        
        # Obtener nombres de archivos de salida
        output_files = self.config.get("output_files", {})
        self.csv_filename = output_files.get("csv", f"{name.lower().replace(' ', '_')}.csv")
        self.md_filename = output_files.get("markdown", f"{name.lower().replace(' ', '_')}.md")
        
        # Rutas completas a los archivos de salida
        self.csv_path = self.output_dir / self.csv_filename
        self.md_path = self.output_dir / self.md_filename
    
    def initialize(self):
        """Inicializa el agente y sus recursos"""
        try:
            self.logger.info(f"Inicializando agente {self.name}")
            self.initialized = True
            return True
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error al inicializar agente: {e}")
            return False
    
    @abstractmethod
    def execute(self):
        """
        Ejecuta el agente para realizar su tarea principal
        Returns:
            bool: True si la ejecución fue exitosa, False en caso contrario
        """
        pass
    
    def process_data(self, data):
        """
        Procesa los datos obtenidos
        Args:
            data: Datos a procesar
        Returns:
            pd.DataFrame: DataFrame con los resultados procesados
        """
        # Implementación por defecto
        return pd.DataFrame(data) if data else pd.DataFrame()
    
    def generate_report(self, df):
        """
        Genera un informe en formato Markdown a partir de los datos procesados
        Args:
            df: DataFrame con los datos procesados
        Returns:
            str: Informe en formato Markdown
        """
        # Implementación por defecto
        report = f"# Informe del Agente {self.name}\n\n"
        report += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if df is not None and not df.empty:
            report += "## Datos Procesados\n\n"
            report += f"Total de registros: {len(df)}\n\n"
            report += "### Primeras filas\n\n"
            report += df.head().to_markdown() + "\n\n"
        else:
            report += "No hay datos disponibles.\n\n"
        
        return report
    
    def save_results(self, df, report):
        """
        Guarda los resultados en archivos CSV y Markdown
        Args:
            df: DataFrame con los resultados
            report: Informe en formato Markdown
        Returns:
            Tuple[bool, bool]: (éxito_csv, éxito_md)
        """
        csv_success = False
        md_success = False
        
        try:
            # Guardar CSV
            if df is not None and not df.empty:
                df.to_csv(self.csv_path, index=False)
                csv_success = True
                self.logger.info(f"Resultados guardados en {self.csv_path}")
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error al guardar CSV: {str(e)}")
        
        try:
            # Guardar Markdown
            with open(self.md_path, "w", encoding="utf-8") as f:
                f.write(report)
            md_success = True
            self.logger.info(f"Informe guardado en {self.md_path}")
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error al guardar informe Markdown: {str(e)}")
        
        return csv_success, md_success
    
    def get_status(self):
        """
        Obtiene el estado actual del agente
        Returns:
            dict: Estado actual del agente
        """
        return {
            "name": self.name,
            "running": self.is_running,
            "initialized": self.initialized,
            "last_error": self.last_error,
            "completion_tokens": self.completion_tokens,
            "prompt_tokens": self.prompt_tokens,
            "total_cost": self.total_cost,
            "status": self.status,  # Asegurar que esta clave exista
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "csv_path": str(self.csv_path),
            "md_path": str(self.md_path),
            "csv_exists": self.csv_path.exists(),
            "md_exists": self.md_path.exists(),
            "update_frequency": self.config.get("update_frequency", "Manual")
        }
    
    def cleanup(self):
        """Limpia recursos utilizados por el agente"""
        self.logger.info(f"Limpiando recursos del agente {self.name}")
        return True