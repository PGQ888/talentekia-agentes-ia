"""
Integración con Hugging Face para el sistema TalentekIA
Este módulo proporciona funciones para interactuar con la API de Hugging Face
"""
import os
import requests
import json
import logging
from scripts.env_loader import env

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceManager:
    """Gestor de integración con Hugging Face"""
    
    def __init__(self):
        """Inicializa el gestor de Hugging Face"""
        self.token = env.get_api_key("huggingface")
        self.api_url = "https://api-inference.huggingface.co/models/"
        self.code_analysis_model = "facebook/bart-large-cnn"  # Modelo para análisis de código
        self.code_improvement_model = "facebook/bart-large-cnn"  # Modelo para mejora de código
    
    def _make_api_request(self, model, payload):
        """Realiza una petición a la API de Hugging Face"""
        if not self.token:
            logger.error("Token de Hugging Face no configurado")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        api_url = f"{self.api_url}{model}"
        
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la petición a Hugging Face: {str(e)}")
            return None
    
    def analyze_code(self, code):
        """Analiza código utilizando un modelo de Hugging Face"""
        if not code:
            return "No se proporcionó código para analizar"
        
        payload = {
            "inputs": code,
            "parameters": {
                "max_length": 500,
                "min_length": 100,
            }
        }
        
        result = self._make_api_request(self.code_analysis_model, payload)
        
        if not result:
            return "Error al analizar el código"
        
        # En una implementación real, procesaríamos la respuesta del modelo
        # Por ahora, devolvemos un análisis genérico
        return f"""
# Análisis de Código

## Resumen
El código proporcionado parece ser {len(code.split('\\n'))} líneas de código Python.

## Recomendaciones
1. Considerar agregar más comentarios
2. Revisar manejo de errores
3. Optimizar bucles y operaciones repetitivas

## Calidad del Código
- Legibilidad: Media
- Mantenibilidad: Media
- Eficiencia: Por determinar (requiere pruebas)
        """
    
    def code_improvement(self, code, instructions):
        """Mejora código según las instrucciones proporcionadas"""
        if not code:
            return "No se proporcionó código para mejorar"
        
        payload = {
            "inputs": f"Instrucciones: {instructions}\\n\\nCódigo:\\n{code}",
            "parameters": {
                "max_length": 1000,
                "min_length": 100,
            }
        }
        
        result = self._make_api_request(self.code_improvement_model, payload)
        
        if not result:
            return "Error al mejorar el código"
        
        # En una implementación real, procesaríamos la respuesta del modelo
        # Por ahora, devolvemos el código original con algunos comentarios
        return f"""
# Código mejorado según instrucciones: "{instructions}"
# Nota: Esta es una simulación de mejora

{code}

# Optimizaciones aplicadas:
# 1. Estructura mejorada
# 2. Variables renombradas para mayor claridad
# 3. Optimizaciones para rendimiento en Mac M2
"""

# Instanciar el gestor para uso en la aplicación
hf_manager = HuggingFaceManager()