#!/bin/bash

# Script para iniciar el servicio de sincronización automática
echo "Iniciando servicio de sincronización automática de TalentekIA..."

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Instalar dependencias necesarias si no están ya instaladas
pip install schedule python-dotenv

# Ejecutar el script de sincronización en segundo plano
echo "Iniciando servicio en segundo plano..."
nohup python scripts/auto_sync.py > auto_sync_output.log 2>&1 &

# Guardar el PID para poder detener el servicio más tarde
echo $! > auto_sync.pid

echo "Servicio iniciado con PID: $(cat auto_sync.pid)"
echo "Logs disponibles en: auto_sync_output.log"
echo "Para detener el servicio, ejecuta: ./stop_auto_sync.sh"