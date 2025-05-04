"""
Módulo base para todos los agentes de IA en TalentekAI Unified.
Este módulo define la clase base que todos los agentes deben heredar.
"""

import os
import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Tuple

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseAgent(ABC):
    """
    Clase base para todos los agentes de IA en TalentekAI.
    
    Esta clase define la interfaz común y funcionalidades compartidas
    que todos los agentes deben implementar.
    """
    
    def __init__(self, 
                 agent_id: str, 
                 config: Optional[Dict[str, Any]] = None,
                 model_name: Optional[str] = None,
                 **kwargs):
        """
        Inicializa un nuevo agente.
        
        Args:
            agent_id: Identificador único del agente
            config: Configuración del agente (opcional)
            model_name: Nombre del modelo a utilizar (opcional)
            **kwargs: Argumentos adicionales específicos del agente
        """
        self.agent_id = agent_id
        self.config = config or {}
        self.model_name = model_name
        self.logger = logging.getLogger(f"agent.{agent_id}")
        
        # Métricas y telemetría
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "total_processing_time": 0,
        }
        
        # Estado interno del agente
        self._is_initialized = False
        self._last_error = None
        self._conversation_history = []
        
        # Procesar argumentos adicionales
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # Inicializar el agente
        self._initialize()
    
    def _initialize(self) -> None:
        """
        Inicializa el agente y sus recursos.
        Este método puede ser sobrescrito por las clases hijas para
        realizar inicializaciones específicas.
        """
        try:
            self.logger.info(f"Inicializando agente {self.agent_id}")
            self._load_resources()
            self._is_initialized = True
            self.logger.info(f"Agente {self.agent_id} inicializado correctamente")
        except Exception as e:
            self._last_error = str(e)
            self.logger.error(f"Error al inicializar agente {self.agent_id}: {e}")
            raise
    
    def _load_resources(self) -> None:
        """
        Carga recursos necesarios para el agente.
        Este método debe ser implementado por las clases hijas.
        """
        pass
    
    @abstractmethod
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa una entrada y genera una respuesta.
        
        Args:
            input_data: Datos de entrada para procesar
            
        Returns:
            Diccionario con la respuesta y metadatos
        """
        pass
    
    def update_conversation_history(self, 
                                   user_input: str, 
                                   agent_response: str,
                                   metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Actualiza el historial de conversación del agente.
        
        Args:
            user_input: Entrada del usuario
            agent_response: Respuesta del agente
            metadata: Metadatos adicionales sobre la interacción
        """
        timestamp = time.time()
        entry = {
            "timestamp": timestamp,
            "user_input": user_input,
            "agent_response": agent_response,
            "metadata": metadata or {}
        }
        self._conversation_history.append(entry)
        
        # Limitar el tamaño del historial si es necesario
        max_history = self.config.get("max_history_size", 100)
        if len(self._conversation_history) > max_history:
            self._conversation_history = self._conversation_history[-max_history:]
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de conversación del agente.
        
        Returns:
            Lista con el historial de conversación
        """
        return self._conversation_history
    
    def clear_conversation_history(self) -> None:
        """Limpia el historial de conversación del agente."""
        self._conversation_history = []
    
    def update_metrics(self, 
                      success: bool, 
                      tokens: int = 0, 
                      processing_time: float = 0) -> None:
        """
        Actualiza las métricas del agente.
        
        Args:
            success: Si la solicitud fue exitosa
            tokens: Número de tokens utilizados
            processing_time: Tiempo de procesamiento en segundos
        """
        self.metrics["total_requests"] += 1
        if success:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1
        
        self.metrics["total_tokens"] += tokens
        self.metrics["total_processing_time"] += processing_time
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Obtiene las métricas actuales del agente.
        
        Returns:
            Diccionario con las métricas del agente
        """
        metrics = self.metrics.copy()
        
        # Calcular métricas derivadas
        if metrics["total_requests"] > 0:
            metrics["success_rate"] = metrics["successful_requests"] / metrics["total_requests"]
            metrics["avg_processing_time"] = metrics["total_processing_time"] / metrics["total_requests"]
            if metrics["successful_requests"] > 0:
                metrics["avg_tokens_per_request"] = metrics["total_tokens"] / metrics["successful_requests"]
        
        return metrics
    
    def save_state(self, filepath: str) -> bool:
        """
        Guarda el estado actual del agente en un archivo.
        
        Args:
            filepath: Ruta donde guardar el estado
            
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            state = {
                "agent_id": self.agent_id,
                "config": self.config,
                "model_name": self.model_name,
                "metrics": self.metrics,
                "conversation_history": self._conversation_history,
                # Las clases hijas pueden añadir más información al estado
                "additional_state": self._get_additional_state()
            }
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(state, f, indent=2)
            
            self.logger.info(f"Estado del agente guardado en {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error al guardar estado del agente: {e}")
            self._last_error = str(e)
            return False
    
    def load_state(self, filepath: str) -> bool:
        """
        Carga el estado del agente desde un archivo.
        
        Args:
            filepath: Ruta del archivo de estado
            
        Returns:
            True si se cargó correctamente, False en caso contrario
        """
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            # Verificar que el estado corresponde a este agente
            if state.get("agent_id") != self.agent_id:
                self.logger.warning(f"El estado cargado corresponde a otro agente: {state.get('agent_id')}")
            
            # Cargar estado
            self.config.update(state.get("config", {}))
            self.model_name = state.get("model_name", self.model_name)
            self.metrics = state.get("metrics", self.metrics)
            self._conversation_history = state.get("conversation_history", [])
            
            # Las clases hijas pueden procesar información adicional
            self._restore_additional_state(state.get("additional_state", {}))
            
            self.logger.info(f"Estado del agente cargado desde {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error al cargar estado del agente: {e}")
            self._last_error = str(e)
            return False
    
    def _get_additional_state(self) -> Dict[str, Any]:
        """
        Obtiene información adicional del estado del agente.
        Este método debe ser sobrescrito por las clases hijas que
        necesiten guardar información adicional.
        
        Returns:
            Diccionario con información adicional del estado
        """
        return {}
    
    def _restore_additional_state(self, additional_state: Dict[str, Any]) -> None:
        """
        Restaura información adicional del estado del agente.
        Este método debe ser sobrescrito por las clases hijas que
        necesiten restaurar información adicional.
        
        Args:
            additional_state: Información adicional del estado
        """
        pass
    
    def get_last_error(self) -> Optional[str]:
        """
        Obtiene el último error registrado.
        
        Returns:
            Mensaje del último error o None si no hay errores
        """
        return self._last_error
    
    def is_initialized(self) -> bool:
        """
        Verifica si el agente está inicializado correctamente.
        
        Returns:
            True si el agente está inicializado, False en caso contrario
        """
        return self._is_initialized
    
    def __str__(self) -> str:
        """Representación en string del agente."""
        return f"{self.__class__.__name__}(id={self.agent_id}, model={self.model_name})"
    
    def __repr__(self) -> str:
        """Representación oficial del agente."""
        return f"{self.__class__.__name__}(agent_id='{self.agent_id}', model_name='{self.model_name}')"