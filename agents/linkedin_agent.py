"""
Agente LinkedIn para TalentekIA
Este agente se encarga de buscar oportunidades de trabajo y candidatos en LinkedIn
"""
import os
import json
import logging
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

from agents.base_agent import BaseAgent
from scripts.env_loader import env

class LinkedInAgent(BaseAgent):
    """Agente para buscar oportunidades y candidatos en LinkedIn"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Inicializa el agente de LinkedIn"""
        super().__init__("linkedin", config)
        
        # Configuración específica para LinkedIn
        self.username = env.get("LINKEDIN_USERNAME")
        self.cookies = self._parse_cookies(env.get("LINKEDIN_COOKIES", "{}"))
        
        # Parámetros de búsqueda
        self.search_params = self.config.get("search_params", {
            "keywords": ["Python", "Data Science", "AI", "Machine Learning"],
            "locations": ["España", "Remoto"],
            "job_types": ["Tiempo completo", "Contrato"],
            "experience_levels": ["Medio", "Senior"]
        })
    
    def _parse_cookies(self, cookies_str: str) -> Dict[str, str]:
        """Convierte la cadena de cookies en un diccionario"""
        try:
            if isinstance(cookies_str, str):
                return json.loads(cookies_str)
            return cookies_str
        except json.JSONDecodeError:
            self.logger.error("Error al parsear cookies de LinkedIn")
            return {}
    
    def _check_auth(self) -> bool:
        """Verifica si la autenticación con LinkedIn es válida"""
        if not self.username or not self.cookies:
            self.logger.error("Faltan credenciales de LinkedIn")
            return False
        
        # En una implementación real, aquí verificaríamos la validez de las cookies
        # Por ahora, simplemente verificamos que existan las cookies necesarias
        required_cookies = ["li_at", "JSESSIONID"]
        for cookie in required_cookies:
            if cookie not in self.cookies:
                self.logger.error(f"Falta la cookie {cookie} para LinkedIn")
                return False
        
        return True
    
    def run(self) -> bool:
        """
        Ejecuta la búsqueda en LinkedIn
        
        Returns:
            bool: True si la búsqueda fue exitosa, False en caso contrario
        """
        if not self._check_auth():
            return False
        
        self.logger.info("Iniciando búsqueda en LinkedIn")
        
        try:
            # En una implementación real, aquí haríamos la búsqueda en LinkedIn
            # Por ahora, generamos datos de ejemplo
            self.results = self._generate_sample_data()
            return True
        
        except Exception as e:
            self.logger.error(f"Error durante la búsqueda en LinkedIn: {str(e)}")
            return False
    
    def _generate_sample_data(self) -> List[Dict[str, Any]]:
        """Genera datos de ejemplo para demostración"""
        return [
            {
                "id": "1",
                "title": "Data Scientist",
                "company": "TechCorp",
                "location": "Madrid, España",
                "description": "Buscamos un Data Scientist con experiencia en Python y Machine Learning",
                "salary": "45.000€ - 60.000€",
                "date_posted": "2025-05-01",
                "url": "https://linkedin.com/jobs/view/1"
            },
            {
                "id": "2",
                "title": "ML Engineer",
                "company": "AI Solutions",
                "location": "Remoto",
                "description": "Desarrollador de modelos de ML para aplicaciones de procesamiento de lenguaje natural",
                "salary": "50.000€ - 70.000€",
                "date_posted": "2025-05-02",
                "url": "https://linkedin.com/jobs/view/2"
            },
            {
                "id": "3",
                "title": "Python Developer",
                "company": "Software Innovations",
                "location": "Barcelona, España",
                "description": "Desarrollo de aplicaciones web con Django y Flask",
                "salary": "40.000€ - 55.000€",
                "date_posted": "2025-05-03",
                "url": "https://linkedin.com/jobs/view/3"
            },
            {
                "id": "4",
                "title": "AI Research Scientist",
                "company": "Research Labs",
                "location": "Remoto",
                "description": "Investigación en algoritmos de aprendizaje profundo",
                "salary": "60.000€ - 80.000€",
                "date_posted": "2025-05-01",
                "url": "https://linkedin.com/jobs/view/4"
            },
            {
                "id": "5",
                "title": "Data Engineer",
                "company": "Big Data Solutions",
                "location": "Valencia, España",
                "description": "Diseño e implementación de pipelines de datos",
                "salary": "45.000€ - 65.000€",
                "date_posted": "2025-05-02",
                "url": "https://linkedin.com/jobs/view/5"
            }
        ]
    
    def process_data(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Procesa los datos obtenidos de LinkedIn
        
        Args:
            data: Lista de ofertas de trabajo
            
        Returns:
            pd.DataFrame: DataFrame con las ofertas procesadas
        """
        self.logger.info(f"Procesando {len(data)} ofertas de trabajo")
        
        # Convertir a DataFrame
        df = pd.DataFrame(data)
        
        # Añadir columnas derivadas
        df["days_ago"] = (datetime.now() - pd.to_datetime(df["date_posted"])).dt.days
        df["remote"] = df["location"].str.contains("Remoto", case=False)
        
        # Ordenar por fecha de publicación (más recientes primero)
        df = df.sort_values("date_posted", ascending=False)
        
        return df
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Genera un informe en formato Markdown con las ofertas encontradas
        
        Args:
            df: DataFrame con las ofertas procesadas
            
        Returns:
            str: Informe en formato Markdown
        """
        self.logger.info("Generando informe de ofertas de trabajo")
        
        # Crear el informe
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# Informe de Ofertas de Trabajo en LinkedIn
        
## Resumen
**Fecha de generación:** {now}
**Total de ofertas encontradas:** {len(df)}
**Ofertas remotas:** {df["remote"].sum()}
**Rango salarial promedio:** {self._calculate_avg_salary_range(df)}

## Ofertas Destacadas

"""
        
        # Añadir cada oferta al informe
        for _, row in df.iterrows():
            report += f"""### {row['title']} - {row['company']}
**Ubicación:** {row['location']}
**Salario:** {row['salary']}
**Fecha:** {row['date_posted']} ({row['days_ago']} días)

{row['description']}

[Ver oferta en LinkedIn]({row['url']})

---

"""
        
        return report
    
    def _calculate_avg_salary_range(self, df: pd.DataFrame) -> str:
        """Calcula el rango salarial promedio de las ofertas"""
        try:
            # Extraer los valores mínimos y máximos de los rangos salariales
            min_values = []
            max_values = []
            
            for salary in df["salary"]:
                if isinstance(salary, str) and "€" in salary:
                    parts = salary.split("-")
                    if len(parts) == 2:
                        min_str = parts[0].strip().replace("€", "").replace(".", "")
                        max_str = parts[1].strip().replace("€", "").replace(".", "")
                        
                        try:
                            min_values.append(float(min_str))
                            max_values.append(float(max_str))
                        except ValueError:
                            pass
            
            if min_values and max_values:
                avg_min = sum(min_values) / len(min_values)
                avg_max = sum(max_values) / len(max_values)
                return f"{avg_min:.2f}€ - {avg_max:.2f}€"
            
            return "No disponible"
        
        except Exception as e:
            self.logger.error(f"Error al calcular rango salarial: {str(e)}")
            return "Error en cálculo"


# Función para crear una instancia del agente
def create_agent(config=None):
    """Crea una instancia del agente de LinkedIn"""
    return LinkedInAgent(config)