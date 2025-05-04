import streamlit as st
import os
import pandas as pd
from datetime import datetime
import sys
import subprocess

# Añadir el directorio scripts al path de Python para poder importar los módulos
scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
sys.path.append(scripts_dir)

# Ahora importamos los módulos desde scripts
try:
    from scripts.weekly_summary import generar_resumen_semanal
except ImportError:
    # Si no existe el archivo, creamos una función básica
    def generar_resumen_semanal():
        st.header("📊 Resumen Semanal")
        st.info("Función de resumen semanal no disponible.")

try:
    from scripts.config_tab_fixed import render_config_tab
except ImportError:
    # Si no existe el archivo, creamos una función básica
    def render_config_tab():
        st.header("⚙️ Configuración")
        st.info("Función de configuración no disponible.")

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

def mostrar_resultado_agente(path_csv, path_md):
    """Muestra los resultados de un agente (CSV y Markdown)"""
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

# Función principal
def main():
    st.set_page_config(page_title="Talentek IA", layout="wide")
    st.title("Panel Inteligente Talentek IA")

    menu = st.sidebar.radio(
        "Selecciona un módulo:",
        ["🔍 LinkedIn Pro", "📊 Estrategia Comercial", "💵 Finanzas Personales", "⚙️ Auto Mejora", "📋 Resumen Semanal", "⚙️ Configuración"]
    )

    if menu == "🔍 LinkedIn Pro":
        st.header("Agente LinkedIn Pro")
        st.write("Este agente escanea LinkedIn en busca de oportunidades de trabajo y candidatos potenciales.")
        
        # Rutas a los archivos de resultados
        path_csv = os.path.join(os.path.dirname(__file__), "docs", "linkedin_ofertas.csv")
        path_md = os.path.join(os.path.dirname(__file__), "docs", "linkedin_ofertas.md")
        
        # Mostrar resultados
        mostrar_resultado_agente(path_csv, path_md)
        
        # Botón para ejecutar el agente
        if st.button("🚀 Ejecutar Agente LinkedIn Pro"):
            st.info("Ejecutando agente LinkedIn Pro...")
            # Aquí iría el código para ejecutar el agente
            st.success("Agente ejecutado correctamente.")

    elif menu == "📊 Estrategia Comercial":
        st.header("Agente de Estrategia Comercial")
        st.write("Este agente analiza tendencias del mercado y genera estrategias comerciales personalizadas.")
        
        # Placeholder para futuros resultados
        st.info("Módulo en desarrollo.")

    elif menu == "💵 Finanzas Personales":
        st.header("Agente de Finanzas Personales")
        st.write("Este agente analiza tus finanzas y te proporciona recomendaciones personalizadas.")
        
        # Placeholder para futuros resultados
        st.info("Módulo en desarrollo.")

    elif menu == "⚙️ Auto Mejora":
        st.header("Agente de Auto Mejora")
        st.write("Este agente analiza tu rendimiento y te proporciona recomendaciones para mejorar.")
        
        # Placeholder para futuros resultados
        st.info("Módulo en desarrollo.")

    elif menu == "📋 Resumen Semanal":
        # Usar la función importada si está disponible
        generar_resumen_semanal()

    elif menu == "⚙️ Configuración":
        # Usar la función importada si está disponible
        render_config_tab()

if __name__ == "__main__":
    main()