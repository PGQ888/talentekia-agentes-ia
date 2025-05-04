#!/bin/bash
# Script de despliegue para TalentekAI Unified
# Autor: Pablo Giráldez
# Fecha: 2025-05-04

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    DESPLIEGUE DE TALENTEKAI UNIFIED    ${NC}"
echo -e "${BLUE}========================================${NC}"

# Verificar requisitos previos
echo -e "\n${YELLOW}Verificando requisitos previos...${NC}"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker no está instalado. Por favor, instala Docker antes de continuar.${NC}"
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose no está instalado. Por favor, instala Docker Compose antes de continuar.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker y Docker Compose están instalados.${NC}"

# Verificar archivo .env
if [ ! -f "./config/.env" ]; then
    echo -e "${YELLOW}No se encontró el archivo .env en ./config/.${NC}"
    echo -e "${YELLOW}Creando archivo .env de ejemplo...${NC}"
    
    # Crear directorio config si no existe
    mkdir -p ./config
    
    # Crear archivo .env de ejemplo
    cat > ./config/.env << EOL
# Configuración de Anything LLM
ANYTHING_LLM_API_KEY=tu_token_aqui

# Configuración de GitHub
GITHUB_TOKEN=tu_token_github_aqui

# Configuración del entorno
TALENTEK_ENV=production

# Rutas de proyecto
TALENTEK_ROOT=/app

# Configuración de notificaciones
NOTIFY_ON_COMPLETION=true
NOTIFY_ON_ERROR=true

# Configuración de seguridad
AUTO_IMPROVEMENT_PERMISSION_LEVEL=write
EOL

    echo -e "${YELLOW}Por favor, edita el archivo ./config/.env con tus credenciales antes de continuar.${NC}"
    read -p "¿Deseas editar el archivo ahora? (s/n): " edit_env
    
    if [[ $edit_env == "s" || $edit_env == "S" ]]; then
        if command -v nano &> /dev/null; then
            nano ./config/.env
        elif command -v vim &> /dev/null; then
            vim ./config/.env
        else
            echo -e "${YELLOW}Por favor, edita el archivo ./config/.env manualmente.${NC}"
        fi
    fi
fi

echo -e "${GREEN}✓ Archivo .env configurado.${NC}"

# Crear directorios necesarios
echo -e "\n${YELLOW}Creando estructura de directorios...${NC}"
mkdir -p ./data/qdrant
mkdir -p ./data/anythingllm
mkdir -p ./logs
mkdir -p ./reports

echo -e "${GREEN}✓ Estructura de directorios creada.${NC}"

# Verificar si hay actualizaciones en el repositorio
echo -e "\n${YELLOW}Verificando actualizaciones en el repositorio...${NC}"
if command -v git &> /dev/null; then
    git fetch
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse @{u})
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo -e "${YELLOW}Hay actualizaciones disponibles.${NC}"
        read -p "¿Deseas actualizar el sistema? (s/n): " update_system
        
        if [[ $update_system == "s" || $update_system == "S" ]]; then
            git pull
            echo -e "${GREEN}✓ Sistema actualizado.${NC}"
        fi
    else
        echo -e "${GREEN}✓ El sistema está actualizado.${NC}"
    fi
else
    echo -e "${YELLOW}Git no está instalado. No se puede verificar actualizaciones.${NC}"
fi

# Iniciar los servicios con Docker Compose
echo -e "\n${YELLOW}Iniciando servicios...${NC}"
docker-compose down
docker-compose build
docker-compose up -d

# Verificar que todos los servicios estén funcionando
echo -e "\n${YELLOW}Verificando estado de los servicios...${NC}"
sleep 10
docker-compose ps

# Mostrar información de acceso
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}    TALENTEKAI UNIFIED DESPLEGADO       ${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${BLUE}Acceso a los servicios:${NC}"
echo -e "  • Interfaz de usuario: ${GREEN}http://localhost:8501${NC}"
echo -e "  • API: ${GREEN}http://localhost:8502${NC}"
echo -e "  • Anything LLM: ${GREEN}http://localhost:3001${NC}"
echo -e "  • Qdrant: ${GREEN}http://localhost:6333${NC}"

echo -e "\n${BLUE}Comandos útiles:${NC}"
echo -e "  • Ver logs: ${YELLOW}docker-compose logs -f${NC}"
echo -e "  • Detener servicios: ${YELLOW}docker-compose down${NC}"
echo -e "  • Reiniciar servicios: ${YELLOW}docker-compose restart${NC}"
echo -e "  • Estado del sistema: ${YELLOW}./scripts/talentek_auto_improve.py status${NC}"

echo -e "\n${GREEN}¡Gracias por usar TalentekAI Unified!${NC}"
echo -e "${BLUE}========================================${NC}\n"