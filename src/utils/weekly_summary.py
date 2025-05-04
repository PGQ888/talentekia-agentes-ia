import streamlit as st
import pandas as pd
import os
from datetime import datetime

def generar_resumen_semanal():
    """
    Genera un resumen semanal de los datos recopilados por los agentes
    """
    st.header("📊 Resumen Semanal")
    
    # Verificar si hay datos para mostrar
    docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    
    if os.path.exists(docs_path):
        files = os.listdir(docs_path)
        csv_files = [f for f in files if f.endswith('.csv')]
        
        if csv_files:
            st.success(f"✅ Se encontraron {len(csv_files)} archivos de datos")
            
            # Mostrar resumen de cada archivo
            for csv_file in csv_files:
                file_path = os.path.join(docs_path, csv_file)
                try:
                    df = pd.read_csv(file_path)
                    st.subheader(f"📄 {csv_file}")
                    st.write(f"Registros: {len(df)}")
                    st.write(f"Última actualización: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')}")
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"Error al procesar {csv_file}: {str(e)}")
        else:
            st.warning("⚠️ No se encontraron archivos CSV en la carpeta docs.")
    else:
        st.error("⚠️ No se encontró la carpeta docs.")
    
    # Agregar información adicional
    st.subheader("📈 Estadísticas del Sistema")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Agentes Activos", "5")
        st.metric("Documentos Procesados", "10")
    
    with col2:
        st.metric("Tiempo de Ejecución", "2 horas")
        st.metric("Eficiencia", "95%")

if __name__ == "__main__":
    generar_resumen_semanal()