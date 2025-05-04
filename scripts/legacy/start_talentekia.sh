#!/bin/bash
# Script de inicio rápido para TalentekIA en Mac M2
# Este script inicia la aplicación con optimizaciones específicas para Mac con chip M2

# Colores para mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║   ████████╗ █████╗ ██╗     ███████╗███╗   ██╗████████╗     ║"
echo "║   ╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║╚══██╔══╝     ║"
echo "║      ██║   ███████║██║     █████╗  ██╔██╗ ██║   ██║        ║"
echo "║      ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║   ██║        ║"
echo "║      ██║   ██║  ██║███████╗███████╗██║ ╚████║   ██║        ║"
echo "║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝        ║"
echo "║                                                            ║"
echo "║                      TalentekIA                            ║"
echo "║                                                            ║"
echo "║           Sistema de Agentes de IA Personalizados          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Obtener el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Verificar que estamos en un Mac M2
if [[ "$(uname)" != "Darwin" ]] || [[ "$(uname -m)" != "arm64" ]]; then
    echo -e "${YELLOW}⚠️  Advertencia: Este script está optimizado para Mac con chip M2 (Apple Silicon).${NC}"
    echo -e "${YELLOW}   Es posible que algunas optimizaciones no funcionen correctamente en tu sistema.${NC}"
    read -p "¿Deseas continuar de todos modos? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo -e "${RED}Operación cancelada.${NC}"
        exit 1
    fi
fi

# Activar entorno virtual si existe
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo -e "${BLUE}Activando entorno virtual...${NC}"
    source "$SCRIPT_DIR/venv/bin/activate"
    echo -e "${GREEN}✓ Entorno virtual activado${NC}"
else
    echo -e "${YELLOW}⚠️  No se encontró un entorno virtual en $SCRIPT_DIR/venv${NC}"
    echo -e "${YELLOW}   Se utilizará el Python del sistema.${NC}"
fi

# Configurar variables de entorno para optimización
export PYTORCH_ENABLE_MPS_FALLBACK=1
export TF_ENABLE_ONEDNN_OPTS=0
export OMP_NUM_THREADS=$(( $(sysctl -n hw.ncpu) - 1 ))
export MKL_NUM_THREADS=$(( $(sysctl -n hw.ncpu) - 1 ))
export TALENTEKIA_PERFORMANCE_MODE=performance

# Crear directorio de logs si no existe
mkdir -p "$SCRIPT_DIR/logs"

# Verificar dependencias críticas
echo -e "${BLUE}Verificando dependencias críticas...${NC}"
python3 -c "import streamlit, pandas, numpy, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error: Faltan dependencias críticas.${NC}"
    echo -e "${YELLOW}Ejecutando inicialización del sistema...${NC}"
    python3 "$SCRIPT_DIR/initialize_system.py"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error en la inicialización. Por favor, revisa los errores e intenta nuevamente.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Dependencias críticas verificadas${NC}"
fi

# Aplicar configuración personal
echo -e "${BLUE}Aplicando configuración personal...${NC}"
python3 -c "from config.personal_settings import apply_personal_settings; apply_personal_settings()" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Configuración personal aplicada${NC}"
else
    echo -e "${YELLOW}⚠️  No se pudo aplicar la configuración personal${NC}"
fi

# Iniciar la aplicación
echo -e "${BLUE}Iniciando TalentekIA...${NC}"
echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}  TalentekIA está iniciando en modo optimizado ${NC}"
echo -e "${GREEN}  para Mac M2 (Apple Silicon)                 ${NC}"
echo -e "${GREEN}==============================================${NC}"

# Ejecutar la aplicación con Streamlit
streamlit run "$SCRIPT_DIR/src/interface/streamlit_app.py" "$@"