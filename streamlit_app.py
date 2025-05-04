import streamlit as st
import os
import pandas as pd
from datetime import datetime
import sys
import subprocess
import json

# Añadir los directorios necesarios al path de Python
project_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_dir, "scripts")
agents_dir = os.path.join(project_dir, "agents")
sys.path.append(scripts_dir)
sys.path.append(agents_dir)

# Cargar el entorno
try:
    from scripts.env_loader import env
    USER_NAME = env.get("USER_NAME", "Usuario")
except ImportError:
    USER_NAME = "Usuario"
    st.error("No se pudo cargar el módulo de entorno. Algunas funcionalidades pueden no estar disponibles.")

# Importar módulos de integración
try:
    from scripts.huggingface_integration import hf_manager
    from scripts.github_integration import github_manager
    from scripts.anythingllm_integration import anything_llm_manager
    INTEGRATIONS_AVAILABLE = True
except ImportError:
    INTEGRATIONS_AVAILABLE = False
    st.warning("No se pudieron cargar los módulos de integración. Algunas funcionalidades estarán limitadas.")

# Importar módulos de agentes
try:
    from scripts.weekly_summary import generar_resumen_semanal
    from scripts.config_tab_fixed import render_config_tab, get_config, save_config
    from agents.config import get_agent_config, get_all_agents
except ImportError:
    # Si no existen los archivos, creamos funciones básicas
    def generar_resumen_semanal():
        st.header("📊 Resumen Semanal")
        st.info("Función de resumen semanal no disponible.")
    
    def render_config_tab():
        st.header("⚙️ Configuración")
        st.info("Función de configuración no disponible.")
    
    def get_config():
        return {}
    
    def save_config(config):
        return False
    
    def get_agent_config(agent_id):
        return None
    
    def get_all_agents():
        return {}

# Funciones auxiliares
def leer_markdown(path):
    """Lee un archivo markdown y devuelve su contenido"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error al leer archivo: {str(e)}"

def leer_csv(path):
    """Lee un archivo CSV y devuelve un DataFrame"""
    try:
        return pd.read_csv(path)
    except Exception as e:
        return None

def ejecutar_comando(comando):
    """Ejecuta un comando del sistema y devuelve el resultado"""
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        return resultado.returncode == 0, resultado.stdout
    except Exception as e:
        return False, str(e)

def ejecutar_agente(agent_id):
    """Ejecuta un agente específico"""
    agent_config = get_agent_config(agent_id)
    if not agent_config:
        return False, "Configuración del agente no encontrada"
    
    agent_script = os.path.join(agents_dir, f"{agent_id}_pro.py")
    if not os.path.exists(agent_script):
        agent_script = os.path.join(agents_dir, f"{agent_id}_agent.py")
    
    if os.path.exists(agent_script):
        return ejecutar_comando(f"python {agent_script}")
    else:
        return False, f"Script del agente no encontrado: {agent_script}"

def mostrar_resultado_agente(agent_id):
    """Muestra los resultados de un agente"""
    agent_config = get_agent_config(agent_id)
    if not agent_config:
        st.warning(f"No se encontró configuración para el agente {agent_id}")
        return
    
    output_files = agent_config.get("output_files", {})
    path_csv = os.path.join(project_dir, "docs", output_files.get("csv", f"{agent_id}.csv"))
    path_md = os.path.join(project_dir, "docs", output_files.get("markdown", f"{agent_id}.md"))
    
    # Verificar y mostrar CSV
    if os.path.exists(path_csv):
        st.subheader("📄 Resultados CSV")
        df = leer_csv(path_csv)
        if df is not None:
            st.dataframe(df)
            with open(path_csv, "r", encoding="utf-8") as f:
                st.download_button("📥 Descargar CSV", f, file_name=os.path.basename(path_csv))
            st.success(f"✅ Datos reales encontrados: {len(df)} registros")
    else:
        st.warning("⚠️ No se ha generado ningún CSV.")
    
    # Verificar y mostrar Markdown
    if os.path.exists(path_md):
        st.subheader("🗒️ Resumen en Markdown")
        st.markdown(leer_markdown(path_md))
    else:
        st.warning("⚠️ No se ha generado ningún informe en Markdown.")

def mostrar_panel_integraciones():
    """Muestra el panel de estado de integraciones"""
    st.sidebar.subheader("Estado de Integraciones")
    
    if INTEGRATIONS_AVAILABLE:
        # Verificar estado de Hugging Face
        hf_status = "✅ Conectado" if hf_manager.token else "❌ No configurado"
        st.sidebar.text(f"🤗 Hugging Face: {hf_status}")
        
        # Verificar estado de GitHub
        gh_status = "✅ Conectado" if github_manager.token else "❌ No configurado"
        st.sidebar.text(f"📦 GitHub: {gh_status}")
        
        # Verificar estado de AnythingLLM
        allm_status = "✅ Conectado" if anything_llm_manager.api_key else "❌ No configurado"
        st.sidebar.text(f"🧠 AnythingLLM: {allm_status}")
    else:
        st.sidebar.warning("Integraciones no disponibles")

def verificar_estado_sincronizacion():
    """Verifica si el servicio de sincronización automática está activo"""
    try:
        result = subprocess.run("ps aux | grep '[a]uto_sync.py'", shell=True, capture_output=True, text=True)
        return result.stdout.strip() != ""
    except:
        return False

# Función principal
def main():
    st.set_page_config(page_title="Talentek IA", layout="wide")
    
    # Barra lateral
    st.sidebar.title(f"Talentek IA")
    st.sidebar.text(f"Bienvenido, {USER_NAME}")
    
    # Mostrar estado de integraciones
    mostrar_panel_integraciones()
    
    # Mostrar estado de sincronización
    sync_status = "✅ Activo" if verificar_estado_sincronizacion() else "❌ Inactivo"
    st.sidebar.text(f"🔄 Sincronización: {sync_status}")
    
    # Menú principal
    agents = get_all_agents()
    menu_items = []
    
    for agent_id, agent_data in agents.items():
        menu_items.append(f"{agent_data.get('icon', '📋')} {agent_data.get('name', agent_id.capitalize())}")
    
    menu_items.append("📊 Resumen Semanal")
    menu_items.append("⚙️ Configuración")
    
    menu = st.sidebar.radio("Selecciona un módulo:", menu_items)
    
    # Título principal
    st.title("Panel Inteligente Talentek IA")
    
    # Mostrar contenido según la selección
    if menu == "⚙️ Configuración":
        render_config_tab()
    elif menu == "📊 Resumen Semanal":
        generar_resumen_semanal()
    else:
        # Encontrar el ID del agente seleccionado
        selected_agent_id = None
        for agent_id, agent_data in agents.items():
            menu_item = f"{agent_data.get('icon', '📋')} {agent_data.get('name', agent_id.capitalize())}"
            if menu == menu_item:
                selected_agent_id = agent_id
                break
        
        if selected_agent_id:
            agent_data = agents[selected_agent_id]
            
            # Mostrar encabezado del agente
            st.header(f"{agent_data.get('icon', '📋')} {agent_data.get('name', selected_agent_id.capitalize())}")
            st.write(agent_data.get("description", ""))
            
            # Columnas para información y acciones
            col1, col2 = st.columns([3, 1])
            
            with col2:
                st.subheader("Acciones")
                if st.button(f"🚀 Ejecutar {agent_data.get('name', 'Agente')}"):
                    with st.spinner(f"Ejecutando {agent_data.get('name', 'agente')}..."):
                        success, output = ejecutar_agente(selected_agent_id)
                        if success:
                            st.success("✅ Agente ejecutado correctamente")
                        else:
                            st.error(f"❌ Error al ejecutar el agente: {output}")
                
                st.text(f"Actualización: {agent_data.get('update_frequency', 'Manual')}")
                
                # Si tenemos integración con AnythingLLM, mostrar botón para procesar documentos
                if INTEGRATIONS_AVAILABLE and anything_llm_manager.api_key:
                    if st.button("🧠 Procesar con AnythingLLM"):
                        with st.spinner("Procesando documentos con AnythingLLM..."):
                            docs_dir = os.path.join(project_dir, "docs")
                            success = anything_llm_manager.process_documents_for_agent(
                                agent_data.get('name', selected_agent_id),
                                docs_dir
                            )
                            if success:
                                st.success("✅ Documentos procesados correctamente")
                            else:
                                st.error("❌ Error al procesar documentos")
            
            with col1:
                # Mostrar resultados del agente
                mostrar_resultado_agente(selected_agent_id)
                
                # Si es el agente de Auto Mejora y tenemos integración con Hugging Face, mostrar panel de análisis de código
                if selected_agent_id == "automejora" and INTEGRATIONS_AVAILABLE and hf_manager.token:
                    st.subheader("🔍 Análisis de Código")
                    code_file = st.text_input("Ruta al archivo de código para analizar:")
                    if code_file and os.path.exists(code_file):
                        with open(code_file, "r") as f:
                            code = f.read()
                        
                        if st.button("Analizar Código"):
                            with st.spinner("Analizando código con Hugging Face..."):
                                analysis = hf_manager.analyze_code(code)
                                st.code(analysis)
                    
                    st.subheader("🛠️ Mejora de Código")
                    code_to_improve = st.text_area("Código a mejorar:", height=200)
                    instructions = st.text_input("Instrucciones de mejora:", "Optimizar para rendimiento en Mac M2")
                    
                    if code_to_improve and st.button("Mejorar Código"):
                        with st.spinner("Mejorando código con Hugging Face..."):
                            improved_code = hf_manager.code_improvement(code_to_improve, instructions)
                            st.code(improved_code)
        
        # Si no se encontró el agente seleccionado
        else:
            st.warning("Módulo no encontrado o en desarrollo.")

if __name__ == "__main__":
    main()