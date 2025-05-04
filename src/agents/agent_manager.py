"""
Gestor de agentes para TalentekIA
Proporciona funciones para registrar, inicializar y ejecutar agentes
"""
import os
import importlib
import logging
import platform
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class AgentManager:
    """Gestor de agentes del sistema TalentekIA"""
    
    # Lista predefinida de agentes disponibles
    AVAILABLE_AGENTS = [
        "linkedin_agent",
        "estrategia_comercial_agent",
        "finanzas_personales_agent",
        "automejora_agent",
        "email_automation_agent"
    ]
    
    def __init__(self):
        """Inicializa el gestor de agentes"""
        self.logger = logging.getLogger("TalentekIA-AgentManager")
        self.agents = {}
        self.execution_history = {}
        
        # Verificar si estamos en Mac M2 y aplicar optimizaciones
        if platform.system() == "Darwin" and platform.machine() == "arm64":
            self.logger.info("Detectado Mac con Apple Silicon (M1/M2), aplicando optimizaciones...")
            self._apply_m2_optimizations()
        
        # Cargar agentes disponibles
        self._load_available_agents()
    
    def _apply_m2_optimizations(self):
        """Aplica optimizaciones específicas para Mac M1/M2"""
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
        
        # Intentar configurar PyTorch para usar MPS si está disponible
        try:
            import torch
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                self.logger.info("MPS disponible para PyTorch, configurando como dispositivo por defecto")
                os.environ["PYTORCH_DEVICE"] = "mps"
        except (ImportError, AttributeError):
            self.logger.warning("No se pudo configurar MPS para PyTorch")
    
    def _load_available_agents(self):
        """Carga los agentes disponibles en el sistema"""
        self.logger.info("Cargando agentes disponibles...")
        
        # Registrar todos los agentes predefinidos
        for agent_id in self.AVAILABLE_AGENTS:
            # Extraer el ID base sin el sufijo "_agent"
            base_id = agent_id.replace("_agent", "")
            self.logger.info(f"Registrando agente: {agent_id}")
            self.agents[base_id] = {"id": base_id, "loaded": False, "instance": None}
    
    def get_available_agents(self) -> List[str]:
        """
        Obtiene la lista de agentes disponibles
        
        Returns:
            List[str]: Lista de IDs de agentes disponibles
        """
        return list(self.agents.keys())
    
    def get_agent(self, agent_id: str):
        """
        Obtiene una instancia de un agente específico
        
        Args:
            agent_id: ID del agente
            
        Returns:
            Instancia del agente o None si no se pudo cargar
        """
        if agent_id not in self.agents:
            self.logger.error(f"El agente {agent_id} no está registrado")
            return None
        
        if not self.agents[agent_id]["loaded"] or self.agents[agent_id]["instance"] is None:
            self._load_agent(agent_id)
        
        return self.agents[agent_id]["instance"]
    
    def _load_agent(self, agent_id: str) -> bool:
        """
        Carga un agente específico
        
        Args:
            agent_id: ID del agente
            
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        try:
            # Construir el nombre del módulo
            module_name = f"src.agents.{agent_id}_agent"
            
            # Importar dinámicamente el módulo
            module = importlib.import_module(module_name)
            
            # Construir el nombre de la clase (CamelCase)
            class_name = ''.join(word.capitalize() for word in agent_id.split('_'))
            
            # Verificar si la clase existe en el módulo
            if hasattr(module, class_name):
                agent_class = getattr(module, class_name)
                
                # Inicializar el agente
                agent_instance = agent_class()
                
                # Registrar la instancia
                self.agents[agent_id]["instance"] = agent_instance
                self.agents[agent_id]["loaded"] = True
                
                self.logger.info(f"Agente {agent_id} cargado correctamente")
                return True
            else:
                self.logger.error(f"No se encontró la clase {class_name} en el módulo {module_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error al cargar el agente {agent_id}: {str(e)}", exc_info=True)
            # Manejo de error, pero mantenemos el agente en el registro
            self.agents[agent_id]["loaded"] = False
            self.agents[agent_id]["instance"] = None
            return False
    
    def run_agent(self, agent_id: str) -> bool:
        """
        Ejecuta un agente específico
        Args:
            agent_id: ID del agente
        Returns:
            bool: True si la ejecución fue exitosa, False en caso contrario
        """
        self.logger.info(f"Solicitando ejecución del agente {agent_id}")
        
        agent = self.get_agent(agent_id)
        if agent is None:
            self.logger.error(f"No se pudo obtener el agente {agent_id}")
            return False
        
        # Verificar si el agente ya está en ejecución
        status = self.get_agent_status(agent_id)
        if status.get("is_running", False):
            self.logger.warning(f"El agente {agent_id} ya está en ejecución")
            return False
        
        # Registrar inicio de ejecución
        start_time = time.time()
        
        # Actualizar estado
        agent.status = "running"
        
        # Ejecutar el agente
        try:
            # Ejecutar el flujo completo del agente
            success = agent.execute()
            
            # Registrar fin de ejecución
            end_time = time.time()
            duration = end_time - start_time
            
            # Registrar en el historial
            self._register_execution(agent_id, success, duration)
            
            # Actualizar estado
            agent.status = "completed" if success else "error"
            
            self.logger.info(f"Ejecución del agente {agent_id} completada. Éxito: {success}")
            return success
        
        except Exception as e:
            self.logger.error(f"Error durante la ejecución del agente {agent_id}: {str(e)}", exc_info=True)
            
            # Registrar fin de ejecución
            end_time = time.time()
            duration = end_time - start_time
            
            # Registrar en el historial
            self._register_execution(agent_id, False, duration, error=str(e))
            
            # Actualizar estado
            agent.status = "error"
            
            return False
    
    def _register_execution(self, agent_id: str, success: bool, duration: float, error: str = None) -> None:
        """
        Registra una ejecución en el historial
        Args:
            agent_id: ID del agente
            success: Si la ejecución fue exitosa
            duration: Duración de la ejecución en segundos
            error: Mensaje de error (opcional)
        """
        # Inicializar historial para el agente si no existe
        if agent_id not in self.execution_history:
            self.execution_history[agent_id] = []
        
        # Crear registro
        record = {
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration": duration
        }
        
        if error:
            record["error"] = error
        
        # Añadir al historial
        self.execution_history[agent_id].insert(0, record)  # Insertar al principio (más reciente primero)
        
        # Limitar historial a 100 registros
        if len(self.execution_history[agent_id]) > 100:
            self.execution_history[agent_id].pop()  # Eliminar el más antiguo
    
    def get_execution_history(self, agent_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de ejecuciones de un agente
        Args:
            agent_id: ID del agente
            limit: Número máximo de registros a devolver
        Returns:
            List[Dict[str, Any]]: Historial de ejecuciones
        """
        if agent_id not in self.execution_history:
            return []
        
        return self.execution_history[agent_id][:limit]
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Obtiene el estado actual de un agente
        Args:
            agent_id: ID del agente
        Returns:
            Dict[str, Any]: Estado del agente
        """
        agent = self.get_agent(agent_id)
        if agent is None:
            return {
                "id": agent_id,
                "name": agent_id.capitalize(),
                "loaded": False,
                "is_running": False,
                "status": "not_loaded"  # Valor por defecto para asegurar que siempre exista
            }
        
        try:
            # Obtener estado del agente
            status = agent.get_status()
            
            # Asegurar que la clave 'status' siempre exista
            if 'status' not in status:
                status['status'] = "ready"  # Estado por defecto
            
            return status
        
        except Exception as e:
            self.logger.error(f"Error al obtener el estado del agente {agent_id}: {str(e)}")
            
            # Devolver un estado básico en caso de error
            return {
                "id": agent_id,
                "name": getattr(agent, "name", agent_id.capitalize()),
                "loaded": True,
                "is_running": getattr(agent, "is_running", False),
                "status": "error"  # Estado en caso de error
            }