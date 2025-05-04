"""
Aplicación principal de TalentekIA
Interfaz de usuario para gestionar y ejecutar agentes de IA
"""

import os
import sys
import streamlit as st
import pandas as pd
import platform
from datetime import datetime
from pathlib import Path
import json

# Añadir el directorio raíz al path para importaciones
sys.path.append(str(Path(__file__).parent.parent.parent))

# Aplicar parche para asyncio (Python 3.12 y Streamlit)
from src.utils.async_helper import streamlit_asyncio_patch
streamlit_asyncio_patch()

# Importar módulos del proyecto
from src.utils.env_loader import EnvLoader
from src.agents.agent_manager import AgentManager

# Configuración específica para Mac M2
def configure_for_mac_m2():
    """Configura el entorno para optimizar el rendimiento en Mac M2"""
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
        st.sidebar.success("✅ Optimizaciones para Mac M2 aplicadas")

# Configuración de la página
st.set_page_config(
    page_title="TalentekIA - Plataforma de Agentes IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4a86e8;
        margin-bottom: 1rem;
    }
    .agent-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f9f9f9;
        margin-bottom: 1rem;
        border-left: 5px solid #4a86e8;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Función para leer archivos markdown
def leer_markdown(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

# Función para leer archivos CSV
def leer_csv(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Error al leer el archivo CSV: {str(e)}")
        return None

# Inicializar el gestor de agentes
@st.cache_resource
def get_agent_manager():
    """Inicializa y retorna el gestor de agentes"""
    return AgentManager()

# Aplicar configuración M2
configure_for_mac_m2()

def get_agent_status(agent_id):
    """
    Obtiene el estado de un agente de manera segura
    
    Args:
        agent_id (str): ID del agente
        
    Returns:
        dict: Estado del agente o un estado por defecto si hay error
    """
    manager = get_agent_manager()
    try:
        status = manager.get_agent_status(agent_id)
        # Asegurar que la clave 'status' existe
        if 'status' not in status:
            status['status'] = 'unknown'
        return status
    except Exception as e:
        st.error(f"Error al obtener el estado del agente {agent_id}: {str(e)}")
        return {
            "id": agent_id,
            "name": agent_id.capitalize(),
            "is_running": False,
            "status": "error"
        }

# Función para mostrar resultados de un agente
def mostrar_resultado_agente(agent_id):
    st.subheader(f"Resultados del Agente: {agent_id}")
    
    # Obtener historial de ejecuciones
    manager = get_agent_manager()
    history = manager.get_execution_history(agent_id, limit=5)
    
    if not history:
        st.info("No hay ejecuciones registradas para este agente.")
        return
    
    # Mostrar la última ejecución
    last_execution = history[0]
    st.write(f"Última ejecución: {last_execution['timestamp']}")
    st.write(f"Estado: {'✅ Exitoso' if last_execution['success'] else '❌ Fallido'}")
    st.write(f"Duración: {last_execution['duration']:.2f} segundos")
    
    # Buscar archivos de resultados
    data_dir = os.path.join(Path(__file__).parent.parent.parent, "data", "output", agent_id)
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')] if os.path.exists(data_dir) else []
    md_files = [f for f in os.listdir(data_dir) if f.endswith('.md')] if os.path.exists(data_dir) else []
    
    # Mostrar datos tabulares si existen
    if csv_files:
        with st.expander("Ver datos tabulares", expanded=True):
            selected_csv = st.selectbox("Seleccionar archivo de datos:", csv_files)
            df = leer_csv(os.path.join(data_dir, selected_csv))
            if df is not None:
                st.dataframe(df)
    
    # Mostrar informes si existen
    if md_files:
        with st.expander("Ver informe", expanded=True):
            selected_md = st.selectbox("Seleccionar informe:", md_files)
            md_content = leer_markdown(os.path.join(data_dir, selected_md))
            st.markdown(md_content)

# Función para renderizar la pestaña de configuración
def render_config_tab():
    st.header("Configuración del Sistema")
    
    # Cargar configuración actual
    config_path = os.path.join(Path(__file__).parent.parent.parent, "config", "settings.json")
    
    if not os.path.exists(config_path):
        # Crear configuración por defecto
        default_config = {
            "api_keys": {
                "openai": "",
                "anthropic": "",
                "huggingface": ""
            },
            "performance_mode": "balanced",
            "update_frequency": {
                "linkedin_agent": "daily",
                "estrategia_comercial": "weekly",
                "finanzas_personales": "monthly"
            },
            "notifications": {
                "email": "",
                "enable_email": False,
                "enable_desktop": True
            }
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
    
    # Cargar configuración
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # API Keys
    st.subheader("API Keys")
    api_keys = config.get("api_keys", {})
    
    col1, col2 = st.columns(2)
    with col1:
        openai_key = st.text_input("OpenAI API Key", value=api_keys.get("openai", ""), type="password")
    with col2:
        anthropic_key = st.text_input("Anthropic API Key", value=api_keys.get("anthropic", ""), type="password")
    
    huggingface_key = st.text_input("HuggingFace API Key", value=api_keys.get("huggingface", ""), type="password")
    
    # Modo de rendimiento
    st.subheader("Rendimiento")
    performance_mode = st.selectbox(
        "Modo de rendimiento",
        options=["eco", "balanced", "performance"],
        index=["eco", "balanced", "performance"].index(config.get("performance_mode", "balanced"))
    )
    
    # Frecuencia de actualización
    st.subheader("Frecuencia de actualización")
    update_freq = config.get("update_frequency", {})
    
    col1, col2 = st.columns(2)
    with col1:
        linkedin_freq = st.selectbox(
            "LinkedIn Agent",
            options=["hourly", "daily", "weekly", "monthly"],
            index=["hourly", "daily", "weekly", "monthly"].index(update_freq.get("linkedin_agent", "daily"))
        )
    with col2:
        estrategia_freq = st.selectbox(
            "Estrategia Comercial",
            options=["daily", "weekly", "monthly"],
            index=["daily", "weekly", "monthly"].index(update_freq.get("estrategia_comercial", "weekly"))
        )
    
    finanzas_freq = st.selectbox(
        "Finanzas Personales",
        options=["weekly", "monthly", "quarterly"],
        index=["weekly", "monthly", "quarterly"].index(update_freq.get("finanzas_personales", "monthly"))
    )
    
    # Notificaciones
    st.subheader("Notificaciones")
    notifications = config.get("notifications", {})
    
    email = st.text_input("Email para notificaciones", value=notifications.get("email", ""))
    col1, col2 = st.columns(2)
    with col1:
        enable_email = st.checkbox("Habilitar notificaciones por email", value=notifications.get("enable_email", False))
    with col2:
        enable_desktop = st.checkbox("Habilitar notificaciones de escritorio", value=notifications.get("enable_desktop", True))
    
    # Guardar configuración
    if st.button("Guardar configuración"):
        # Actualizar configuración
        config["api_keys"] = {
            "openai": openai_key,
            "anthropic": anthropic_key,
            "huggingface": huggingface_key
        }
        config["performance_mode"] = performance_mode
        config["update_frequency"] = {
            "linkedin_agent": linkedin_freq,
            "estrategia_comercial": estrategia_freq,
            "finanzas_personales": finanzas_freq
        }
        config["notifications"] = {
            "email": email,
            "enable_email": enable_email,
            "enable_desktop": enable_desktop
        }
        
        # Guardar en archivo
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        st.success("Configuración guardada correctamente")

def main():
    # Sidebar
    st.sidebar.markdown("<h1 class='main-header'>🧠 TalentekIA</h1>", unsafe_allow_html=True)
    
    # Menú principal
    menu = st.sidebar.radio(
        "Navegación",
        ["Dashboard", "Agentes", "Resultados", "Configuración", "Documentación"]
    )
    
    # Mostrar página según selección
    if menu == "Dashboard":
        st.markdown("<h1 class='main-header'>Dashboard de TalentekIA</h1>", unsafe_allow_html=True)
        
        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Agentes Activos", value=len(get_agent_manager().get_available_agents()))
        with col2:
            st.metric(label="Última Ejecución", value=datetime.now().strftime("%d/%m/%Y %H:%M"))
        with col3:
            st.metric(label="Estado del Sistema", value="Operativo")
        
        # Estado de los agentes
        st.subheader("Estado de los Agentes")
        agents = get_agent_manager().get_available_agents()
        for agent_id in agents:
            status = get_agent_status(agent_id)
            with st.container():
                st.markdown(f"""
                <div class="agent-card">
                    <h3>{agent_id}</h3>
                    <p>Estado: {status['status']}</p>
                    <p>Última ejecución: {status.get('last_run', 'Nunca')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif menu == "Agentes":
        st.markdown("<h1 class='main-header'>Gestión de Agentes</h1>", unsafe_allow_html=True)
        
        # Lista de agentes disponibles
        agents = get_agent_manager().get_available_agents()
        
        for agent_id in agents:
            st.subheader(agent_id)
            status = get_agent_status(agent_id)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"Estado: {status['status']}")
                st.write(f"Última ejecución: {status.get('last_run', 'Nunca')}")
            with col2:
                if st.button(f"Ejecutar {agent_id}", key=f"run_{agent_id}"):
                    with st.spinner(f"Ejecutando {agent_id}..."):
                        success = get_agent_manager().run_agent(agent_id)
                        if success:
                            st.success(f"Agente {agent_id} ejecutado correctamente")
                        else:
                            st.error(f"Error al ejecutar el agente {agent_id}")
            
            st.markdown("---")
    
    elif menu == "Resultados":
        st.markdown("<h1 class='main-header'>Resultados de los Agentes</h1>", unsafe_allow_html=True)
        
        # Selector de agente
        agents = get_agent_manager().get_available_agents()
        selected_agent = st.selectbox("Seleccionar agente", agents)
        
        # Mostrar resultados del agente seleccionado
        if selected_agent:
            mostrar_resultado_agente(selected_agent)
    
    elif menu == "Configuración":
        render_config_tab()
    
    elif menu == "Documentación":
        st.markdown("<h1 class='main-header'>Documentación</h1>", unsafe_allow_html=True)
        
        # Lista de documentos disponibles
        docs_dir = os.path.join(Path(__file__).parent.parent.parent, "docs")
        docs_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
        
        selected_doc = st.selectbox("Seleccionar documento", docs_files)
        
        if selected_doc:
            doc_content = leer_markdown(os.path.join(docs_dir, selected_doc))
            st.markdown(doc_content)

if __name__ == "__main__":
    main()