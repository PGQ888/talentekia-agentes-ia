#!/bin/bash
# Script para configurar el entorno de desarrollo local en Mac M2

# Colores para salida
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================${NC}"
echo -e "${BLUE}  TalentekIA - Entorno Dev M2   ${NC}"
echo -e "${BLUE}=================================${NC}"

# Verificar si estamos en un Mac con Apple Silicon
if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "arm64" ]; then
    echo -e "${GREEN}✓ Detectado Mac con Apple Silicon (M1/M2/M3)${NC}"
else
    echo -e "${YELLOW}⚠️  Este script está optimizado para Mac con Apple Silicon${NC}"
    echo "¿Deseas continuar de todas formas? (s/n)"
    read -r response
    if [[ ! "$response" =~ ^[sS]$ ]]; then
        echo "Operación cancelada"
        exit 1
    fi
fi

# Configurar variables de entorno para optimización
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
export OMP_NUM_THREADS=4
export VECLIB_MAXIMUM_THREADS=4
export NUMEXPR_NUM_THREADS=4
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_CUDA_ALLOC_CONF="max_split_size_mb:512"

# Verificar si existe un entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python3 -m venv venv
fi

# Activar entorno virtual
echo -e "${YELLOW}Activando entorno virtual...${NC}"
source venv/bin/activate

# Actualizar pip y herramientas
echo -e "${YELLOW}Actualizando pip y herramientas...${NC}"
pip install --upgrade pip setuptools wheel

# Instalar dependencias si es necesario
if [ ! -f ".dev_setup_done" ]; then
    echo -e "${YELLOW}Instalando dependencias...${NC}"
    pip install -r requirements.txt
    pip install -e .
    touch .dev_setup_done
else
    echo -e "${GREEN}✓ Dependencias ya instaladas${NC}"
fi

echo -e "${GREEN}✓ Entorno de desarrollo configurado y optimizado para M2${NC}"
echo -e "${YELLOW}Para activar este entorno en el futuro, ejecuta:${NC}"
echo -e "  ${BLUE}source dev.sh${NC}"

# Mantener el entorno activado para la sesión actual
exec "${SHELL}"