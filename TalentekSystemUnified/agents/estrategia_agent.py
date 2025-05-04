#!/usr/bin/env python3
"""
Estrategia Comercial - Agente para redacción de propuestas de valor
Este agente genera propuestas de valor según cliente y sector
"""
import os
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join("logs", "estrategia_agent.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TalentekIA-Estrategia")

class EstrategiaAgent:
    """Agente para generación de propuestas de valor comerciales"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el agente de estrategia comercial
        
        Args:
            config: Configuración específica (opcional)
        """
        self.config = config or {}
        
        # Configuración del agente
        self.plantillas_path = self.config.get("plantillas_path", "data/plantillas/")
        
        # Estado del agente
        self.status = "ready"
        self.last_execution = None
        self.results = {}
        
        # Crear directorios necesarios
        self.plantillas_dir = Path(self.plantillas_path)
        self.plantillas_dir.mkdir(parents=True, exist_ok=True)
        self.propuestas_dir = Path("data/propuestas")
        self.propuestas_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self) -> bool:
        """
        Ejecuta el flujo principal del agente
        
        Returns:
            bool: True si la ejecución fue exitosa
        """
        print("╔═══════════════════════════════════════════╗")
        print("║         ESTRATEGIA COMERCIAL              ║")
        print("╚═══════════════════════════════════════════╝")
        print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Generando propuestas de valor según sector...")
        
        self.status = "running"
        
        try:
            # Simulación de proceso
            print("Analizando datos de mercado...")
            logger.info("Analizando datos de mercado")
            print("Identificando puntos de dolor del cliente...")
            
            # Sectores simulados para generar propuestas
            sectores = [
                {"nombre": "Tecnología", "cliente": "Startup SaaS"},
                {"nombre": "Finanzas", "cliente": "Banco Digital"},
                {"nombre": "Educación", "cliente": "Universidad Online"}
            ]
            
            # Generar propuestas para cada sector
            propuestas = self.generar_propuestas(sectores)
            
            # Guardar resultados
            self.results = {
                "propuestas": propuestas,
                "timestamp": datetime.now().isoformat()
            }
            
            # Mostrar propuestas generadas
            print("\nPropuestas de valor generadas:")
            for propuesta in propuestas:
                print(f"\n## Sector: {propuesta['sector']} - Cliente: {propuesta['cliente']}")
                print("-------------------------------------------")
                print(f"Propuesta: {propuesta['texto']}")
            
            # Guardar propuestas en archivos
            self.guardar_propuestas(propuestas)
            
            print("\nGenerando documentos de presentación...")
            print("\nProceso completado exitosamente.")
            print(f"Las propuestas han sido guardadas en {self.propuestas_dir}/")
            
            self.last_execution = datetime.now()
            self.status = "completed"
            return True
            
        except Exception as e:
            logger.error(f"Error en la ejecución del agente de estrategia: {str(e)}", exc_info=True)
            self.status = "error"
            return False
    
    def generar_propuestas(self, sectores: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Genera propuestas de valor para los sectores especificados
        
        Args:
            sectores: Lista de sectores y clientes
            
        Returns:
            List: Lista de propuestas generadas
        """
        propuestas = []
        
        for sector in sectores:
            propuesta = {
                "sector": sector["nombre"],
                "cliente": sector["cliente"],
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "texto": "",
                "puntos_clave": []
            }
            
            # Generar texto según el sector
            if sector["nombre"] == "Tecnología":
                propuesta["texto"] = "Implementación de sistema de IA que reduce en un 40% el tiempo de respuesta al cliente mientras aumenta la precisión de las soluciones en un 25%, con ROI demostrable en menos de 6 meses."
                propuesta["puntos_clave"] = [
                    "Reducción del 40% en tiempo de respuesta",
                    "Aumento del 25% en precisión",
                    "ROI en menos de 6 meses",
                    "Integración con sistemas existentes"
                ]
            
            elif sector["nombre"] == "Finanzas":
                propuesta["texto"] = "Plataforma de análisis predictivo que identifica oportunidades de inversión con un 30% más de precisión que los métodos tradicionales, reduciendo el riesgo en un 20% y aumentando el rendimiento en un 15%."
                propuesta["puntos_clave"] = [
                    "30% más de precisión en identificación de oportunidades",
                    "Reducción del 20% en riesgo",
                    "Aumento del 15% en rendimiento",
                    "Cumplimiento normativo automatizado"
                ]
            
            elif sector["nombre"] == "Educación":
                propuesta["texto"] = "Sistema de aprendizaje adaptativo que personaliza el contenido según el perfil del estudiante, aumentando las tasas de finalización en un 60% y mejorando los resultados académicos en un 35%."
                propuesta["puntos_clave"] = [
                    "Contenido personalizado según perfil del estudiante",
                    "Aumento del 60% en tasas de finalización",
                    "Mejora del 35% en resultados académicos",
                    "Análisis detallado del progreso del estudiante"
                ]
            
            propuestas.append(propuesta)
        
        return propuestas
    
    def guardar_propuestas(self, propuestas: List[Dict[str, Any]]) -> None:
        """
        Guarda las propuestas generadas en archivos
        
        Args:
            propuestas: Lista de propuestas generadas
        """
        try:
            # Guardar todas las propuestas en un solo archivo JSON
            json_path = self.propuestas_dir / "propuestas_valor.json"
            with open(json_path, "w") as f:
                json.dump(propuestas, f, indent=2)
            
            # Guardar cada propuesta como un archivo Markdown separado
            for propuesta in propuestas:
                md_filename = f"propuesta_{propuesta['sector'].lower()}_{datetime.now().strftime('%Y%m%d')}.md"
                md_path = self.propuestas_dir / md_filename
                
                with open(md_path, "w") as f:
                    f.write(f"# Propuesta de Valor: {propuesta['sector']}\n\n")
                    f.write(f"**Cliente:** {propuesta['cliente']}\n")
                    f.write(f"**Fecha:** {propuesta['fecha']}\n\n")
                    f.write("## Propuesta\n\n")
                    f.write(f"{propuesta['texto']}\n\n")
                    f.write("## Puntos Clave\n\n")
                    for punto in propuesta['puntos_clave']:
                        f.write(f"- {punto}\n")
                    f.write("\n## Próximos Pasos\n\n")
                    f.write("1. Presentación inicial al cliente\n")
                    f.write("2. Recopilación de feedback\n")
                    f.write("3. Ajuste de propuesta según necesidades específicas\n")
                    f.write("4. Presentación de propuesta final\n\n")
                    f.write("---\n")
                    f.write("*Generado automáticamente por TalentekIA - Estrategia Comercial*\n")
            
            logger.info(f"Propuestas guardadas en {self.propuestas_dir}")
        except Exception as e:
            logger.error(f"Error al guardar propuestas: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del agente
        
        Returns:
            Dict: Estado del agente
        """
        return {
            "status": self.status,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "propuestas_generadas": len(self.results.get("propuestas", []))
        }

def main():
    """Función principal para ejecución independiente"""
    # Cargar configuración desde archivo TOML si existe
    config = {}
    try:
        import toml
        if Path("config/talentek_agentes_config.toml").exists():
            with open("config/talentek_agentes_config.toml", "r") as f:
                full_config = toml.load(f)
                if "agente_estrategia" in full_config:
                    config = full_config["agente_estrategia"]
    except ImportError:
        logger.warning("No se pudo importar toml. Usando configuración por defecto.")
    except Exception as e:
        logger.warning(f"Error al cargar configuración: {str(e)}")
    
    # Inicializar y ejecutar agente
    agent = EstrategiaAgent(config)
    success = agent.run()
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())