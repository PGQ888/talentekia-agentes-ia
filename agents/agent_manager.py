"""
Gestor de agentes para TalentekIA
Este módulo proporciona funciones para gestionar y ejecutar los agentes del sistema
"""
import os
import sys
import time
import logging
import importlib
import concurrent.futures
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TalentekIA-AgentManager")

# Asegurar que el directorio raíz está en el path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Crear directorio de logs si no existe
logs_dir = project_root / 'logs'
logs_dir.mkdir(exist_ok=True)

# Añadir manejador de archivo para logging
file_handler = logging.FileHandler(logs_dir / 'agent_manager.log', mode='a', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Importar después de configurar el path
try:
    from agents.config import get_all_agents, get_agent_config
    from scripts.env_loader import env
except ImportError as e:
    logger.error(f"Error al importar módulos necesarios: {e}")
    logger.error("Asegúrate de que la estructura del proyecto es correcta y que todos los módulos están instalados")
    sys.exit(1)

def get_available_agents() -> List[str]:
    """
    Obtiene la lista de agentes disponibles en el sistema
    
    Returns:
        List[str]: Lista de IDs de agentes disponibles
    """
    try:
        agents_config = get_all_agents()
        return list(agents_config.keys())
    except Exception as e:
        logger.error(f"Error al obtener la lista de agentes: {e}")
        return []

def load_agent(agent_id: str) -> Any:
    """
    Carga un agente específico
    
    Args:
        agent_id: ID del agente a cargar
        
    Returns:
        Any: Instancia del agente o None si no se pudo cargar
    """
    try:
        agent_config = get_agent_config(agent_id)
        if not agent_config:
            logger.error(f"No se encontró configuración para el agente {agent_id}")
            return None
    
        # Intentar importar el módulo del agente
        module_path = f"agents.{agent_id}_agent"
        module = importlib.import_module(module_path)
        
        # Crear una instancia del agente
        if hasattr(module, "create_agent"):
            logger.debug(f"Creando instancia del agente {agent_id}")
            return module.create_agent(agent_config)
        else:
            logger.error(f"El módulo {module_path} no tiene la función create_agent")
            return None
    
    except ImportError as e:
        logger.error(f"No se pudo importar el módulo para el agente {agent_id}: {e}")
        logger.error(f"Asegúrate de que el archivo agents/{agent_id}_agent.py existe")
        return None
    
    except Exception as e:
        logger.error(f"Error al cargar el agente {agent_id}: {str(e)}")
        return None

def execute_agent(agent_id: str, timeout: int = 3600) -> bool:
    """
    Ejecuta un agente específico con un tiempo límite opcional
    
    Args:
        agent_id: ID del agente a ejecutar
        timeout: Tiempo máximo de ejecución en segundos (por defecto 1 hora)
        
    Returns:
        bool: True si la ejecución fue exitosa, False en caso contrario
    """
    start_time = time.time()
    logger.info(f"Solicitando ejecución del agente {agent_id}")
    
    try:
        agent = load_agent(agent_id)
        if not agent:
            logger.error(f"No se pudo cargar el agente {agent_id}")
            return False
        
        # Ejecutar con límite de tiempo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(agent.execute)
            try:
                result = future.result(timeout=timeout)
                execution_time = time.time() - start_time
                logger.info(f"Agente {agent_id} ejecutado en {execution_time:.2f} segundos")
                log_execution(agent_id, result, execution_time)
                return result
            except concurrent.futures.TimeoutError:
                logger.error(f"La ejecución del agente {agent_id} excedió el tiempo límite de {timeout} segundos")
                log_execution(agent_id, False, timeout)
                return False
    
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error durante la ejecución del agente {agent_id} después de {execution_time:.2f} segundos: {e}")
        log_execution(agent_id, False, execution_time)
        return False

def execute_multiple_agents(agent_ids: List[str], parallel: bool = False) -> Dict[str, bool]:
    """
    Ejecuta múltiples agentes, ya sea en serie o en paralelo
    
    Args:
        agent_ids: Lista de IDs de agentes a ejecutar
        parallel: Si es True, ejecuta los agentes en paralelo
        
    Returns:
        Dict[str, bool]: Diccionario con los resultados de ejecución para cada agente
    """
    results = {}
    
    if parallel:
        # Ejecución en paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Crear un futuro para cada agente
            future_to_agent = {executor.submit(execute_agent, agent_id): agent_id for agent_id in agent_ids}
            
            # Procesar los resultados a medida que se completan
            for future in concurrent.futures.as_completed(future_to_agent):
                agent_id = future_to_agent[future]
                try:
                    results[agent_id] = future.result()
                except Exception as e:
                    logger.error(f"Error en la ejecución paralela del agente {agent_id}: {e}")
                    results[agent_id] = False
    else:
        # Ejecución en serie
        for agent_id in agent_ids:
            results[agent_id] = execute_agent(agent_id)
    
    return results

def get_agent_status(agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene el estado actual de un agente
    
    Args:
        agent_id: ID del agente
        
    Returns:
        Optional[Dict[str, Any]]: Estado del agente o None si no se pudo obtener
    """
    try:
        agent = load_agent(agent_id)
        if not agent:
            logger.error(f"No se pudo cargar el agente {agent_id} para obtener su estado")
            return None
        
        status = agent.get_status()
        # Añadir información adicional
        status['last_check'] = datetime.now().isoformat()
        
        return status
    except Exception as e:
        logger.error(f"Error al obtener el estado del agente {agent_id}: {e}")
        return None

def get_all_agents_status() -> Dict[str, Dict[str, Any]]:
    """
    Obtiene el estado de todos los agentes
    
    Returns:
        Dict[str, Dict[str, Any]]: Diccionario con el estado de cada agente
    """
    result = {}
    for agent_id in get_available_agents():
        try:
            status = get_agent_status(agent_id)
            if status:
                result[agent_id] = status
        except Exception as e:
            logger.error(f"Error al obtener el estado del agente {agent_id}: {e}")
    
    return result

def check_agent_health(agent_id: str) -> Tuple[bool, str]:
    """
    Verifica la salud de un agente comprobando su configuración y dependencias
    
    Args:
        agent_id: ID del agente a verificar
        
    Returns:
        Tuple[bool, str]: (está_saludable, mensaje)
    """
    try:
        # 1. Verificar si existe la configuración
        config = get_agent_config(agent_id)
        if not config:
            return False, f"No existe configuración para el agente {agent_id}"
        
        # 2. Verificar si se puede cargar el agente
        agent = load_agent(agent_id)
        if not agent:
            return False, f"No se puede cargar el agente {agent_id}"
        
        # 3. Verificar si existen los archivos de salida
        status = agent.get_status()
        if not status:
            return False, f"No se puede obtener el estado del agente {agent_id}"
        
        # 4. Verificar dependencias específicas del agente (si el agente tiene un método para ello)
        if hasattr(agent, "check_dependencies"):
            deps_ok, deps_msg = agent.check_dependencies()
            if not deps_ok:
                return False, f"Dependencias del agente {agent_id} no satisfechas: {deps_msg}"
        
        return True, f"El agente {agent_id} está en buen estado"
    
    except Exception as e:
        return False, f"Error al verificar la salud del agente {agent_id}: {str(e)}"

def log_execution(agent_id: str, success: bool, duration: float):
    """
    Registra una ejecución en el historial
    
    Args:
        agent_id: ID del agente
        success: Si la ejecución fue exitosa
        duration: Duración de la ejecución en segundos
    """
    log_file = logs_dir / "execution_history.log"
    
    try:
        timestamp = datetime.now().isoformat()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp}|{agent_id}|{success}|{duration:.2f}\n")
    except Exception as e:
        logger.error(f"Error al registrar ejecución en el historial: {e}")

def get_execution_history(agent_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Obtiene el historial de ejecuciones de un agente o de todos los agentes
    
    Args:
        agent_id: ID del agente (opcional, si es None devuelve para todos)
        limit: Número máximo de registros a devolver
        
    Returns:
        List[Dict[str, Any]]: Lista de registros de ejecución
    """
    history = []
    log_file = logs_dir / "execution_history.log"
    
    if not log_file.exists():
        return history
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in reversed(lines[-limit*2:]):  # Leer el doble por si hay que filtrar
            if not line.strip():
                continue
                
            try:
                parts = line.strip().split("|")
                if len(parts) >= 4:
                    record = {
                        "timestamp": parts[0].strip(),
                        "agent_id": parts[1].strip(),
                        "success": parts[2].strip().lower() == "true",
                        "duration": parts[3].strip()
                    }
                    
                    if agent_id is None or record["agent_id"] == agent_id:
                        history.append(record)
                        
                        if len(history) >= limit:
                            break
            except Exception:
                continue
    except Exception as e:
        logger.error(f"Error al leer el historial de ejecuciones: {e}")
    
    return history

if __name__ == "__main__":
    # Si se ejecuta como script principal, permitir ejecutar agentes desde la línea de comandos
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestor de agentes TalentekIA")
    parser.add_argument("--list", action="store_true", help="Listar agentes disponibles")
    parser.add_argument("--execute", type=str, help="Ejecutar un agente específico")
    parser.add_argument("--execute-all", action="store_true", help="Ejecutar todos los agentes")
    parser.add_argument("--execute-parallel", action="store_true", help="Ejecutar agentes en paralelo (con --execute-all o --execute-multiple)")
    parser.add_argument("--execute-multiple", type=str, help="Ejecutar múltiples agentes (separados por comas)")
    parser.add_argument("--timeout", type=int, default=3600, help="Tiempo máximo de ejecución en segundos (por defecto 1 hora)")
    parser.add_argument("--status", type=str, help="Obtener estado de un agente específico")
    parser.add_argument("--all-status", action="store_true", help="Obtener estado de todos los agentes")
    parser.add_argument("--health-check", type=str, help="Verificar la salud de un agente específico")
    parser.add_argument("--history", type=str, help="Ver historial de ejecuciones de un agente específico")
    parser.add_argument("--all-history", action="store_true", help="Ver historial de ejecuciones de todos los agentes")
    parser.add_argument("--limit", type=int, default=10, help="Límite de registros para el historial")
    
    args = parser.parse_args()
    
    if args.list:
        print("Agentes disponibles:")
        for agent_id in get_available_agents():
            config = get_agent_config(agent_id)
            print(f"- {agent_id}: {config.get('name', agent_id.capitalize())}")
            print(f"  {config.get('description', 'Sin descripción')}")
            print(f"  Frecuencia: {config.get('update_frequency', 'Manual')}")
    elif args.execute:
        start_time = time.time()
        success = execute_agent(args.execute, timeout=args.timeout)
        duration = time.time() - start_time
        print(f"Ejecución del agente {args.execute}: {'Exitosa' if success else 'Fallida'}")
        print(f"Duración: {duration:.2f} segundos")
    
    elif args.execute_all:
        agents = get_available_agents()
        start_time = time.time()
        results = execute_multiple_agents(agents, parallel=args.execute_parallel)
        duration = time.time() - start_time
        
        print(f"Ejecución de todos los agentes {'en paralelo' if args.execute_parallel else 'en serie'}:")
        for agent_id, success in results.items():
            print(f"- {agent_id}: {'Exitosa' if success else 'Fallida'}")
        print(f"Duración total: {duration:.2f} segundos")
    
    elif args.execute_multiple:
        agents = [a.strip() for a in args.execute_multiple.split(",")]
        start_time = time.time()
        results = execute_multiple_agents(agents, parallel=args.execute_parallel)
        duration = time.time() - start_time
        
        print(f"Ejecución de agentes seleccionados {'en paralelo' if args.execute_parallel else 'en serie'}:")
        for agent_id, success in results.items():
            print(f"- {agent_id}: {'Exitosa' if success else 'Fallida'}")
        print(f"Duración total: {duration:.2f} segundos")
    
    elif args.status:
        status = get_agent_status(args.status)
        if status:
            print(f"Estado del agente {args.status}:")
            for key, value in status.items():
                print(f"- {key}: {value}")
        else:
            print(f"No se pudo obtener el estado del agente {args.status}")
    
    elif args.all_status:
        status_dict = get_all_agents_status()
        if not status_dict:
            print("No se pudo obtener el estado de ningún agente")
        else:
            print("Estado de todos los agentes:")
            for agent_id, status in status_dict.items():
                print(f"\n{status.get('name', agent_id.capitalize())} ({agent_id}):")
                print(f"- Última ejecución: {status.get('last_run') or 'Nunca'}")
                print(f"- En ejecución: {'Sí' if status.get('is_running', False) else 'No'}")
                print(f"- Frecuencia: {status.get('update_frequency', 'Desconocida')}")
                print(f"- CSV: {'Existe' if status.get('csv_exists', False) else 'No existe'}")
                print(f"- Informe: {'Existe' if status.get('md_exists', False) else 'No existe'}")
    
    elif args.health_check:
        healthy, message = check_agent_health(args.health_check)
        status = "✅ SALUDABLE" if healthy else "❌ PROBLEMAS"
        print(f"Salud del agente {args.health_check}: {status}")
        print(f"Mensaje: {message}")
    
    elif args.history or args.all_history:
        agent_id = args.history if args.history else None
        history = get_execution_history(agent_id, args.limit)
        
        if not history:
            print(f"No hay registros de ejecución{' para el agente ' + agent_id if agent_id else ''}")
        else:
            print(f"Historial de ejecuciones{' para el agente ' + agent_id if agent_id else ''}:")
            for record in history:
                status = "✅ Exitosa" if record["success"] else "❌ Fallida"
                print(f"- {record['timestamp']} | {record['agent_id']} | {status} | {record['duration']}s")
    
    else:
        parser.print_help()
