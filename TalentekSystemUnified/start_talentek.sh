#!/bin/bash
# Script de inicio para TalentekSystem Unified
# Optimizado para Mac con chip M2

# Colores para la salida
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═════════════════════════════════════════════════════════╗"
echo "║                                                         ║"
echo "║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗████████╗  ║"
echo "║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║╚══██╔══╝  ║"
echo "║      ██║   ███████║██║     █████╗  ██╔██╗ ██║   ██║     ║"
echo "║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║   ██║     ║"
echo "║      ██║   ██║  ██║███████╗███████╗██║ ╚████║   ██║     ║"
echo "║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝     ║"
echo "║                                                         ║"
echo "║                 SISTEMA UNIFICADO                       ║"
echo "║                                                         ║"
echo "║             Optimizado para Apple Silicon               ║"
echo "║                                                         ║"
echo "╚═════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Directorio base del sistema
BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASEDIR"

# Verificar si estamos en un Mac con Apple Silicon
if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    echo -e "${GREEN}✅ Detectado Mac con Apple Silicon${NC}"
else
    echo -e "${YELLOW}⚠️ Este sistema está optimizado para Mac con Apple Silicon${NC}"
fi

# Verificar si existe un entorno virtual
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Entorno virtual encontrado${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️ Creando entorno virtual...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    
    echo -e "${BLUE}Instalando dependencias...${NC}"
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
    # Instalar PyTorch optimizado para M1/M2 si estamos en Apple Silicon
    if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
        echo -e "${BLUE}Instalando PyTorch optimizado para Apple Silicon...${NC}"
        pip3 install torch torchvision torchaudio
    fi
    
    echo -e "${GREEN}✅ Entorno virtual configurado${NC}"
fi

# Verificar archivos de configuración
if [ -f "config/talentek_agentes_config.toml" ]; then
    echo -e "${GREEN}✅ Archivo de configuración encontrado${NC}"
else
    echo -e "${RED}❌ Archivo de configuración no encontrado${NC}"
    exit 1
fi

# Crear directorios necesarios
mkdir -p logs data/temp data/finanzas data/informes data/plantillas data/propuestas

# Menú de opciones
echo ""
echo -e "${BLUE}=== MENÚ DE OPCIONES ===${NC}"
echo "1. Ejecutar todos los agentes (paralelo)"
echo "2. Ejecutar todos los agentes (secuencial)"
echo "3. Listar agentes disponibles"
echo "4. Ejecutar un agente específico"
echo "5. Salir"
echo ""
read -p "Seleccione una opción (1-5): " option

case $option in
    1)
        echo -e "${BLUE}Ejecutando todos los agentes en paralelo...${NC}"
        python3 launch_talentek_system.py
        ;;
    2)
        echo -e "${BLUE}Ejecutando todos los agentes secuencialmente...${NC}"
        python3 launch_talentek_system.py --sequential
        ;;
    3)
        echo -e "${BLUE}Listando agentes disponibles...${NC}"
        python3 launch_talentek_system.py --list
        ;;
    4)
        echo -e "${BLUE}Agentes disponibles:${NC}"
        python3 launch_talentek_system.py --list
        echo ""
        read -p "Ingrese el ID del agente a ejecutar: " agent_id
        echo -e "${BLUE}Ejecutando agente $agent_id...${NC}"
        python3 launch_talentek_system.py --agent $agent_id
        ;;
    5)
        echo -e "${BLUE}Saliendo...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Opción inválida${NC}"
        exit 1
        ;;
esac

# Desactivar entorno virtual al finalizar
deactivate

echo -e "${GREEN}Proceso completado${NC}"