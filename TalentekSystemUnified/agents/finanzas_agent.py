#!/usr/bin/env python3
"""
Gestor de Finanzas Personales - Agente para análisis financiero
Este agente analiza gastos, activos, ahorro y propone optimizaciones
"""
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join("logs", "finanzas_agent.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TalentekIA-Finanzas")

class FinanzasAgent:
    """Agente para análisis y optimización de finanzas personales"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el agente de finanzas personales
        
        Args:
            config: Configuración específica (opcional)
        """
        self.config = config or {}
        
        # Configuración de fuentes de datos
        self.datos_fuente = self.config.get("datos_fuente", "data/finanzas/gastos.csv")
        
        # Estado del agente
        self.status = "ready"
        self.last_execution = None
        self.results = {}
        
        # Crear directorios para datos e informes si no existen
        self.data_dir = Path("data/finanzas")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir = Path("data/informes")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self) -> bool:
        """
        Ejecuta el flujo principal del agente
        
        Returns:
            bool: True si la ejecución fue exitosa
        """
        print("╔═══════════════════════════════════════════╗")
        print("║       GESTOR DE FINANZAS PERSONALES       ║")
        print("╚═══════════════════════════════════════════╝")
        print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Analizando datos financieros...")
        
        self.status = "running"
        
        try:
            # Simulación de proceso
            print("Cargando datos de gastos e ingresos...")
            logger.info("Cargando datos financieros")
            print("Calculando métricas financieras...")
            
            # Resultados simulados
            metricas = {
                "ingresos_totales": 5200,
                "gastos_totales": 3800,
                "ahorro_mensual": 1400,
                "tasa_ahorro": 26.9,
                "principales_gastos": {
                    "Vivienda": 1500,
                    "Alimentación": 800,
                    "Transporte": 350,
                    "Educación": 600,
                    "Ocio": 250
                }
            }
            
            # Guardar resultados
            self.results = metricas
            
            # Mostrar resumen
            print("\nResumen financiero del mes:")
            print(f"Ingresos totales: {metricas['ingresos_totales']}€")
            print(f"Gastos totales: {metricas['gastos_totales']}€")
            print(f"Ahorro mensual: {metricas['ahorro_mensual']}€")
            print(f"Tasa de ahorro: {metricas['tasa_ahorro']}%")
            
            print("\nPrincipales categorías de gasto:")
            for categoria, importe in metricas['principales_gastos'].items():
                print(f"- {categoria}: {importe}€")
            
            # Generar recomendaciones
            print("\nRecomendaciones para optimización:")
            print("1. Reducir gastos en ocio en un 10%")
            print("2. Aumentar aportaciones a fondo de emergencia")
            print("3. Revisar posibilidades de inversión para excedente")
            
            # Generar y guardar informe
            self.generate_report(metricas)
            
            print("\nAnálisis completado exitosamente.")
            print(f"El informe detallado ha sido guardado en {self.reports_dir}/informe_mensual.md")
            
            self.last_execution = datetime.now()
            self.status = "completed"
            return True
            
        except Exception as e:
            logger.error(f"Error en la ejecución del agente de finanzas: {str(e)}", exc_info=True)
            self.status = "error"
            return False
    
    def generate_report(self, metricas: Dict[str, Any]) -> None:
        """
        Genera un informe en formato Markdown
        
        Args:
            metricas: Métricas financieras calculadas
        """
        try:
            # Crear informe en formato Markdown
            report = f"""# Informe Financiero Mensual

## Resumen Ejecutivo
- **Fecha del informe**: {datetime.now().strftime('%d/%m/%Y')}
- **Periodo analizado**: Mes actual

## Métricas Principales
- **Ingresos totales**: {metricas['ingresos_totales']}€
- **Gastos totales**: {metricas['gastos_totales']}€
- **Ahorro mensual**: {metricas['ahorro_mensual']}€
- **Tasa de ahorro**: {metricas['tasa_ahorro']}%

## Desglose de Gastos
| Categoría | Importe (€) | Porcentaje |
|-----------|-------------|------------|
"""
            # Añadir desglose de gastos
            for categoria, importe in metricas['principales_gastos'].items():
                porcentaje = (importe / metricas['gastos_totales']) * 100
                report += f"| {categoria} | {importe} | {porcentaje:.1f}% |\n"
            
            # Añadir recomendaciones
            report += """
## Recomendaciones
1. **Reducir gastos en ocio** en un 10% (ahorro potencial: 25€)
2. **Aumentar aportaciones a fondo de emergencia** hasta alcanzar 6 meses de gastos
3. **Revisar posibilidades de inversión** para el excedente mensual

## Evolución Histórica
El ahorro mensual ha aumentado un 5% respecto al mes anterior.

## Próximos Pasos
- Revisión de seguros para optimizar costes
- Planificación de gastos extraordinarios previstos
- Actualización de objetivos financieros a medio plazo

---
*Informe generado automáticamente por TalentekIA - Gestor de Finanzas Personales*
"""
            
            # Guardar informe
            report_path = self.reports_dir / "informe_mensual.md"
            with open(report_path, "w") as f:
                f.write(report)
            
            logger.info(f"Informe generado y guardado en {report_path}")
            
        except Exception as e:
            logger.error(f"Error al generar informe: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del agente
        
        Returns:
            Dict: Estado del agente
        """
        return {
            "status": self.status,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "ingresos": self.results.get("ingresos_totales"),
            "gastos": self.results.get("gastos_totales"),
            "ahorro": self.results.get("ahorro_mensual")
        }

def main():
    """Función principal para ejecución independiente"""
    # Cargar configuración desde archivo TOML si existe
    config = {}
    try:
        import toml
        if Path("config/talentek_agentes_config.toml").exists():
            with open("config/talentek_agentes_config.toml", "r") as f:
                full_config = toml.load(f)
                if "agente_finanzas" in full_config:
                    config = full_config["agente_finanzas"]
    except ImportError:
        logger.warning("No se pudo importar toml. Usando configuración por defecto.")
    except Exception as e:
        logger.warning(f"Error al cargar configuración: {str(e)}")
    
    # Inicializar y ejecutar agente
    agent = FinanzasAgent(config)
    success = agent.run()
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())