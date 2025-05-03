#!/bin/bash

# Script para detener el servicio de sincronización automática
echo "Deteniendo servicio de sincronización automática de TalentekIA..."

if [ -f "auto_sync.pid" ]; then
    PID=$(cat auto_sync.pid)
    if ps -p $PID > /dev/null; then
        echo "Deteniendo proceso con PID: $PID"
        kill $PID
        rm auto_sync.pid
        echo "Servicio detenido correctamente."
    else
        echo "El proceso con PID $PID ya no está en ejecución."
        rm auto_sync.pid
    fi
else
    echo "No se encontró archivo PID. El servicio podría no estar en ejecución."
fi