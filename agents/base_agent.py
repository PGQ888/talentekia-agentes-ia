"""
Clase base para todos los agentes de TalentekIA
Proporciona la estructura y funcionalidades comunes para todos los agentes
"""
import os
import logging
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# Importar módulos del proyecto
from scripts.env_loader import env

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseAgent(ABC):
    """Clase base abstracta para todos los agentes del sistema"""
    
    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa un nuevo agente
        
        Args:
            agent_id: Identificador único del agente
            config: Configuración específica del agente (opcional)
        """
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"TalentekIA-{agent_id}")
        
        # Cargar configuración
        from agents.config import get_agent_config
        self.config = config or get_agent_config(agent_id) or {}
        
        # Configurar rutas de salida
        self.output_dir = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs"))
        self.output_dir.mkdir(exist_ok=True)
        
        # Obtener nombres de archivos de salida
        output_files = self.config.get("output_files", {})
        self.csv_filename = output_files.get("csv", f"{agent_id}.csv")
        self.md_filename = output_files.get("markdown", f"{agent_id}.md")
        
        # Rutas completas a los archivos de salida
        self.csv_path = self.output_dir / self.csv_filename
        self.md_path = self.output_dir / self.md_filename
        
        # Inicializar estado
        self.last_run = None
        self.is_running = False
        self.results = None
    
    @abstractmethod
    def run(self) -> bool:
        """
        Ejecuta el agente para realizar su tarea principal
        
        Returns:
            bool: True si la ejecución fue exitosa, False en caso contrario
        """
        pass
    
    @abstractmethod
    def process_data(self, data: Any) -> pd.DataFrame:
        """
        Procesa los datos obtenidos
        
        Args:
            data: Datos a procesar
            
        Returns:
            pd.DataFrame: DataFrame con los resultados procesados
        """
        pass
    
    @abstractmethod
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Genera un informe en formato Markdown a partir de los datos procesados
        
        Args:
            df: DataFrame con los datos procesados
            
        Returns:
            str: Informe en formato Markdown
        """
        pass
    
    def save_results(self, df: pd.DataFrame, report: str) -> Tuple[bool, bool]:
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
            df.to_csv(self.csv_path, index=False)
            csv_success = True
            self.logger.info(f"Resultados guardados en {self.csv_path}")
        except Exception as e:
            self.logger.error(f"Error al guardar CSV: {str(e)}")
        
        try:
            # Guardar Markdown
            with open(self.md_path, "w", encoding="utf-8") as f:
                f.write(report)
            md_success = True
            self.logger.info(f"Informe guardado en {self.md_path}")
        except Exception as e:
            self.logger.error(f"Error al guardar informe Markdown: {str(e)}")
        
        return csv_success, md_success
    
    def execute(self) -> bool:
        """
        Ejecuta el flujo completo del agente: obtención de datos, procesamiento y generación de informes
        
        Returns:
            bool: True si la ejecución completa fue exitosa, False en caso contrario
        """
        self.logger.info(f"Iniciando ejecución del agente {self.agent_id}")
        self.is_running = True
        success = False
        
        try:
            # Ejecutar el agente
            run_success = self.run()
            
            if run_success and self.results is not None:
                # Procesar datos
                df = self.process_data(self.results)
                
                # Generar informe
                report = self.generate_report(df)
                
                # Guardar resultados
                csv_success, md_success = self.save_results(df, report)
                
                success = csv_success and md_success
            else:
                self.logger.error("La ejecución del agente no produjo resultados")
        
        except Exception as e:
            self.logger.error(f"Error durante la ejecución del agente: {str(e)}", exc_info=True)
        
        finally:
            self.is_running = False
            self.last_run = datetime.now()
            self.logger.info(f"Ejecución del agente {self.agent_id} finalizada. Éxito: {success}")
            
            return success
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del agente
        
        Returns:
            Dict[str, Any]: Estado del agente
        """
        return {
            "id": self.agent_id,
            "name": self.config.get("name", self.agent_id.capitalize()),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "is_running": self.is_running,
            "csv_path": str(self.csv_path),
            "md_path": str(self.md_path),
            "csv_exists": self.csv_path.exists(),
            "md_exists": self.md_path.exists(),
            "update_frequency": self.config.get("update_frequency", "Manual")
        }