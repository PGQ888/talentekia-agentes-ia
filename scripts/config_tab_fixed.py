import streamlit as st
import json
import os
from pathlib import Path

def get_config():
    """Carga la configuración desde el archivo o crea uno por defecto"""
    config_path = Path(os.path.dirname(os.path.dirname(__file__))) / "config" / "settings.json"
    
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error al cargar configuración: {str(e)}")
            return create_default_config(config_path)
    else:
        return create_default_config(config_path)

def create_default_config(config_path):
    """Crea una configuración por defecto"""
    default_config = {
        "api_keys": {
            "openai": "",
            "linkedin": "",
            "github": ""
        },
        "update_frequency": {
            "resumen_semanal": "Sunday 08:00",
            "linkedin_scraping": "Daily 09:00",
            "auto_improve": "Monday 07:00"
        },
        "performance_mode": "balanced"
    }
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Guardar configuración por defecto
    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=2)
    
    return default_config

def save_config(config):
    """Guarda la configuración en el archivo"""
    config_path = Path(os.path.dirname(os.path.dirname(__file__))) / "config" / "settings.json"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error al guardar configuración: {str(e)}")
        return False

def render_config_tab():
    """Renderiza la pestaña de configuración"""
    st.header("⚙️ Configuración del Sistema")
    
    # Cargar configuración actual
    config = get_config()
    
    # Crear pestañas para organizar la configuración
    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "⏱️ Programación", "🛠️ Rendimiento"])
    
    with tab1:
        st.subheader("🔑 Claves de API")
        
        # OpenAI API Key
        openai_key = st.text_input(
            "OpenAI API Key", 
            value=config["api_keys"]["openai"],
            type="password"
        )
        
        # LinkedIn API Key
        linkedin_key = st.text_input(
            "LinkedIn API Key", 
            value=config["api_keys"]["linkedin"],
            type="password"
        )
        
        # GitHub API Key
        github_key = st.text_input(
            "GitHub API Key", 
            value=config["api_keys"]["github"],
            type="password"
        )
        
        # Actualizar valores en el diccionario de configuración
        config["api_keys"]["openai"] = openai_key
        config["api_keys"]["linkedin"] = linkedin_key
        config["api_keys"]["github"] = github_key
    
    with tab2:
        st.subheader("⏱️ Programación de Tareas")
        st.write("Configura cuándo se ejecutarán automáticamente los agentes.")
        
        # Resumen semanal
        resumen_freq = st.text_input(
            "Resumen Semanal (formato: Day HH:MM)", 
            value=config["update_frequency"]["resumen_semanal"]
        )
        
        # LinkedIn scraping
        linkedin_freq = st.text_input(
            "LinkedIn Scraping (formato: Daily HH:MM o Day HH:MM)", 
            value=config["update_frequency"]["linkedin_scraping"]
        )
        
        # Auto-mejora
        auto_improve_freq = st.text_input(
            "Auto-Mejora (formato: Day HH:MM)", 
            value=config["update_frequency"]["auto_improve"]
        )
        
        # Actualizar valores en el diccionario de configuración
        config["update_frequency"]["resumen_semanal"] = resumen_freq
        config["update_frequency"]["linkedin_scraping"] = linkedin_freq
        config["update_frequency"]["auto_improve"] = auto_improve_freq
    
    with tab3:
        st.subheader("⚡ Modo de Rendimiento")
        
        # Modo de rendimiento (corregido el error de sintaxis)
        performance_mode = st.selectbox(
            "Modo de Rendimiento",
            options=["eco", "balanced", "performance"],
            index=["eco", "balanced", "performance"].index(config["performance_mode"])
        )
        
        # Actualizar valor en el diccionario de configuración
        config["performance_mode"] = performance_mode
    
    # Botón para guardar la configuración
    if st.button("💾 Guardar Configuración"):
        if save_config(config):
            st.success("✅ Configuración guardada correctamente")
        else:
            st.error("❌ Error al guardar la configuración")

if __name__ == "__main__":
    render_config_tab()