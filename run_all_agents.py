#!/usr/bin/env python3
"""
Script para ejecutar todos los agentes de TalentekIA de forma coordinada
Optimizado para Mac M2
"""

import os
import sys
import time
import asyncio
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Configurar directorio raíz en el path
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

# Importaciones de la aplicación
from src.utils.env_loader import env
from src.agents.agent_manager import AgentManager
from src.utils.async_helper import run_async

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(root_dir / "logs" / f"agents_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)

logger = logging.getLogger("TalentekIA-Runner")

def print_banner():
    """Muestra el banner de inicio"""
    print("""
╔═══════════════════════════════════════════════╗
║             TALENTEK IA - RUNNER              ║
║      Ejecución coordinada de agentes IA       ║
║           Optimizado para Mac M2              ║
╚═══════════════════════════════════════════════╝
    """)

async def run_agent(manager, agent_id):
    """Ejecuta un agente y registra su resultado"""
    logger.info(f"Iniciando ejecución del agente: {agent_id}")
    
    # Simular operación asíncrona
    start_time = time.time()
    success = manager.run_agent(agent_id)
    end_time = time.time()
    
    duration = round(end_time - start_time, 2)
    status = "✅ Completado" if success else "❌ Error"
    
    logger.info(f"Agente {agent_id}: {status} en {duration}s")
    return {
        "agent_id": agent_id,
        "success": success,
        "duration": duration
    }

async def run_all_agents(parallel=True):
    """Ejecuta todos los agentes disponibles en paralelo o secuencialmente"""
    manager = AgentManager()
    agents = manager.get_available_agents()
    
    if not agents:
        logger.error("No se encontraron agentes disponibles")
        return []
    
    logger.info(f"Iniciando ejecución de {len(agents)} agentes. Modo: {'paralelo' if parallel else 'secuencial'}")
    
    results = []
    
    if parallel:
        # Ejecución en paralelo
        tasks = [run_agent(manager, agent_id) for agent_id in agents]
        results = await asyncio.gather(*tasks)
    else:
        # Ejecución secuencial
        for agent_id in agents:
            result = await run_agent(manager, agent_id)
            results.append(result)
    
    return results

def generate_summary(results):
    """Genera un resumen de la ejecución de los agentes"""
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    total_duration = sum(r["duration"] for r in results)
    
    print("\n===== RESUMEN DE EJECUCIÓN =====")
    print(f"Total de agentes: {total_count}")
    print(f"Exitosos: {success_count}")
    print(f"Fallidos: {total_count - success_count}")
    print(f"Duración total: {total_duration:.2f}s")
    print(f"Tiempo promedio: {total_duration/total_count if total_count else 0:.2f}s")
    print()
    
    # Tabla de resultados
    print(f"{'AGENTE':<20} {'ESTADO':<12} {'DURACIÓN':<10}")
    print("=" * 42)
    for r in results:
        status = "✅ Éxito" if r["success"] else "❌ Error"
        print(f"{r['agent_id']:<20} {status:<12} {r['duration']:.2f}s")

@run_async
async def main():
    """Función principal"""
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Ejecutar agentes TalentekIA')
    parser.add_argument('--sequential', action='store_true', help='Ejecutar agentes secuencialmente')
    parser.add_argument('--agent', type=str, help='Ejecutar un agente específico')
    args = parser.parse_args()
    
    # Mostrar banner
    print_banner()
    
    # Crear directorio de logs si no existe
    log_dir = root_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configurar modo de ejecución
    parallel = not args.sequential
    
    # Ejecutar agentes
    manager = AgentManager()
    
    if args.agent:
        # Ejecutar un agente específico
        logger.info(f"Ejecutando agente específico: {args.agent}")
        result = await run_agent(manager, args.agent)
        results = [result] if result else []
    else:
        # Ejecutar todos los agentes
        results = await run_all_agents(parallel)
    
    # Generar resumen
    generate_summary(results)
    
    return 0

if __name__ == "__main__":
    # Verificar conexión M2
    if os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") == "1":
        print("✅ Optimizaciones para Mac M2 aplicadas")
    
    # Ejecutar programa principal
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        sys.exit(1)