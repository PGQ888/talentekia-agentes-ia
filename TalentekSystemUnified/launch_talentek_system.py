#!/usr/bin/env python3
"""
Lanzador unificado para el sistema TalentekIA
Optimizado para Mac M2 y basado en configuración TOML
"""

import os
import sys
import time
import asyncio
import logging
import argparse
import toml
import importlib
from datetime import datetime, timedelta
from pathlib import Path
import platform
import subprocess
from typing import Dict, List, Any, Optional, Tuple

# Configurar rutas base
ROOT_DIR = Path(__file__).parent
CONFIG_PATH = ROOT_DIR / "config" / "talentek_agentes_config.toml"

# Asegurar que estamos en el directorio correcto
os.chdir(ROOT_DIR)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROOT_DIR / "logs" / f"talentek_system_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)

logger = logging.getLogger("TalentekSystemUnified")

class TalentekSystem:
    """Sistema unificado de gestión de agentes de TalentekIA"""
    
    def __init__(self):
        """Inicializa el sistema unificado"""
        self.config = self.load_config()
        self.agents = {}
        self.agent_instances = {}
        self.ensure_directories()
        
        # Verificar si estamos en Mac M2/M1
        if self.is_apple_silicon():
            self.apply_m2_optimizations()
    
    def load_config(self) -> Dict:
        """Carga la configuración desde el archivo TOML"""
        try:
            if not CONFIG_PATH.exists():
                logger.error(f"Archivo de configuración no encontrado: {CONFIG_PATH}")
                sys.exit(1)
                
            config = toml.load(CONFIG_PATH)
            logger.info(f"Configuración cargada desde {CONFIG_PATH}")
            return config
        except Exception as e:
            logger.error(f"Error al cargar la configuración: {str(e)}")
            sys.exit(1)
    
    def ensure_directories(self):
        """Crea los directorios necesarios si no existen"""
        directories = [
            "logs",
            "data",
            "data/temp",
            "data/finanzas",
            "data/informes",
            "data/plantillas"
        ]
        
        for directory in directories:
            path = ROOT_DIR / directory
            path.mkdir(parents=True, exist_ok=True)
    
    def is_apple_silicon(self) -> bool:
        """Detecta si estamos en un Mac con Apple Silicon"""
        return platform.system() == "Darwin" and platform.machine() == "arm64"
    
    def apply_m2_optimizations(self):
        """Aplica optimizaciones específicas para Mac M1/M2"""
        logger.info("Detectado Mac con Apple Silicon, aplicando optimizaciones...")
        
        # Configurar variables de entorno para optimizar el rendimiento
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
        
        # Verificar si PyTorch está disponible y configurar MPS
        try:
            import torch
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                logger.info("MPS (Metal Performance Shaders) disponible para PyTorch")
                os.environ["PYTORCH_DEVICE"] = "mps"
            else:
                logger.warning("MPS no disponible para PyTorch en este sistema")
        except ImportError:
            logger.warning("No se pudo importar PyTorch para optimizaciones M2")
    
    def get_agent_configs(self) -> Dict[str, Dict]:
        """Obtiene la configuración de todos los agentes disponibles"""
        agent_configs = {}
        
        for key, value in self.config.items():
            if key.startswith('agente_'):
                agent_id = key.replace('agente_', '')
                agent_configs[agent_id] = value
                
        return agent_configs
    
    def load_agent(self, agent_id: str) -> Tuple[bool, str]:
        """
        Carga un agente específico basado en su configuración
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        agent_configs = self.get_agent_configs()
        
        if agent_id not in agent_configs:
            return False, f"Agente {agent_id} no encontrado en la configuración"
        
        agent_config = agent_configs[agent_id]
        script_path = agent_config.get('script', '')
        
        if not script_path:
            return False, f"Ruta de script no definida para el agente {agent_id}"
        
        # Construir la ruta completa al script
        script_full_path = ROOT_DIR / script_path
        
        if not script_full_path.exists():
            return False, f"Script {script_full_path} no encontrado"
        
        try:
            # Determinar el nombre de módulo a partir de la ruta
            module_path = str(script_full_path).replace(str(ROOT_DIR) + os.sep, '').replace('/', '.').replace('\\', '.').replace('.py', '')
            
            # Importar el módulo dinámicamente
            spec = importlib.util.spec_from_file_location(module_path, script_full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Buscar la clase del agente (convención: archivo linkedin_agent.py -> clase LinkedinAgent)
            class_name = ''.join(word.capitalize() for word in agent_id.split('_')) + 'Agent'
            
            if hasattr(module, class_name):
                agent_class = getattr(module, class_name)
                self.agent_instances[agent_id] = agent_class(agent_id=agent_id, config=agent_config)
                self.agents[agent_id] = {
                    'config': agent_config,
                    'module': module_path,
                    'class': class_name
                }
                return True, f"Agente {agent_id} cargado correctamente"
            else:
                return False, f"Clase {class_name} no encontrada en el módulo {module_path}"
                
        except Exception as e:
            return False, f"Error al cargar el agente {agent_id}: {str(e)}"
    
    async def run_agent(self, agent_id: str) -> Dict[str, Any]:
        """Ejecuta un agente y devuelve su resultado"""
        logger.info(f"Iniciando ejecución del agente: {agent_id}")
        
        if agent_id not in self.agent_instances:
            success, message = self.load_agent(agent_id)
            if not success:
                logger.error(message)
                return {
                    "agent_id": agent_id,
                    "success": False,
                    "message": message,
                    "duration": 0
                }
        
        agent = self.agent_instances[agent_id]
        start_time = time.time()
        
        try:
            # Ejecutar el agente
            success = agent.run()
            
            # Generar y guardar informes si la ejecución fue exitosa
            if success and hasattr(agent, 'results') and agent.results:
                # Procesar datos
                df = agent.process_data(agent.results)
                
                # Generar informe
                report = agent.generate_report(df)
                
                # Guardar resultados
                if hasattr(agent, 'save_results'):
                    agent.save_results(df, report)
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            status = "✅ Completado" if success else "❌ Error"
            logger.info(f"Agente {agent_id}: {status} en {duration}s")
            
            return {
                "agent_id": agent_id,
                "success": success,
                "duration": duration,
                "name": self.agents[agent_id]['config'].get('nombre', agent_id)
            }
            
        except Exception as e:
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            logger.error(f"Error al ejecutar el agente {agent_id}: {str(e)}")
            
            return {
                "agent_id": agent_id,
                "success": False,
                "duration": duration,
                "message": str(e),
                "name": self.agents[agent_id]['config'].get('nombre', agent_id) if agent_id in self.agents else agent_id
            }
    
    async def run_all_agents(self, parallel=True) -> List[Dict[str, Any]]:
        """Ejecuta todos los agentes disponibles en paralelo o secuencialmente"""
        agent_configs = self.get_agent_configs()
        
        if not agent_configs:
            logger.error("No se encontraron agentes configurados")
            return []
        
        logger.info(f"Iniciando ejecución de {len(agent_configs)} agentes. Modo: {'paralelo' if parallel else 'secuencial'}")
        
        results = []
        
        if parallel:
            # Ejecución en paralelo
            tasks = [self.run_agent(agent_id) for agent_id in agent_configs.keys()]
            results = await asyncio.gather(*tasks)
        else:
            # Ejecución secuencial
            for agent_id in agent_configs.keys():
                result = await self.run_agent(agent_id)
                results.append(result)
        
        return results

def print_banner(config):
    """Muestra el banner de inicio personalizado"""
    entorno = config.get('entorno', {})
    personalizacion = config.get('personalizacion', {})
    nombre_entorno = entorno.get('nombre', 'TalentekSystem')
    usuario = personalizacion.get('usuario', 'Usuario')
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║          {nombre_entorno.upper()} - LANZADOR UNIFICADO          ║
║                                                           ║
║      Sistema personalizado para: {usuario}        ║
║      Optimizado para Mac {entorno.get('chip', 'M2')}                          ║
╚═══════════════════════════════════════════════════════════╝
    """)

def generate_summary(results):
    """Genera un resumen de la ejecución de los agentes"""
    success_count = sum(1 for r in results if r.get("success", False))
    total_count = len(results)
    total_duration = sum(r.get("duration", 0) for r in results)
    
    print("\n===== RESUMEN DE EJECUCIÓN =====")
    print(f"Total de agentes: {total_count}")
    print(f"Exitosos: {success_count}")
    print(f"Fallidos: {total_count - success_count}")
    print(f"Duración total: {total_duration:.2f}s")
    print(f"Tiempo promedio: {total_duration/total_count if total_count else 0:.2f}s")
    print()
    
    # Tabla de resultados
    print(f"{'AGENTE':<20} {'NOMBRE':<25} {'ESTADO':<10} {'DURACIÓN':<10}")
    print("=" * 65)
    for r in results:
        status = "✅ Éxito" if r.get("success", False) else "❌ Error"
        name = r.get("name", r.get("agent_id", "Desconocido"))
        print(f"{r.get('agent_id', 'Desconocido'):<20} {name:<25} {status:<10} {r.get('duration', 0):.2f}s")

async def main_async():
    """Función principal asíncrona"""
    # Inicializar el sistema
    system = TalentekSystem()
    
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Lanzador unificado de TalentekSystem')
    parser.add_argument('--sequential', action='store_true', help='Ejecutar agentes secuencialmente')
    parser.add_argument('--agent', type=str, help='Ejecutar un agente específico')
    parser.add_argument('--list', action='store_true', help='Listar agentes disponibles')
    args = parser.parse_args()
    
    # Mostrar banner
    print_banner(system.config)
    
    # Crear directorio de logs si no existe
    log_dir = ROOT_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Listar agentes si se solicita
    if args.list:
        agent_configs = system.get_agent_configs()
        print("\n===== AGENTES DISPONIBLES =====")
        for agent_id, config in agent_configs.items():
            print(f"- {agent_id}: {config.get('nombre', 'Sin nombre')} - {config.get('descripcion', 'Sin descripción')}")
        return 0
    
    # Configurar modo de ejecución
    parallel = not args.sequential
    
    # Ejecutar agentes
    if args.agent:
        # Ejecutar un agente específico
        logger.info(f"Ejecutando agente específico: {args.agent}")
        result = await system.run_agent(args.agent)
        results = [result]
    else:
        # Ejecutar todos los agentes
        results = await system.run_all_agents(parallel)
    
    # Generar resumen
    generate_summary(results)
    
    return 0

def main():
    """Función principal que ejecuta el bucle de eventos asyncio"""
    try:
        # Crear bucle de eventos
        loop = asyncio.get_event_loop()
        exit_code = loop.run_until_complete(main_async())
        return exit_code
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario")
        return 1
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        return 1
    finally:
        # Cerrar el bucle de eventos
        try:
            loop.close()
        except:
            pass

if __name__ == "__main__":
    # Verificar si estamos en Mac M2
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        print("✅ Optimizaciones para Mac M2 disponibles")
    
    # Ejecutar programa principal
    sys.exit(main())