"""
Agente de resumen semanal
Este agente consolida la información de todos los demás agentes y genera un informe integrado
"""
import os
import logging
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Importar la clase base
from src.agents.base_agent import BaseAgent
from src.utils.env_loader import env

class ResumenSemanalAgent(BaseAgent):
    """Agente para generación de resúmenes semanales integrales"""
    
    def __init__(self, agent_id: str = "resumen_semanal", config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el agente de resumen semanal
        
        Args:
            agent_id: Identificador del agente
            config: Configuración específica (opcional)
        """
        super().__init__(agent_id, config)
        self.logger = logging.getLogger("TalentekIA-ResumenSemanal")
        
        # Estado del agente
        self.status = "ready"
        self.last_execution = None
        self.data_path = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                           "..", "data", "resumen"))
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Periodo del resumen (por defecto, la semana actual)
        self.fecha_inicio = datetime.now() - timedelta(days=datetime.now().weekday())
        self.fecha_fin = self.fecha_inicio + timedelta(days=6)
        
        # Agentes a incluir en el resumen
        self.agentes_objetivo = ["linkedin", "estrategia_comercial", 
                                "finanzas_personales", "automejora", 
                                "email_automation"]
    
    def run(self) -> bool:
        """
        Ejecuta el flujo principal del agente de resumen
        
        Returns:
            bool: True si la ejecución fue exitosa
        """
        self.logger.info("Iniciando agente de Resumen Semanal")
        self.status = "running"
        
        try:
            # Recolectar información de los demás agentes
            self.logger.info("Recopilando información de todos los agentes")
            
            # Crear resumen de periodo
            periodo_str = f"{self.fecha_inicio.strftime('%d/%m/%Y')} - {self.fecha_fin.strftime('%d/%m/%Y')}"
            
            # Recolectar resúmenes (simulado para este ejemplo)
            # En una implementación real, aquí se cargarían los datos generados 
            # por cada agente durante la semana
            resumen_linkedin = self._obtener_resumen_linkedin()
            resumen_estrategia = self._obtener_resumen_estrategia()
            resumen_finanzas = self._obtener_resumen_finanzas()
            resumen_automejora = self._obtener_resumen_automejora()
            resumen_email = self._obtener_resumen_email()
            
            # Consolidar todos los resúmenes
            self.results = {
                "periodo": periodo_str,
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "resumen_ejecutivo": {
                    "destacados": [
                        "Aumento del 15% en conexiones de LinkedIn",
                        "Nueva estrategia comercial para el sector tecnológico",
                        "Reducción del 8% en gastos mensuales",
                        "Progreso del 25% en objetivo de certificación profesional",
                        "Reducción del 30% en tiempo dedicado a email"
                    ],
                    "alertas": [
                        "Tendencia negativa en el sector retail",
                        "Aumento en gastos de categoría 'Otros'",
                        "Email importante pendiente de respuesta"
                    ]
                },
                "agentes": {
                    "linkedin": resumen_linkedin,
                    "estrategia_comercial": resumen_estrategia,
                    "finanzas_personales": resumen_finanzas,
                    "automejora": resumen_automejora,
                    "email_automation": resumen_email
                },
                "acciones_recomendadas": [
                    {"agente": "linkedin", "accion": "Aumentar publicaciones semanales", "prioridad": "Media"},
                    {"agente": "estrategia_comercial", "accion": "Explorar alianzas en sector tecnología", "prioridad": "Alta"},
                    {"agente": "finanzas_personales", "accion": "Revisar categoría de gastos 'Otros'", "prioridad": "Alta"},
                    {"agente": "automejora", "accion": "Dedicar 30 min adicionales al estudio de IA", "prioridad": "Media"},
                    {"agente": "email_automation", "accion": "Configurar reglas de archivado automático", "prioridad": "Baja"}
                ],
                "estadisticas": {
                    "total_agentes_activos": len(self.agentes_objetivo),
                    "total_informes_generados": 5,
                    "tiempo_ahorrado_estimado": "8.5 horas"
                }
            }
            
            self.last_execution = datetime.now()
            self.status = "completed"
            return True
            
        except Exception as e:
            self.logger.error(f"Error en la ejecución del agente de resumen semanal: {str(e)}", exc_info=True)
            self.status = "error"
            return False
    
    def _obtener_resumen_linkedin(self) -> Dict[str, Any]:
        """Obtiene el resumen del agente de LinkedIn (simulado)"""
        return {
            "conexiones_nuevas": 28,
            "total_conexiones": 732,
            "mensajes_recibidos": 15,
            "interacciones": 47,
            "publicaciones": 3,
            "destacado": "Mensaje del reclutador de TechCorp"
        }
    
    def _obtener_resumen_estrategia(self) -> Dict[str, Any]:
        """Obtiene el resumen del agente de estrategia comercial (simulado)"""
        return {
            "sectores_analizados": 3,
            "oportunidades_detectadas": 2,
            "principales_tendencias": ["Aumento en demanda de IA", "Caída en retail tradicional"],
            "recomendacion_principal": "Desarrollar oferta para sector tecnológico"
        }
    
    def _obtener_resumen_finanzas(self) -> Dict[str, Any]:
        """Obtiene el resumen del agente de finanzas (simulado)"""
        return {
            "ingresos": 8500,
            "gastos": 5200,
            "ahorro": 3300,
            "tasa_ahorro": 38.8,
            "principal_gasto": "Vivienda",
            "cambio_patrimonio": "+3.5%"
        }
    
    def _obtener_resumen_automejora(self) -> Dict[str, Any]:
        """Obtiene el resumen del agente de automejora (simulado)"""
        return {
            "objetivos_en_curso": 3,
            "habitos_completados": 15,
            "area_mayor_progreso": "Habilidades técnicas",
            "area_menor_progreso": "Gestión del tiempo",
            "recomendacion_principal": "Implementar técnica Pomodoro"
        }
    
    def _obtener_resumen_email(self) -> Dict[str, Any]:
        """Obtiene el resumen del agente de email (simulado)"""
        return {
            "emails_procesados": 127,
            "tiempo_ahorrado": 45,
            "emails_priorizados": 15,
            "emails_archivados": 82,
            "emails_pendientes": 7,
            "categoria_principal": "Trabajo"
        }
    
    def process_data(self, data: Any) -> pd.DataFrame:
        """
        Procesa los datos para generar una tabla de resumen
        
        Args:
            data: Datos a procesar
            
        Returns:
            pd.DataFrame: DataFrame con los datos procesados
        """
        # Crear un DataFrame con las acciones recomendadas
        if "acciones_recomendadas" in data:
            df = pd.DataFrame(data["acciones_recomendadas"])
            # Ordenar por prioridad
            prioridad_map = {"Alta": 0, "Media": 1, "Baja": 2}
            df["prioridad_num"] = df["prioridad"].map(prioridad_map)
            df = df.sort_values(by="prioridad_num").drop("prioridad_num", axis=1)
            return df
        
        return pd.DataFrame(columns=["agente", "accion", "prioridad"])
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Genera un informe en formato Markdown
        
        Args:
            df: DataFrame con los datos procesados
            
        Returns:
            str: Informe en formato Markdown
        """
        # Generar informe básico
        report = f"""# Resumen Semanal - {self.results.get('periodo', 'N/A')}

## Resumen Ejecutivo

### Puntos Destacados
"""
        
        # Añadir puntos destacados
        for destacado in self.results["resumen_ejecutivo"].get("destacados", []):
            report += f"- {destacado}\n"
        
        # Añadir alertas
        report += "\n### Alertas a Considerar\n"
        for alerta in self.results["resumen_ejecutivo"].get("alertas", []):
            report += f"- ⚠️ {alerta}\n"
        
        # Añadir resumen de cada agente
        report += "\n## Resumen por Agentes\n"
        
        # LinkedIn
        linkedin_data = self.results["agentes"].get("linkedin", {})
        report += f"""
### 1. LinkedIn
- **Conexiones nuevas**: {linkedin_data.get('conexiones_nuevas', 0)}
- **Total de conexiones**: {linkedin_data.get('total_conexiones', 0)}
- **Mensajes recibidos**: {linkedin_data.get('mensajes_recibidos', 0)}
- **Interacciones**: {linkedin_data.get('interacciones', 0)}
- **Publicaciones realizadas**: {linkedin_data.get('publicaciones', 0)}
- **Destacado**: {linkedin_data.get('destacado', 'Ninguno')}
"""
        
        # Estrategia Comercial
        estrategia_data = self.results["agentes"].get("estrategia_comercial", {})
        report += f"""
### 2. Estrategia Comercial
- **Sectores analizados**: {estrategia_data.get('sectores_analizados', 0)}
- **Oportunidades detectadas**: {estrategia_data.get('oportunidades_detectadas', 0)}
- **Principales tendencias**: {', '.join(estrategia_data.get('principales_tendencias', ['Ninguna']))}
- **Recomendación principal**: {estrategia_data.get('recomendacion_principal', 'Ninguna')}
"""
        
        # Finanzas Personales
        finanzas_data = self.results["agentes"].get("finanzas_personales", {})
        report += f"""
### 3. Finanzas Personales
- **Ingresos**: ${finanzas_data.get('ingresos', 0):,}
- **Gastos**: ${finanzas_data.get('gastos', 0):,}
- **Ahorro**: ${finanzas_data.get('ahorro', 0):,}
- **Tasa de ahorro**: {finanzas_data.get('tasa_ahorro', 0)}%
- **Principal categoría de gasto**: {finanzas_data.get('principal_gasto', 'N/A')}
- **Cambio en patrimonio**: {finanzas_data.get('cambio_patrimonio', 'N/A')}
"""
        
        # Automejora
        automejora_data = self.results["agentes"].get("automejora", {})
        report += f"""
### 4. Automejora Personal
- **Objetivos en curso**: {automejora_data.get('objetivos_en_curso', 0)}
- **Hábitos completados**: {automejora_data.get('habitos_completados', 0)}
- **Área de mayor progreso**: {automejora_data.get('area_mayor_progreso', 'N/A')}
- **Área de menor progreso**: {automejora_data.get('area_menor_progreso', 'N/A')}
- **Recomendación principal**: {automejora_data.get('recomendacion_principal', 'N/A')}
"""
        
        # Email
        email_data = self.results["agentes"].get("email_automation", {})
        report += f"""
### 5. Automatización de Email
- **Emails procesados**: {email_data.get('emails_procesados', 0)}
- **Tiempo ahorrado**: {email_data.get('tiempo_ahorrado', 0)} minutos
- **Emails priorizados**: {email_data.get('emails_priorizados', 0)}
- **Emails archivados automáticamente**: {email_data.get('emails_archivados', 0)}
- **Emails pendientes**: {email_data.get('emails_pendientes', 0)}
- **Categoría principal**: {email_data.get('categoria_principal', 'N/A')}
"""
        
        # Añadir acciones recomendadas
        report += "\n## Acciones Recomendadas\n\n"
        report += "| Agente | Acción | Prioridad |\n"
        report += "|--------|--------|----------|\n"
        
        for _, row in df.iterrows():
            report += f"| {row['agente']} | {row['accion']} | {row['prioridad']} |\n"
        
        # Añadir estadísticas
        stats = self.results.get("estadisticas", {})
        report += f"""
## Estadísticas del Sistema
- **Total de agentes activos**: {stats.get('total_agentes_activos', 0)}
- **Informes generados**: {stats.get('total_informes_generados', 0)}
- **Tiempo ahorrado estimado**: {stats.get('tiempo_ahorrado_estimado', 'N/A')}
"""
        
        # Añadir fecha del informe
        report += f"\n\n*Informe generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
        
        return report
    
    def save_results(self, df: pd.DataFrame, report: str) -> None:
        """
        Guarda los resultados en archivos
        
        Args:
            df: DataFrame con los datos procesados
            report: Informe en formato Markdown
        """
        # Crear carpeta para la fecha actual si no existe
        fecha_str = datetime.now().strftime("%Y%m%d")
        output_dir = self.data_path / fecha_str
        output_dir.mkdir(exist_ok=True)
        
        # Guardar DataFrame como CSV
        df_path = output_dir / f"acciones_recomendadas_{fecha_str}.csv"
        df.to_csv(df_path, index=False)
        
        # Guardar informe como Markdown
        report_path = output_dir / f"resumen_semanal_{fecha_str}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        # Guardar datos completos como JSON
        json_path = output_dir / f"datos_resumen_{fecha_str}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Resultados guardados en {output_dir}")