"""
Agente para gestión de finanzas personales
Este agente se encarga de analizar y proporcionar recomendaciones financieras
"""
import os
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# Importar la clase base
from src.agents.base_agent import BaseAgent
from src.utils.env_loader import env

class FinanzasPersonalesAgent(BaseAgent):
    """Agente para análisis y recomendaciones de finanzas personales"""
    
    def __init__(self, agent_id: str = "finanzas_personales", config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el agente de finanzas personales
        
        Args:
            agent_id: Identificador del agente
            config: Configuración específica (opcional)
        """
        super().__init__(agent_id, config)
        self.logger = logging.getLogger("TalentekIA-FinanzasPersonales")
        
        # Estado del agente
        self.status = "ready"
        self.last_execution = None
        self.data_path = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                           "..", "data", "finanzas"))
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    def run(self) -> bool:
        """
        Ejecuta el flujo principal del agente
        
        Returns:
            bool: True si la ejecución fue exitosa
        """
        self.logger.info("Iniciando agente de Finanzas Personales")
        self.status = "running"
        
        try:
            # Simulación de análisis financiero
            self.logger.info("Analizando datos financieros")
            
            # Datos de ejemplo (reemplazar con conexión a datos reales)
            self.results = {
                "periodo": "Mayo 2025",
                "resumen": {
                    "ingresos_totales": 8500,
                    "gastos_totales": 5200,
                    "ahorro": 3300,
                    "tasa_ahorro": 38.8
                },
                "categorias_gastos": [
                    {"categoria": "Vivienda", "monto": 1800, "porcentaje": 34.6},
                    {"categoria": "Alimentación", "monto": 950, "porcentaje": 18.3},
                    {"categoria": "Transporte", "monto": 450, "porcentaje": 8.7},
                    {"categoria": "Entretenimiento", "monto": 600, "porcentaje": 11.5},
                    {"categoria": "Servicios", "monto": 320, "porcentaje": 6.2},
                    {"categoria": "Otros", "monto": 1080, "porcentaje": 20.7}
                ],
                "recomendaciones": [
                    {"tipo": "Ahorro", "descripcion": "Incrementar fondo de emergencia", "impacto": "Alto"},
                    {"tipo": "Inversión", "descripcion": "Diversificar cartera en ETFs", "impacto": "Medio"},
                    {"tipo": "Gasto", "descripcion": "Reducir gastos en categoría 'Otros'", "impacto": "Alto"}
                ],
                "proyeccion_anual": {
                    "ahorro_proyectado": 39600,
                    "patrimonio_fin_año": 152000
                }
            }
            
            self.last_execution = datetime.now()
            self.status = "completed"
            return True
            
        except Exception as e:
            self.logger.error(f"Error en la ejecución del agente de finanzas personales: {str(e)}", exc_info=True)
            self.status = "error"
            return False
    
    def process_data(self, data: Any) -> pd.DataFrame:
        """
        Procesa los datos obtenidos
        
        Args:
            data: Datos a procesar
            
        Returns:
            pd.DataFrame: DataFrame con los datos procesados
        """
        # Procesar categorías de gastos
        if "categorias_gastos" in data:
            df = pd.DataFrame(data["categorias_gastos"])
            # Ordenar por monto descendente
            df = df.sort_values(by="monto", ascending=False)
            return df
        
        return pd.DataFrame(columns=["categoria", "monto", "porcentaje"])
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Genera un informe en formato Markdown
        
        Args:
            df: DataFrame con los datos procesados
            
        Returns:
            str: Informe en formato Markdown
        """
        # Generar informe básico
        report = f"""# Informe de Finanzas Personales - {self.results.get('periodo', 'N/A')}
        
## Resumen Financiero

- **Ingresos totales**: ${self.results['resumen'].get('ingresos_totales', 0):,.2f}
- **Gastos totales**: ${self.results['resumen'].get('gastos_totales', 0):,.2f}
- **Ahorro**: ${self.results['resumen'].get('ahorro', 0):,.2f}
- **Tasa de ahorro**: {self.results['resumen'].get('tasa_ahorro', 0)}%

## Distribución de Gastos

| Categoría | Monto ($) | Porcentaje (%) |
|-----------|-----------|----------------|
"""
        
        # Añadir distribución de gastos
        for _, row in df.iterrows():
            report += f"| {row['categoria']} | ${row['monto']:,.2f} | {row['porcentaje']}% |\n"
        
        # Añadir recomendaciones
        report += """
## Recomendaciones Financieras

"""
        for i, rec in enumerate(self.results.get('recomendaciones', []), 1):
            report += f"### {i}. {rec.get('descripcion')}\n"
            report += f"- **Tipo**: {rec.get('tipo')}\n"
            report += f"- **Impacto**: {rec.get('impacto')}\n\n"
        
        # Añadir proyección anual
        report += f"""
## Proyección Anual

- **Ahorro proyectado**: ${self.results['proyeccion_anual'].get('ahorro_proyectado', 0):,.2f}
- **Patrimonio estimado a fin de año**: ${self.results['proyeccion_anual'].get('patrimonio_fin_año', 0):,.2f}

"""
        
        # Añadir fecha del informe
        report += f"\n\n*Informe generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
        
        return report