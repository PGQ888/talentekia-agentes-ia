#!/bin/bash
# Script para iniciar la sincronización automática de agentes
# Este script inicia el proceso de sincronización en segundo plano

echo "Iniciando sincronización automática de agentes de TalentekIA..."

# Obtener el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activar entorno virtual si existe
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "Entorno virtual activado"
else
    echo "Advertencia: No se encontró entorno virtual en $SCRIPT_DIR/venv"
fi

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado o no está en el PATH"
    exit 1
fi

# Iniciar el proceso de sincronización en segundo plano
nohup python3 -u "$SCRIPT_DIR/src/utils/auto_sync.py" > "$SCRIPT_DIR/logs/auto_sync.log" 2>&1 &

# Guardar el PID del proceso
echo $! > "$SCRIPT_DIR/auto_sync.pid"

echo "Proceso de sincronización iniciado con PID $(cat "$SCRIPT_DIR/auto_sync.pid")"
echo "Los logs se guardan en $SCRIPT_DIR/logs/auto_sync.log"
echo "Para detener la sincronización, ejecuta: ./stop_auto_sync.sh"