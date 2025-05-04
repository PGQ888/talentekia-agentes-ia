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
