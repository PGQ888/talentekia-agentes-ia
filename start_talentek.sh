#!/bin/bash
# Script de inicio para el sistema TalentekIA unificado

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

# Fecha y hora actual
echo -e "${YELLOW}Fecha y hora: $(date)${NC}"
echo -e "${YELLOW}Sistema: $(uname -s) $(uname -r) ($(uname -m))${NC}"
echo "--------------------------------------------------------"

# Verificar que estamos en el directorio correcto
if [ ! -f "talentek.py" ]; then
    echo -e "${RED}Error: No se encontró el archivo talentek.py${NC}"
    echo "Por favor, ejecute este script desde el directorio raíz del proyecto."
    exit 1
fi

# Verificar Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: No se encontró Python instalado${NC}"
    echo "Por favor, instale Python 3.8 o superior."
    exit 1
fi

echo -e "${GREEN}Usando Python: $($PYTHON_CMD --version)${NC}"

# Verificar entorno virtual
if [ -d "venv" ] || [ -d ".venv" ]; then
    if [ -d "venv" ]; then
        VENV_DIR="venv"
    else
        VENV_DIR=".venv"
    fi
    
    echo -e "${GREEN}Entorno virtual encontrado. Activando...${NC}"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source "$VENV_DIR/Scripts/activate"
    else
        # Unix/Linux/MacOS
        source "$VENV_DIR/bin/activate"
    fi
else
    echo -e "${YELLOW}No se encontró un entorno virtual. Creando uno nuevo...${NC}"
    $PYTHON_CMD -m venv venv
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source "venv/Scripts/activate"
    else
        # Unix/Linux/MacOS
        source "venv/bin/activate"
    fi
    
    echo -e "${GREEN}Instalando dependencias...${NC}"
    pip install -r requirements.txt
fi

# Verificar si es Mac con Apple Silicon
if [[ "$(uname -s)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    echo -e "${BLUE}Detectado Mac con Apple Silicon (M1/M2)${NC}"
    echo "Aplicando optimizaciones para Apple Silicon..."
    export PYTORCH_ENABLE_MPS_FALLBACK=1
    export TF_ENABLE_ONEDNN_OPTS=0
fi

# Crear directorios necesarios
mkdir -p logs data config

# Verificar archivo de configuración
if [ ! -f "config/talentek_config.toml" ]; then
    echo -e "${YELLOW}Advertencia: No se encontró el archivo de configuración${NC}"
    if [ -f "config/talentek_config.toml.example" ]; then
        echo "Copiando archivo de configuración de ejemplo..."
        cp config/talentek_config.toml.example config/talentek_config.toml
    fi
fi

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Advertencia: No se encontró el archivo .env${NC}"
    if [ -f ".env.example" ]; then
        echo "Copiando archivo .env de ejemplo..."
        cp .env.example .env
        echo -e "${YELLOW}Por favor, edite el archivo .env con sus claves API${NC}"
    else
        echo "Creando archivo .env básico..."
        echo "# Configuración de TalentekIA" > .env
        echo "# API Keys" >> .env
        echo "OPENAI_API_KEY=" >> .env
        echo "ANTHROPIC_API_KEY=" >> .env
        echo "HUGGINGFACE_API_KEY=" >> .env
        echo -e "${YELLOW}Por favor, edite el archivo .env con sus claves API${NC}"
    fi
fi

# Mostrar menú de opciones
echo ""
echo -e "${BLUE}=== MENÚ DE TALENTEK IA ===${NC}"
echo "1. Inicializar el sistema"
echo "2. Ejecutar todos los agentes"
echo "3. Ejecutar agente específico"
echo "4. Sincronizar con GitHub"
echo "5. Iniciar interfaz web"
echo "6. Salir"
echo ""

read -p "Seleccione una opción (1-6): " option

case $option in
    1)
        echo -e "${GREEN}Inicializando el sistema...${NC}"
        $PYTHON_CMD talentek.py --init
        ;;
    2)
        echo -e "${GREEN}Ejecutando todos los agentes...${NC}"
        read -p "¿Ejecutar en paralelo? (s/n): " parallel
        if [[ "$parallel" == "s" || "$parallel" == "S" ]]; then
            $PYTHON_CMD talentek.py --run all --parallel
        else
            $PYTHON_CMD talentek.py --run all
        fi
        ;;
    3)
        echo -e "${GREEN}Agentes disponibles:${NC}"
        echo "- linkedin: Agente de LinkedIn"
        echo "- finanzas: Agente de finanzas personales"
        echo "- estrategia: Agente de estrategia comercial"
        echo "- auto_improve: Agente de optimización"
        echo "- email: Agente de email"
        echo "- resumen: Agente de resumen semanal"
        
        read -p "Ingrese el nombre del agente a ejecutar: " agent_name
        $PYTHON_CMD talentek.py --run $agent_name
        ;;
    4)
        echo -e "${GREEN}Sincronizando con GitHub...${NC}"
        $PYTHON_CMD talentek.py --sync
        ;;
    5)
        echo -e "${GREEN}Iniciando interfaz web...${NC}"
        if command -v streamlit &>/dev/null; then
            streamlit run src/interface/streamlit_app.py
        else
            echo -e "${YELLOW}Instalando Streamlit...${NC}"
            pip install streamlit
            streamlit run src/interface/streamlit_app.py
        fi
        ;;
    6)
        echo -e "${GREEN}Saliendo...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Opción no válida${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Operación completada.${NC}"