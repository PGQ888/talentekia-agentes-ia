"""
Integración con AnythingLLM para el sistema TalentekIA
Este módulo proporciona funciones para interactuar con la API de AnythingLLM
"""
import os
import requests
import json
import logging
from scripts.env_loader import env

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnythingLLMManager:
    """Gestor de integración con AnythingLLM"""
    
    def __init__(self):
        """Inicializa el gestor de AnythingLLM"""
        self.api_key = env.get_api_key("anythingllm")
        self.server_url = env.get("ANYTHINGLLM_SERVER_URL", "http://localhost:3001")
    
    def _make_api_request(self, endpoint, method="GET", data=None, files=None):
        """Realiza una petición a la API de AnythingLLM"""
        if not self.api_key:
            logger.error("API Key de AnythingLLM no configurada")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        url = f"{self.server_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                if files:
                    # Si hay archivos, no incluimos el header Content-Type para que requests lo establezca correctamente
                    response = requests.post(url, headers=headers, data=data, files=files)
                else:
                    headers["Content-Type"] = "application/json"
                    response = requests.post(url, headers=headers, json=data)
            else:
                logger.error(f"Método HTTP no soportado: {method}")
                return None
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la petición a AnythingLLM: {str(e)}")
            return None
    
    def get_workspaces(self):
        """Obtiene la lista de workspaces disponibles"""
        endpoint = "/api/workspaces"
        return self._make_api_request(endpoint)
    
    def create_workspace(self, name, description=""):
        """Crea un nuevo workspace"""
        endpoint = "/api/workspaces"
        data = {
            "name": name,
            "description": description
        }
        return self._make_api_request(endpoint, method="POST", data=data)
    
    def upload_document(self, workspace_id, file_path):
        """Sube un documento a un workspace"""
        if not os.path.exists(file_path):
            logger.error(f"El archivo no existe: {file_path}")
            return False
        
        endpoint = f"/api/workspaces/{workspace_id}/documents"
        
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            result = self._make_api_request(endpoint, method="POST", files=files)
        
        return result is not None
    
    def process_documents_for_agent(self, agent_name, docs_dir):
        """Procesa documentos para un agente específico"""
        # Verificar si existe el workspace para el agente, si no, crearlo
        workspaces = self.get_workspaces()
        
        if not workspaces:
            logger.error("No se pudieron obtener los workspaces")
            return False
        
        workspace_id = None
        for workspace in workspaces.get("workspaces", []):
            if workspace["name"] == agent_name:
                workspace_id = workspace["id"]
                break
        
        if not workspace_id:
            # Crear el workspace
            result = self.create_workspace(agent_name, f"Workspace para el agente {agent_name}")
            if not result or "workspace" not in result:
                logger.error(f"No se pudo crear el workspace para {agent_name}")
                return False
            workspace_id = result["workspace"]["id"]
        
        # Subir documentos
        success = True
        for file_name in os.listdir(docs_dir):
            if file_name.endswith(".md") or file_name.endswith(".csv") or file_name.endswith(".txt"):
                file_path = os.path.join(docs_dir, file_name)
                if not self.upload_document(workspace_id, file_path):
                    logger.error(f"Error al subir el documento {file_name}")
                    success = False
        
        return success

# Instanciar el gestor para uso en la aplicación
anything_llm_manager = AnythingLLMManager()