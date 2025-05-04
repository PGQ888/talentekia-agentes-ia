#!/bin/bash
# Script de acceso directo para TalentekSystemUnified

# Ruta al directorio TalentekSystemUnified
TALENTEK_DIR="$HOME/TalentekSystem/talentekia-agentes-ia/TalentekSystemUnified"

# Verificar si el directorio existe
if [ -d "$TALENTEK_DIR" ]; then
    echo "Iniciando TalentekSystemUnified..."
    cd "$TALENTEK_DIR"
    ./start_talentek.sh
else
    echo "Error: No se encontró el directorio TalentekSystemUnified en $TALENTEK_DIR"
    echo "Por favor, especifica la ruta correcta en este script."
    exit 1
fi