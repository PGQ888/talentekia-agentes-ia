import streamlit as st
import subprocess
import time
import pandas as pd
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
# Configuración de la página
st.set_page_config(page_title="Sistema TalentekAI", layout="wide")
st.title("🧠 Sistema TalentekAI Unified")

# --- Funciones de utilidad ---
def run_docker_command(command, success_message, error_message):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd="..",  # Asegura que se ejecute desde el directorio raíz del proyecto
        )
        if result.returncode == 0:
            return {"success": True, "message": success_message, "output": result.stdout}
        else:
            return {"success": False, "message": error_message, "output": result.stderr}
except Exception as e:
        return {"success": False, "message": f"Error al ejecutar el comando: {e}", "output": str(e)}

def get_container_status():
    try:
        docker_ps = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}},{{.Status}},{{.Ports}}"],
            capture_output=True,
            text=True
        )
        
        containers = []
        if docker_ps.returncode == 0 and docker_ps.stdout.strip():
            for line in docker_ps.stdout.strip().split('\n'):
                if line:
                    parts = line.split(',', 2)
                    if len(parts) >= 2:
                        name = parts[0]
                        status = parts[1]
                        ports = parts[2] if len(parts) > 2 else ""
                        
                        # Determinar el estado para el color
                        if "Up" in status and "healthy" in status:
                            state = "✅ Saludable"
                        elif "Up" in status and "unhealthy" in status:
                            state = "⚠️ No saludable"
                        elif "Up" in status:
                            state = "🟡 En ejecución"
                        elif "Restarting" in status:
                            state = "🔄 Reiniciando"
                        else:
                            state = "❌ Detenido"
                            
                        containers.append({
                            "Contenedor": name,
                            "Estado": state,
                            "Status": status,
                            "Puertos": ports
                        })
        return containers
    except Exception as e:
        return []

def read_log_file(file_path, num_lines=50):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                return ''.join(lines[-num_lines:])
        else:
            return f"El archivo {file_path} no existe."
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

def generate_system_report():
    report = "# Informe del Sistema TalentekAI\n\n"
    report += f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Añadir estado de los contenedores
    report += "## Estado de los contenedores\n\n"
    containers = get_container_status()
    if containers:
        for container in containers:
            report += f"- **{container['Contenedor']}**: {container['Estado']} ({container['Status']})\n"
    else:
        report += "No se encontraron contenedores en ejecución.\n"
    
    # Añadir información de recursos
    try:
        docker_stats = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}"],
            capture_output=True,
            text=True
        )
        
        if docker_stats.returncode == 0 and docker_stats.stdout.strip():
            report += "\n## Uso de recursos\n\n"
            for line in docker_stats.stdout.strip().split('\n'):
                if line:
                    parts = line.split(',')
                    if len(parts) >= 4:
                        report += f"- **{parts[0]}**: CPU {parts[1]}, Memoria {parts[2]} ({parts[3]})\n"
    except:
        pass
    
    # Guardar el informe
    os.makedirs("../reports", exist_ok=True)
    report_path = "../reports/system_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    
    return report_path, report

def check_ollama_status():
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except:
        return False, None

def setup_ollama():
    try:
        # Verificar si Ollama está instalado
        result = subprocess.run(
            ["which", "ollama"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, "Ollama no está instalado. Por favor, instálalo desde https://ollama.ai"
        
        # Verificar si Ollama está en ejecución
        ollama_running, _ = check_ollama_status()
        if not ollama_running:
            # Intentar iniciar Ollama
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(5)  # Esperar a que Ollama inicie
            
            # Verificar nuevamente
            ollama_running, _ = check_ollama_status()
            if not ollama_running:
                return False, "No se pudo iniciar Ollama. Por favor, inicia Ollama manualmente."
        
        # Verificar si el modelo talentek-custom existe
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        
        if "talentek-custom" not in result.stdout and "mistral" not in result.stdout:
            # Descargar el modelo mistral
            st.info("Descargando modelo mistral. Esto puede tardar unos minutos...")
            subprocess.run(
                ["ollama", "pull", "mistral"],
                capture_output=True,
                text=True
            )
            
            # Crear un modelo personalizado basado en mistral
            modelfile = """
FROM mistral
PARAMETER temperature 0.7
SYSTEM Eres TalentekGPT, un asistente de IA personalizado para Pablo Giráldez, con contexto completo sobre su entorno, herramientas e integraciones. Responde con claridad, precisión y proactividad.
"""
            with open("/tmp/Modelfile", "w") as f:
                f.write(modelfile)
            
            st.info("Creando modelo personalizado talentek-custom...")
            subprocess.run(
                ["ollama", "create", "talentek-custom", "-f", "/tmp/Modelfile"],
                capture_output=True,
                text=True
            )
        
        # Actualizar el archivo .env para usar el LLM local
        env_path = "../.env"
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                env_content = f.read()
            
            if "USE_LOCAL_LLM" not in env_content:
                with open(env_path, "a") as f:
                    f.write("\n# Configuración del LLM local\n")
                    f.write("USE_LOCAL_LLM=true\n")
                    f.write("LOCAL_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions\n")
            else:
                # Actualizar las variables existentes
                lines = env_content.split("\n")
                updated_lines = []
                for line in lines:
                    if line.startswith("USE_LOCAL_LLM="):
                        updated_lines.append("USE_LOCAL_LLM=true")
                    elif line.startswith("LOCAL_LLM_ENDPOINT="):
                        updated_lines.append("LOCAL_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions")
                    else:
                        updated_lines.append(line)
                
                with open(env_path, "w") as f:
                    f.write("\n".join(updated_lines))
        else:
            # Crear el archivo .env si no existe
            with open(env_path, "w") as f:
                f.write("# Configuración del LLM local\n")
                f.write("USE_LOCAL_LLM=true\n")
                f.write("LOCAL_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions\n")
        
        return True, "Ollama configurado correctamente con el modelo talentek-custom"
    except Exception as e:
        return False, f"Error al configurar Ollama: {str(e)}"

# --- Funciones del asistente ---
def procesar_mensaje_chat(mensaje):
    # Cargar variables de entorno
    load_dotenv()
    
    USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    LOCAL_LLM_ENDPOINT = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:11434/v1/chat/completions")
    
    # Definir las funciones disponibles para el asistente
    functions = [
        {
            "name": "lanzar_sistema",
            "description": "Inicia todos los contenedores del sistema TalentekAI",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "detener_sistema",
            "description": "Detiene todos los contenedores del sistema TalentekAI",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "reiniciar_sistema",
            "description": "Reinicia todos los contenedores del sistema TalentekAI",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "verificar_estado",
            "description": "Verifica el estado actual de los contenedores del sistema",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "ver_logs",
            "description": "Muestra los logs de un contenedor específico",
            "parameters": {
                "type": "object",
                "properties": {
                    "contenedor": {
                        "type": "string",
                        "description": "Nombre del contenedor (talentek_ui, talentek_api, talentek_agent, talentek_scheduler, talentek_anythingllm, talentek_qdrant)"
                    },
                    "num_lineas": {
                        "type": "integer",
                        "description": "Número de líneas a mostrar"
                    }
                },
                "required": ["contenedor"]
            }
        },
        {
            "name": "generar_informe",
            "description": "Genera un informe completo del estado del sistema",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "leer_documento",
            "description": "Lee un archivo de texto o documento del sistema",
            "parameters": {
                "type": "object",
                "properties": {
                    "ruta_archivo": {
                        "type": "string",
                        "description": "Ruta del archivo a leer"
                    }
                },
                "required": ["ruta_archivo"]
            }
        }
    ]
    
    # Ejecutar la función correspondiente
    def execute_function(function_name, arguments={}):
        if function_name == "lanzar_sistema":
            result = run_docker_command(
                ["docker-compose", "up", "-d", "--build"],
                "Sistema lanzado correctamente.",
                "Error al lanzar el sistema."
            )
            return f"{result['message']}\n\n{result['output']}"
            
        elif function_name == "detener_sistema":
            result = run_docker_command(
                ["docker-compose", "down"],
                "Sistema detenido correctamente.",
                "Error al detener el sistema."
            )
            return f"{result['message']}\n\n{result['output']}"
            
        elif function_name == "reiniciar_sistema":
            result = run_docker_command(
                ["docker-compose", "restart"],
                "Sistema reiniciado correctamente.",
                "Error al reiniciar el sistema."
            )
            return f"{result['message']}\n\n{result['output']}"
            
        elif function_name == "verificar_estado":
            containers = get_container_status()
            if containers:
                response = "Estado actual de los contenedores:\n\n"
                for container in containers:
                    response += f"- {container['Contenedor']}: {container['Estado']} ({container['Status']})\n"
                return response
            else:
                return "No se encontraron contenedores en ejecución."
            
        elif function_name == "ver_logs":
            contenedor = arguments.get("contenedor")
            num_lineas = arguments.get("num_lineas", 50)
            
            logs = subprocess.run(
                ["docker", "logs", contenedor, f"--tail={num_lineas}"],
                capture_output=True,
                text=True
            )
            
            if logs.returncode == 0:
                return f"Logs de {contenedor} (últimas {num_lineas} líneas):\n\n{logs.stdout}"
            else:
                return f"Error al obtener logs de {contenedor}: {logs.stderr}"
            
        elif function_name == "generar_informe":
            report_path, report_content = generate_system_report()
            return f"Informe generado en {report_path}:\n\n{report_content}"
            
        elif function_name == "leer_documento":
            ruta_archivo = arguments.get("ruta_archivo")
            content = read_log_file(ruta_archivo)
            return f"Contenido de {ruta_archivo}:\n\n{content}"
    # Analizar el mensaje para detectar comandos
    command_prefixes = {
        "lanzar": "lanzar_sistema",
        "iniciar": "lanzar_sistema",
        "arrancar": "lanzar_sistema",
        "detener": "detener_sistema",
        "parar": "detener_sistema",
        "apagar": "detener_sistema",
        "reiniciar": "reiniciar_sistema",
        "estado": "verificar_estado",
        "status": "verificar_estado",
        "logs": "ver_logs",
        "informe": "generar_informe",
        "reporte": "generar_informe",
        "leer": "leer_documento"
