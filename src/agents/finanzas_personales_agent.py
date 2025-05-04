#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Agente de Finanzas Personales para TalentekIA

Este agente analiza datos financieros personales y proporciona recomendaciones.
"""

import logging
import pandas as pd
import numpy as np
from typing import Any, Dict, Optional, List, Tuple
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from src.agents.base_agent import BaseAgent

logger = logging.getLogger("TalentekIA-FinanzasPersonales")

class FinanzasPersonales(BaseAgent):
    """Agente para análisis y recomendaciones de finanzas personales."""

    def __init__(self, agent_id: str = "finanzas_personales", config: Optional[Dict[str, Any]] = None):
        """Inicializa el agente de finanzas personales.
        
        Args:
            agent_id: Identificador único del agente
            config: Configuración específica del agente
        """
        super().__init__(agent_id, config)
        logger.info(f"Agente de Finanzas Personales inicializado con ID: {agent_id}")
        
        # Configuración específica del agente
        self.categories = self.config.get("categories", ["ingresos", "gastos", "inversiones", "deudas"])
        self.goals = self.config.get("financial_goals", {})
        self.output_dir = Path(self.config.get("output_dir", "./output/finanzas_personales"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def process_data(self, data: Any) -> pd.DataFrame:
        """Procesa los datos financieros personales.
        
        Args:
            data: Datos financieros a procesar
            
        Returns:
            DataFrame con los resultados del análisis
        """
        logger.info("Procesando datos financieros personales")
        
        try:
            # Implementación básica para demostración
            if isinstance(data, pd.DataFrame):
                df = data.copy()
            else:
                # Crear DataFrame de ejemplo si no se proporcionan datos
                logger.warning("No se proporcionaron datos válidos, usando datos de ejemplo")
                df = pd.DataFrame({
                    "fecha": pd.date_range(start="2025-01-01", periods=12, freq="M"),
                    "ingresos": [5000, 5200, 5000, 5500, 5300, 5800, 5600, 5700, 5900, 6000, 6100, 6200],
                    "gastos_fijos": [2000, 2000, 2100, 2100, 2100, 2200, 2200, 2300, 2300, 2300, 2400, 2400],
                    "gastos_variables": [1500, 1800, 1400, 1900, 1600, 1700, 1500, 1600, 1700, 1800, 1700, 1800],
                    "inversiones": [500, 500, 500, 600, 600, 700, 700, 800, 800, 900, 900, 1000],
                    "deudas": [10000, 9800, 9600, 9400, 9200, 9000, 8800, 8600, 8400, 8200, 8000, 7800]
                })
                
            # Calcular métricas financieras básicas
            df["gastos_totales"] = df["gastos_fijos"] + df["gastos_variables"]
            df["ahorro"] = df["ingresos"] - df["gastos_totales"]
            df["ratio_ahorro"] = (df["ahorro"] / df["ingresos"]) * 100
            df["ratio_deuda_ingreso"] = (df["deudas"] / df["ingresos"])
            df["patrimonio_neto"] = df["inversiones"].cumsum() + df["ahorro"].cumsum() - df["deudas"]
            
            # Calcular tendencias (cambio porcentual mes a mes)
            for col in ["ingresos", "gastos_totales", "ahorro", "deudas"]:
                df[f"tendencia_{col}"] = df[col].pct_change() * 100
                
            return df
            
        except Exception as e:
            logger.error(f"Error al procesar datos financieros: {e}")
            return pd.DataFrame()  # Devolver DataFrame vacío en caso de error
    
    def generate_charts(self, df: pd.DataFrame) -> List[str]:
        """Genera gráficos visuales para el análisis financiero.
        
        Args:
            df: DataFrame con los datos analizados
            
        Returns:
            Lista de rutas a los gráficos generados
        """
        logger.info("Generando visualizaciones financieras")
        
        if df.empty:
            logger.warning("No hay datos suficientes para generar visualizaciones")
            return []
        
        chart_paths = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # 1. Gráfico de ingresos vs gastos
            plt.figure(figsize=(12, 6))
            plt.plot(df["fecha"], df["ingresos"], marker="o", label="Ingresos")
            plt.plot(df["fecha"], df["gastos_totales"], marker="x", label="Gastos Totales")
            plt.plot(df["fecha"], df["ahorro"], marker="^", label="Ahorro")
            plt.title("Evolución de Ingresos, Gastos y Ahorro")
            plt.xlabel("Fecha")
            plt.ylabel("Cantidad ($)")
            plt.grid(True, linestyle="--", alpha=0.7)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            income_chart_path = self.output_dir / f"ingresos_gastos_{timestamp}.png"
            plt.savefig(income_chart_path)
            chart_paths.append(str(income_chart_path))
            plt.close()
            
            # 2. Gráfico de composición de gastos
            plt.figure(figsize=(12, 6))
            plt.stackplot(df["fecha"], df["gastos_fijos"], df["gastos_variables"], 
                         labels=["Gastos Fijos", "Gastos Variables"],
                         alpha=0.7)
            plt.title("Composición de Gastos Mensuales")
            plt.xlabel("Fecha")
            plt.ylabel("Cantidad ($)")
            plt.legend(loc="upper left")
            plt.grid(True, linestyle="--", alpha=0.7)
            plt.tight_layout()
            
            expenses_chart_path = self.output_dir / f"composicion_gastos_{timestamp}.png"
            plt.savefig(expenses_chart_path)
            chart_paths.append(str(expenses_chart_path))
            plt.close()
            
            # 3. Gráfico de patrimonio neto y deudas
            plt.figure(figsize=(12, 6))
            plt.plot(df["fecha"], df["patrimonio_neto"], marker="o", label="Patrimonio Neto")
            plt.plot(df["fecha"], df["deudas"], marker="x", label="Deudas")
            plt.title("Evolución del Patrimonio Neto y Deudas")
            plt.xlabel("Fecha")
            plt.ylabel("Cantidad ($)")
            plt.grid(True, linestyle="--", alpha=0.7)
            plt.legend()
            plt.tight_layout()
            
            wealth_chart_path = self.output_dir / f"patrimonio_deudas_{timestamp}.png"
            plt.savefig(wealth_chart_path)
            chart_paths.append(str(wealth_chart_path))
            plt.close()
            
            logger.info(f"Se generaron {len(chart_paths)} visualizaciones")
            return chart_paths
            
        except Exception as e:
            logger.error(f"Error al generar visualizaciones: {e}")
            return chart_paths
    
    def forecast_finances(self, df: pd.DataFrame, months_ahead: int = 6) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Realiza proyecciones financieras basadas en datos históricos.
        
        Args:
            df: DataFrame con datos históricos
            months_ahead: Número de meses para proyectar
            
        Returns:
            DataFrame con proyecciones y diccionario con métricas de proyección
        """
        logger.info(f"Realizando proyecciones financieras para {months_ahead} meses")
        
        if df.empty or len(df) < 3:  # Necesitamos al menos 3 puntos para una proyección razonable
            logger.warning("Datos insuficientes para realizar proyecciones")
            return pd.DataFrame(), {}
        
        try:
            # Columnas para proyectar
            forecast_cols = ["ingresos", "gastos_fijos", "gastos_variables", "inversiones", "deudas"]
            
            # Crear DataFrame para proyecciones
            last_date = df["fecha"].iloc[-1]
            forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=31), 
                                         periods=months_ahead, freq="M")
            
            forecast_df = pd.DataFrame({"fecha": forecast_dates})
            
            # Calcular tendencias y proyectar cada columna
            for col in forecast_cols:
                # Calcular tendencia promedio (cambio porcentual mensual)
                pct_changes = df[col].pct_change().dropna().mean()
                
                # Valor inicial para proyección (último valor conocido)
                last_value = df[col].iloc[-1]
                projected_values = [last_value]
                
                # Proyectar valores futuros
                for _ in range(months_ahead):
                    next_value = projected_values[-1] * (1 + pct_changes)
                    projected_values.append(next_value)
                
                # Añadir al DataFrame de proyección (ignorar el primer valor que era el inicial)
                forecast_df[col] = projected_values[1:]
            
            # Calcular métricas derivadas en las proyecciones
            forecast_df["gastos_totales"] = forecast_df["gastos_fijos"] + forecast_df["gastos_variables"]
            forecast_df["ahorro"] = forecast_df["ingresos"] - forecast_df["gastos_totales"]
            forecast_df["ratio_ahorro"] = (forecast_df["ahorro"] / forecast_df["ingresos"]) * 100
            
            # Métricas de proyección
            forecast_metrics = {
                "ahorro_total_proyectado": forecast_df["ahorro"].sum(),
                "ingreso_total_proyectado": forecast_df["ingresos"].sum(),
                "deuda_final_proyectada": forecast_df["deudas"].iloc[-1],
                "cambio_patrimonio_proyectado": (
                    forecast_df["ahorro"].sum() - 
                    (df["deudas"].iloc[-1] - forecast_df["deudas"].iloc[-1])
                )
            }
            
            return forecast_df, forecast_metrics
            
        except Exception as e:
            logger.error(f"Error al realizar proyecciones financieras: {e}")
            return pd.DataFrame(), {}
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """Genera un informe basado en los datos financieros analizados.
        
        Args:
            df: DataFrame con los datos analizados
            
        Returns:
            Informe en formato texto
        """
        logger.info("Generando informe de finanzas personales")
        
        if df.empty:
            return "No hay datos suficientes para generar un informe."
        
        # Generar informe básico
        report = []
        report.append("# Informe de Finanzas Personales\n")
        report.append(f"Fecha del informe: {datetime.now().strftime('%Y-%m-%d')}\n")
        
        # Resumen financiero
        report.append("## Resumen Financiero\n")
        
        if "ingresos" in df.columns and "gastos_totales" in df.columns:
            ultimo_mes = df.iloc[-1]
            ingresos_ultimo_mes = ultimo_mes["ingresos"]
            gastos_ultimo_mes = ultimo_mes["gastos_totales"]
            ahorro_ultimo_mes = ultimo_mes["ahorro"] if "ahorro" in df.columns else (ingresos_ultimo_mes - gastos_ultimo_mes)
            
            report.append(f"- **Ingresos (último mes)**: ${ingresos_ultimo_mes:.2f}")
            report.append(f"- **Gastos totales**: ${gastos_ultimo_mes:.2f}")
            report.append(f"- **Ahorro**: ${ahorro_ultimo_mes:.2f}")
            
            if "ratio_ahorro" in df.columns:
                ratio_ahorro = ultimo_mes["ratio_ahorro"]
                report.append(f"- **Ratio de ahorro**: {ratio_ahorro:.2f}%")
            
        # Análisis de tendencias
        report.append("\n## Tendencias\n")
        
        if len(df) >= 2 and "ingresos" in df.columns:
            ingresos_anterior = df.iloc[-2]["ingresos"]
            ingresos_actual = df.iloc[-1]["ingresos"]
            cambio_ingresos = ((ingresos_actual - ingresos_anterior) / ingresos_anterior) * 100
            
            report.append(f"- **Cambio en ingresos**: {cambio_ingresos:.2f}%")
            
        if "deudas" in df.columns and len(df) >= 2:
            deuda_anterior = df.iloc[-2]["deudas"]
            deuda_actual = df.iloc[-1]["deudas"]
            cambio_deuda = ((deuda_actual - deuda_anterior) / deuda_anterior) * 100
            
            report.append(f"- **Cambio en deudas**: {cambio_deuda:.2f}%")
            
        # Análisis del patrimonio
        if "patrimonio_neto" in df.columns:
            patrimonio_actual = df.iloc[-1]["patrimonio_neto"]
            report.append(f"- **Patrimonio neto actual**: ${patrimonio_actual:.2f}")
            
            if len(df) >= 3:
                patrimonio_tendencia = df["patrimonio_neto"].diff().mean()
                report.append(f"- **Tendencia mensual del patrimonio**: ${patrimonio_tendencia:.2f}")
                
        # Proyecciones financieras
        forecast_df, forecast_metrics = self.forecast_finances(df)
        
        if not forecast_df.empty:
            report.append("\n## Proyecciones Financieras (6 meses)\n")
            report.append(f"- **Ahorro total proyectado**: ${forecast_metrics['ahorro_total_proyectado']:.2f}")
            report.append(f"- **Deuda proyectada al final del período**: ${forecast_metrics['deuda_final_proyectada']:.2f}")
            report.append(f"- **Cambio en patrimonio proyectado**: ${forecast_metrics['cambio_patrimonio_proyectado']:.2f}")
        
        # Recomendaciones
        report.append("\n## Recomendaciones\n")
        
        if "ratio_ahorro" in df.columns:
            ratio_ahorro = df.iloc[-1]["ratio_ahorro"]
            if ratio_ahorro < 10:
                report.append("- **Aumentar ahorro**: Tu ratio de ahorro está por debajo del 10% recomendado.")
                report.append("  - Considera revisar gastos variables para identificar áreas de reducción.")
            else:
                report.append(f"- **Buen trabajo en ahorro**: Tu ratio de ahorro del {ratio_ahorro:.2f}% está por encima del mínimo recomendado.")
        
        if "ratio_deuda_ingreso" in df.columns:
            ratio_deuda = df.iloc[-1]["ratio_deuda_ingreso"]
            if ratio_deuda > 0.36:
                report.append("- **Atención a nivel de deuda**: Tu ratio de deuda/ingreso está por encima del nivel recomendado.")
                report.append("  - Prioriza la reducción de deudas de alto interés.")
            else:
                report.append("- **Nivel de deuda saludable**: Mantén tu estrategia actual de gestión de deudas.")
        
        # Recomendaciones de inversión
        if "inversiones" in df.columns:
            inversion_ratio = df.iloc[-1]["inversiones"] / df.iloc[-1]["ingresos"] * 100
            if inversion_ratio < 10:
                report.append("- **Aumentar inversiones**: Estás invirtiendo menos del 10% de tus ingresos.")
                report.append("  - Considera establecer inversiones automáticas mensuales.")
            else:
                report.append(f"- **Buen nivel de inversión**: Estás invirtiendo el {inversion_ratio:.2f}% de tus ingresos.")
        
        return "\n".join(report)
    
    def save_results(self, df: pd.DataFrame, report: str) -> Dict[str, str]:
        """Guarda los resultados del análisis financiero.
        
        Args:
            df: DataFrame con los datos analizados
            report: Informe generado
            
        Returns:
            Diccionario con las rutas de los archivos guardados
        """
        logger.info("Guardando resultados del análisis financiero")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_files = {}
        
        try:
            # Guardar DataFrame procesado
            if not df.empty:
                df_path = self.output_dir / f"datos_financieros_{timestamp}.csv"
                df.to_csv(df_path, index=False)
                output_files["data"] = str(df_path)
            
            # Guardar informe
            if report:
                report_path = self.output_dir / f"informe_financiero_{timestamp}.md"
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(report)
                output_files["report"] = str(report_path)
            
            # Generar y guardar visualizaciones
            chart_paths = self.generate_charts(df)
            if chart_paths:
                output_files["charts"] = chart_paths
            
            logger.info(f"Resultados guardados exitosamente: {output_files}")
            return output_files
            
        except Exception as e:
            logger.error(f"Error al guardar resultados: {e}")
            return output_files
    
    def run(self) -> bool:
        """Ejecuta el agente de finanzas personales.
        
        Returns:
            True si la ejecución fue exitosa, False en caso contrario
        """
        logger.info("Ejecutando agente de finanzas personales")
        
        try:
            # Aquí iría la lógica para obtener datos reales
            # Por ahora usamos datos de ejemplo
            data = None  # Usará datos de ejemplo en process_data
            
            # Procesar datos
            results_df = self.process_data(data)
            
            # Generar informe
            report = self.generate_report(results_df)
            
            # Guardar resultados
            output_files = self.save_results(results_df, report)
            
            logger.info("Ejecución del agente de finanzas personales completada con éxito")
            logger.info(f"Archivos generados: {output_files}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error en la ejecución del agente de finanzas personales: {e}")
            return False