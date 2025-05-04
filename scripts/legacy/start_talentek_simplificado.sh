#!/bin/bash
# Script de inicio simplificado para TalentekIA en Mac con chip M2
# Este script resuelve todos los problemas de compatibilidad encontrados

echo "===== TalentekIA para Mac M2 - Inicio simplificado ====="

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Verificar que Python 3 esté instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Verificar que pip esté instalado
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Verificar que el archivo .env exista en src/
if [ ! -f "./src/.env" ]; then
    echo "Creando enlace simbólico para .env en src/..."
    # Asegurarse de que el directorio existe
    mkdir -p "./src"
    
    if [ -f "./.env" ]; then
        # Copiar el .env existente
        cp ./.env ./src/.env
        echo "Archivo .env copiado a src/.env"
    else
        # Crear un .env básico
        cat > ./src/.env << EOL
# Variables de entorno para TalentekIA
# Optimizado para Mac M2

# API Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
HUGGINGFACE_API_KEY=

# Optimizaciones Mac M2
PYTORCH_ENABLE_MPS_FALLBACK=1
TF_ENABLE_ONEDNN_OPTS=0
PYTORCH_DEVICE=mps
OMP_NUM_THREADS=8
MKL_NUM_THREADS=8
EOL
        echo "Archivo .env básico creado en src/"
    fi
fi

# Verificar dependencias críticas
echo "Verificando dependencias críticas..."
DEPS=(streamlit dotenv torch numpy pandas)
MISSING=()

for DEP in "${DEPS[@]}"; do
    if ! python3 -c "import $DEP" &> /dev/null; then
        MISSING+=("$DEP")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Instalando dependencias faltantes: ${MISSING[*]}"
    pip3 install "${MISSING[@]}"
fi

# Establecer variables de entorno para Python 3.12 y asyncio
export PYTHONWARNINGS=ignore::RuntimeWarning

# Establecer variables de entorno para optimizaciones M2
export PYTORCH_ENABLE_MPS_FALLBACK=1
export TF_ENABLE_ONEDNN_OPTS=0

echo "Iniciando TalentekIA..."

# Ejecutar la aplicación sin mensajes de error de asyncio
python3 -W ignore::RuntimeWarning -m streamlit run src/interface/streamlit_app.py

exit $?