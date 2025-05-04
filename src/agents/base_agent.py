"""
Clase base para todos los agentes del sistema Talentek.
"""

import os
import time
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple
from abc import ABC, abstractmethod

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
        self.name = agent_id  # Para compatibilidad con código anterior
        self.config = config or {}
        self.start_time = None
        self.end_time = None
        
        # Estado del agente
        self.is_running = False
        self.last_error = None
        self.initialized = False
        self.completion_tokens = 0
        self.prompt_tokens = 0
        self.total_cost = 0.0
        self.status = "ready"  # Estado del agente: ready, running, error, completed
        self.last_run = None
        
        # Configurar directorios de datos
        self.data_dir = Path("data")
        self.agent_data_dir = self.data_dir / agent_id
        self.ensure_directories()
        
        # Configurar logging
        self.logger = logging.getLogger(f"TalentekIA-{agent_id}")
        self.logger.setLevel(logging.INFO)
        
        # Optimizaciones para M2 si corresponde
        self.is_m2 = self._is_apple_silicon()
        if self.is_m2:
            self.batch_size = self._get_optimal_batch_size()
        else:
            self.batch_size = 32  # Valor por defecto
        
        # Obtener nombres de archivos de salida
        output_files = self.config.get("output_files", {})
        self.csv_filename = output_files.get("csv", f"{agent_id.lower().replace(' ', '_')}.csv")
        self.md_filename = output_files.get("markdown", f"{agent_id.lower().replace(' ', '_')}.md")
        
        # Rutas completas a los archivos de salida
        self.csv_path = self.agent_data_dir / self.csv_filename
        self.md_path = self.agent_data_dir / self.md_filename
    
    def ensure_directories(self) -> None:
        """Asegura que los directorios necesarios existan."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.agent_data_dir.mkdir(parents=True, exist_ok=True)
    
    def initialize(self):
        """Inicializa el agente y sus recursos"""
        try:
            self.logger.info(f"Inicializando agente {self.agent_id}")
            self.initialized = True
            return True
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error al inicializar agente: {e}")
            return False
    
    def run(self) -> Dict[str, Any]:
        """
        Ejecuta el agente y registra el tiempo de ejecución.
        
        Returns:
            Dict con los resultados de la ejecución
        """
        self.start_time = time.time()
        self.is_running = True
        self.status = "running"
        self.last_run = datetime.now()
        
        try:
            # Asegurar que el agente esté inicializado
            if not self.initialized:
                self.initialize()
            
            # Ejecutar la lógica principal del agente
            success = self.execute()
            
            # Si la ejecución fue exitosa, procesar los datos
            if success:
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
                
                self.status = "completed"
            else:
                result = {"success": False, "error": self.last_error or "Unknown error"}
                self.status = "error"
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error al ejecutar el agente {self.agent_id}: {str(e)}")
            result = {"success": False, "error": str(e)}
            self.status = "error"
        
        self.end_time = time.time()
        self.is_running = False
        result["duration"] = self.end_time - self.start_time
        result["tokens"] = {"completion": self.completion_tokens, "prompt": self.prompt_tokens}
        result["cost"] = self.total_cost
        
        return result
    
    def execute(self):
        """
        Ejecuta el agente para realizar su tarea principal.
        Debe ser implementado por las subclases.
        
        Returns:
            bool: True si la ejecución fue exitosa, False en caso contrario
        """
        # Implementación por defecto que llama a process_data
        try:
            data = self.process_data(None)
            return True
        except Exception as e:
            self.last_error = str(e)
            return False
    
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
        report = f"# Informe del Agente {self.agent_id}\n\n"
        report += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if df is not None and not df.empty:
            report += "## Datos Procesados\n\n"
            report += f"Total de registros: {len(df)}\n\n"
            report += "### Primeras filas\n\n"
            try:
                report += df.head().to_markdown() + "\n\n"
            except:
                report += str(df.head()) + "\n\n"
            
            report += "### Resumen estadístico\n\n"
            try:
                report += df.describe().to_markdown() + "\n\n"
            except:
                report += str(df.describe()) + "\n\n"
        else:
            report += "No hay datos disponibles.\n\n"
        
        return report
    
    def save_results(self, df: pd.DataFrame, report: str) -> None:
        """
        Guarda los resultados del agente.
        
        Args:
            df: DataFrame con los datos procesados
            report: Informe generado
        """
        csv_success = False
        md_success = False
        
        try:
            # Crear timestamp para los nombres de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Guardar DataFrame
            if df is not None and not df.empty:
                csv_path = self.agent_data_dir / f"{self.agent_id}_{timestamp}.csv"
                df.to_csv(csv_path, index=False)
                csv_success = True
                self.logger.info(f"Resultados guardados en {csv_path}")
                
                # Crear enlace simbólico al archivo más reciente
                latest_csv = self.agent_data_dir / f"{self.agent_id}_latest.csv"
                if latest_csv.exists():
                    latest_csv.unlink()
                try:
                    os.symlink(csv_path.name, latest_csv)
                except:
                    # En Windows los enlaces simbólicos pueden fallar
                    df.to_csv(latest_csv, index=False)
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error al guardar CSV: {str(e)}")
        
        try:
            # Guardar informe
            report_path = self.agent_data_dir / f"{self.agent_id}_{timestamp}.md"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)
            md_success = True
            self.logger.info(f"Informe guardado en {report_path}")
            
            # Crear enlace simbólico al informe más reciente
            latest_report = self.agent_data_dir / f"{self.agent_id}_latest.md"
            if latest_report.exists():
                latest_report.unlink()
            try:
                os.symlink(report_path.name, latest_report)
            except:
                # En Windows los enlaces simbólicos pueden fallar
                with open(latest_report, "w", encoding="utf-8") as f:
                    f.write(report)
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Error al guardar informe Markdown: {str(e)}")
    
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
            "name": self.name,
            "running": self.is_running,
            "initialized": self.initialized,
            "last_error": self.last_error,
            "has_data": latest_csv.exists(),
            "last_update": None,
            "enabled": self.config.get("enabled", False),
            "update_frequency": self.config.get("update_frequency", "daily"),
            "completion_tokens": self.completion_tokens,
            "prompt_tokens": self.prompt_tokens,
            "total_cost": self.total_cost,
            "status": self.status,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "csv_path": str(latest_csv),
            "md_path": str(latest_report),
            "csv_exists": latest_csv.exists(),
            "md_exists": latest_report.exists(),
        }
        
        if latest_csv.exists():
            status["last_update"] = datetime.fromtimestamp(latest_csv.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        return status
    
    def cleanup(self):
        """Limpia recursos utilizados por el agente"""
        self.logger.info(f"Limpiando recursos del agente {self.agent_id}")
        return True
    
    def _is_apple_silicon(self):
        """Detecta si el sistema es Apple Silicon (M1/M2)"""
        import platform
        return platform.system() == "Darwin" and platform.machine() == "arm64"
    
    def _get_optimal_batch_size(self):
        """Obtiene el tamaño de lote óptimo para Apple Silicon"""
        # Valores predeterminados optimizados para M1/M2
        return 16  # Un valor conservador para M1/M2