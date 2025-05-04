"""
Clase base para todos los agentes del sistema Talentek.
"""

import os
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List

from ..core.config import get_agent_config
from ..core.m2_optimizer import is_apple_silicon, get_optimal_batch_size

class BaseAgent:
    """Clase base para todos los agentes de Talentek."""
    
    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa un agente base.
        
        Args:
            agent_id: Identificador único del agente
            config: Configuración específica del agente (opcional)
        """
        self.agent_id = agent_id
        self.config = config or get_agent_config(agent_id)
        self.start_time = None
        self.end_time = None
        self.data_dir = Path(os.path.expanduser("~/.talentek/data"))
        self.agent_data_dir = self.data_dir / agent_id
        self.ensure_directories()
        
        # Optimizaciones para M2 si corresponde
        self.is_m2 = is_apple_silicon()
        if self.is_m2:
            self.batch_size = get_optimal_batch_size()
        else:
            self.batch_size = 32  # Valor por defecto
    
    def ensure_directories(self) -> None:
        """Asegura que los directorios necesarios existan."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.agent_data_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self) -> Dict[str, Any]:
        """
        Ejecuta el agente y registra el tiempo de ejecución.
        
        Returns:
            Dict con los resultados de la ejecución
        """
        self.start_time = time.time()
        
        try:
            # Obtener datos
            data = self.process_data(None)
            
            # Generar informe
            if isinstance(data, pd.DataFrame):
                report = self.generate_report(data)
                # Guardar resultados
                self.save_results(data, report)
                result = {"success": True, "data": data, "report": report}
            else:
                result = {"success": True, "data": data}
        except Exception as e:
            print(f"Error al ejecutar el agente {self.agent_id}: {str(e)}")
            result = {"success": False, "error": str(e)}
        
        self.end_time = time.time()
        result["duration"] = self.end_time - self.start_time
        
        return result
    
    def process_data(self, data: Any) -> Any:
        """
        Procesa los datos de entrada. Debe ser implementado por las subclases.
        
        Args:
            data: Datos de entrada para procesar
            
        Returns:
            Datos procesados
        """
        raise NotImplementedError("Las subclases deben implementar process_data")
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Genera un informe basado en los datos procesados.
        
        Args:
            df: DataFrame con los datos procesados
            
        Returns:
            Informe generado como string
        """
        return f"Informe del agente {self.agent_id}\n\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nResumen de datos:\n{df.describe().to_string()}"
    
    def save_results(self, df: pd.DataFrame, report: str) -> None:
        """
        Guarda los resultados del agente.
        
        Args:
            df: DataFrame con los datos procesados
            report: Informe generado
        """
        # Crear timestamp para los nombres de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar DataFrame
        csv_path = self.agent_data_dir / f"{self.agent_id}_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        
        # Guardar informe
        report_path = self.agent_data_dir / f"{self.agent_id}_{timestamp}.md"
        with open(report_path, "w") as f:
            f.write(report)
        
        # Crear enlaces simbólicos a los archivos más recientes
        latest_csv = self.agent_data_dir / f"{self.agent_id}_latest.csv"
        latest_report = self.agent_data_dir / f"{self.agent_id}_latest.md"
        
        # Eliminar enlaces anteriores si existen
        if latest_csv.exists():
            latest_csv.unlink()
        if latest_report.exists():
            latest_report.unlink()
        
        # Crear nuevos enlaces
        os.symlink(csv_path.name, latest_csv)
        os.symlink(report_path.name, latest_report)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del agente.
        
        Returns:
            Dict con información sobre el estado del agente
        """
        latest_csv = self.agent_data_dir / f"{self.agent_id}_latest.csv"
        latest_report = self.agent_data_dir / f"{self.agent_id}_latest.md"
        
        status = {
            "agent_id": self.agent_id,
            "has_data": latest_csv.exists(),
            "last_update": None,
            "enabled": self.config.get("enabled", False),
            "update_frequency": self.config.get("update_frequency", "daily")
        }
        
        if latest_csv.exists():
            status["last_update"] = datetime.fromtimestamp(latest_csv.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        return status
