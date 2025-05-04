#!/bin/bash
# Script para alternar entre modos de configuración en TalentekIA
# Permite cambiar entre configuración estándar y optimizada para Mac M2

# Colores para mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Obtener el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Función para mostrar el uso del script
show_usage() {
    echo -e "${BLUE}Uso: $0 [standard|m2|status]${NC}"
    echo -e "  ${YELLOW}standard${NC} - Cambiar a configuración estándar"
    echo -e "  ${YELLOW}m2${NC}       - Cambiar a configuración optimizada para Mac M2"
    echo -e "  ${YELLOW}status${NC}   - Mostrar modo actual"
    exit 1
}

# Función para verificar el modo actual
check_current_mode() {
    if [ -f "$SCRIPT_DIR/.env" ]; then
        if grep -q "MAC_OPTIMIZED=true" "$SCRIPT_DIR/.env"; then
            echo -e "${GREEN}Modo actual: Optimizado para Mac M2${NC}"
        else
            echo -e "${BLUE}Modo actual: Estándar${NC}"
        fi
    else
        echo -e "${RED}Error: No se encontró el archivo .env${NC}"
        exit 1
    fi
}

# Verificar argumentos
if [ $# -ne 1 ]; then
    show_usage
fi

# Procesar comando
case "$1" in
    standard)
        # Verificar que existe el archivo .env.standard
        if [ ! -f "$SCRIPT_DIR/.env.standard" ]; then
            # Si no existe, crear una copia del .env actual
            if [ -f "$SCRIPT_DIR/.env" ]; then
                cp "$SCRIPT_DIR/.env" "$SCRIPT_DIR/.env.standard"
                echo -e "${GREEN}✓ Se ha creado una copia de seguridad de la configuración estándar${NC}"
            else
                echo -e "${RED}Error: No se encontró el archivo .env${NC}"
                exit 1
            fi
        fi
        
        # Cambiar a configuración estándar
        cp "$SCRIPT_DIR/.env.standard" "$SCRIPT_DIR/.env"
        echo -e "${GREEN}✓ Cambiado a modo estándar${NC}"
        ;;
        
    m2)
        # Verificar que existe el archivo .env.m2
        if [ ! -f "$SCRIPT_DIR/.env.m2" ]; then
            echo -e "${RED}Error: No se encontró el archivo .env.m2${NC}"
            echo -e "${YELLOW}Ejecute primero el script de inicialización para crear la configuración optimizada.${NC}"
            exit 1
        fi
        
        # Hacer copia de seguridad si no existe
        if [ ! -f "$SCRIPT_DIR/.env.standard" ]; then
            if [ -f "$SCRIPT_DIR/.env" ]; then
                cp "$SCRIPT_DIR/.env" "$SCRIPT_DIR/.env.standard"
                echo -e "${GREEN}✓ Se ha creado una copia de seguridad de la configuración estándar${NC}"
            fi
        fi
        
        # Cambiar a configuración optimizada
        cp "$SCRIPT_DIR/.env.m2" "$SCRIPT_DIR/.env"
        echo -e "${GREEN}✓ Cambiado a modo optimizado para Mac M2${NC}"
        ;;
        
    status)
        check_current_mode
        ;;
        
    *)
        show_usage
        ;;
esac

# Mostrar instrucciones adicionales
if [ "$1" != "status" ]; then
    echo -e "${BLUE}Para iniciar TalentekIA con la nueva configuración, ejecute:${NC}"
    echo -e "${YELLOW}./start_talentekia.sh${NC}"
fi

exit 0