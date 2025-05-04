"""
Integración con GitHub para el sistema TalentekIA
Este módulo proporciona funciones para interactuar con la API de GitHub
"""
import os
import requests
import json
import logging
import base64
from scripts.env_loader import env

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubManager:
    """Gestor de integración con GitHub"""
    
    def __init__(self):
        """Inicializa el gestor de GitHub"""
        self.token = env.get_api_key("github")
        self.api_url = "https://api.github.com"
        self.repo = env.get("GITHUB_REPO", "")
    
    def _make_api_request(self, endpoint, method="GET", data=None):
        """Realiza una petición a la API de GitHub"""
        if not self.token:
            logger.error("Token de GitHub no configurado")
            return None
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.api_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data)
            else:
                logger.error(f"Método HTTP no soportado: {method}")
                return None
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la petición a GitHub: {str(e)}")
            return None
    
    def get_repo_contents(self, path=""):
        """Obtiene el contenido de un repositorio"""
        if not self.repo:
            logger.error("Repositorio de GitHub no configurado")
            return None
        
        endpoint = f"/repos/{self.repo}/contents/{path}"
        return self._make_api_request(endpoint)
    
    def get_file_content(self, path):
        """Obtiene el contenido de un archivo del repositorio"""
        if not self.repo:
            logger.error("Repositorio de GitHub no configurado")
            return None
        
        endpoint = f"/repos/{self.repo}/contents/{path}"
        result = self._make_api_request(endpoint)
        
        if not result or "content" not in result:
            return None
        
        content = base64.b64decode(result["content"]).decode("utf-8")
        return content
    
    def update_file(self, path, content, message):
        """Actualiza un archivo en el repositorio"""
        if not self.repo:
            logger.error("Repositorio de GitHub no configurado")
            return False
        
        # Primero obtenemos el SHA del archivo actual
        endpoint = f"/repos/{self.repo}/contents/{path}"
        current_file = self._make_api_request(endpoint)
        
        if not current_file:
            logger.error(f"No se pudo obtener el archivo actual: {path}")
            return False
        
        # Preparamos los datos para la actualización
        data = {
            "message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
            "sha": current_file["sha"]
        }
        
        # Actualizamos el archivo
        result = self._make_api_request(endpoint, method="PUT", data=data)
        return result is not None

# Instanciar el gestor para uso en la aplicación
github_manager = GitHubManager()