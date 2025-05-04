#!/bin/bash
# Script para detener la sincronización automática de agentes
# Este script detiene el proceso de sincronización que se ejecuta en segundo plano

echo "Deteniendo sincronización automática de agentes de TalentekIA..."

# Obtener el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Verificar que exista el archivo PID
if [ ! -f "$SCRIPT_DIR/auto_sync.pid" ]; then
    echo "Error: No se encontró el archivo de PID. El proceso no parece estar en ejecución."
    exit 1
fi

# Leer el PID del proceso
PID=$(cat "$SCRIPT_DIR/auto_sync.pid")

# Verificar que el proceso exista
if ! ps -p $PID > /dev/null; then
    echo "Advertencia: El proceso con PID $PID no está en ejecución."
    rm "$SCRIPT_DIR/auto_sync.pid"
    exit 0
fi

# Detener el proceso
echo "Deteniendo proceso con PID $PID..."
kill $PID

# Verificar que el proceso se haya detenido
sleep 2
if ps -p $PID > /dev/null; then
    echo "El proceso no respondió a la señal TERM. Forzando cierre..."
    kill -9 $PID
    sleep 1
fi

# Eliminar el archivo PID
rm "$SCRIPT_DIR/auto_sync.pid"

echo "Proceso de sincronización detenido correctamente."