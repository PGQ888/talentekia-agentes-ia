#!/bin/bash
# Script de inicio para TalentekIA en Mac con chip M2
# Este script detecta automáticamente el entorno y ejecuta la aplicación

# Colores para mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════╗"
echo "║                                                    ║"
echo "║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗      ║"
echo "║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║      ║"
echo "║      ██║   ███████║██║     █████╗  ██╔██╗ ██║      ║"
echo "║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║      ║"
echo "║      ██║   ██║  ██║███████╗███████╗██║ ╚████║      ║"
echo "║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝      ║"
echo "║                                                    ║"
echo "║                  TalentekIA                        ║"
echo "║                                                    ║"
echo "║          Optimizado para Apple Silicon             ║"
echo "║                                                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Detectar qué versión de Python está disponible
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}No se pudo encontrar Python. Por favor instala Python 3.${NC}"
    exit 1
fi

echo -e "Usando ${GREEN}$PYTHON_CMD${NC}"
echo "Iniciando TalentekIA optimizado para Mac M2..."

# Ejecutar el script principal
$PYTHON_CMD run_talentek_m2.py

exit $?