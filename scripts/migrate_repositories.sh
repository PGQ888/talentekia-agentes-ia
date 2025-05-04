#!/bin/bash
# Script para migrar repositorios antiguos al repositorio unificado de TalentekIA

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== MIGRACIÓN DE REPOSITORIOS TALENTEK IA ===${NC}"
echo "Este script migrará el código de los repositorios antiguos al nuevo repositorio unificado."
echo ""

# Directorio del repositorio unificado
UNIFIED_REPO="$(pwd)"

# Verificar que estamos en el directorio correcto
if [ ! -f "talentek.py" ]; then
    echo -e "${RED}Error: No se encontró el archivo talentek.py${NC}"
    echo "Por favor, ejecute este script desde el directorio raíz del repositorio unificado."
    exit 1
fi

# Crear directorios para los agentes si no existen
echo -e "${GREEN}Creando estructura de directorios para los agentes...${NC}"
mkdir -p src/agents/linkedin
mkdir -p src/agents/finanzas
mkdir -p src/agents/estrategia
mkdir -p src/agents/auto_improve
mkdir -p src/agents/email
mkdir -p src/agents/resumen
mkdir -p data/linkedin
mkdir -p data/finanzas
mkdir -p data/estrategia
mkdir -p data/auto_improve
mkdir -p data/email
mkdir -p data/resumen

# Solicitar rutas a los repositorios antiguos
echo -e "${YELLOW}Por favor, ingrese las rutas absolutas a los repositorios antiguos:${NC}"
echo -e "(Deje en blanco si no tiene ese repositorio)"
read -p "Repositorio de LinkedIn: " LINKEDIN_REPO
read -p "Repositorio de Finanzas: " FINANZAS_REPO
read -p "Repositorio de Estrategia: " ESTRATEGIA_REPO
read -p "Repositorio de Auto-Mejora: " AUTOMEJORA_REPO
read -p "Repositorio de Email: " EMAIL_REPO
read -p "Repositorio de Resumen: " RESUMEN_REPO

# Función para migrar un repositorio
migrate_repo() {
    local repo_path="$1"
    local agent_name="$2"
    local target_dir="$3"
    local data_dir="$4"
    
    if [ -z "$repo_path" ]; then
        echo -e "${YELLOW}Omitiendo migración de $agent_name (no se proporcionó ruta)${NC}"
        return
    fi
    
    if [ ! -d "$repo_path" ]; then
        echo -e "${RED}Error: No se encontró el repositorio de $agent_name en $repo_path${NC}"
        return
    fi
    
    echo -e "${GREEN}Migrando código del agente $agent_name...${NC}"
    
    # Buscar archivos Python en el repositorio
    if [ -d "$repo_path/src" ]; then
        echo "Copiando archivos de src/"
        cp -r "$repo_path/src"/* "$target_dir/" 2>/dev/null
    elif [ -d "$repo_path/lib" ]; then
        echo "Copiando archivos de lib/"
        cp -r "$repo_path/lib"/* "$target_dir/" 2>/dev/null
    else
        # Buscar archivos Python en el directorio raíz
        find "$repo_path" -maxdepth 1 -name "*.py" -exec cp {} "$target_dir/" \;
    fi
    
    # Copiar datos si existen
    if [ -d "$repo_path/data" ]; then
        echo "Copiando datos"
        cp -r "$repo_path/data"/* "$data_dir/" 2>/dev/null
    fi
    
    # Copiar configuración si existe
    if [ -d "$repo_path/config" ]; then
        echo "Copiando configuración"
        mkdir -p "$target_dir/config"
        cp -r "$repo_path/config"/* "$target_dir/config/" 2>/dev/null
    fi
    
    echo -e "${GREEN}✅ Migración de $agent_name completada${NC}"
}

# Migrar cada repositorio
migrate_repo "$LINKEDIN_REPO" "LinkedIn" "$UNIFIED_REPO/src/agents/linkedin" "$UNIFIED_REPO/data/linkedin"
migrate_repo "$FINANZAS_REPO" "Finanzas" "$UNIFIED_REPO/src/agents/finanzas" "$UNIFIED_REPO/data/finanzas"
migrate_repo "$ESTRATEGIA_REPO" "Estrategia" "$UNIFIED_REPO/src/agents/estrategia" "$UNIFIED_REPO/data/estrategia"
migrate_repo "$AUTOMEJORA_REPO" "Auto-Mejora" "$UNIFIED_REPO/src/agents/auto_improve" "$UNIFIED_REPO/data/auto_improve"
migrate_repo "$EMAIL_REPO" "Email" "$UNIFIED_REPO/src/agents/email" "$UNIFIED_REPO/data/email"
migrate_repo "$RESUMEN_REPO" "Resumen" "$UNIFIED_REPO/src/agents/resumen" "$UNIFIED_REPO/data/resumen"

# Crear archivos __init__.py para facilitar las importaciones
echo -e "${GREEN}Creando archivos __init__.py para facilitar importaciones...${NC}"
touch src/agents/__init__.py
touch src/agents/linkedin/__init__.py
touch src/agents/finanzas/__init__.py
touch src/agents/estrategia/__init__.py
touch src/agents/auto_improve/__init__.py
touch src/agents/email/__init__.py
touch src/agents/resumen/__init__.py

# Ajustar importaciones
echo -e "${GREEN}Ajustando importaciones en archivos Python...${NC}"
find src -name "*.py" -exec sed -i.bak 's/from src\./from /g' {} \; 2>/dev/null
find src -name "*.py" -exec sed -i.bak 's/import src\./import /g' {} \; 2>/dev/null
find src -name "*.py.bak" -delete 2>/dev/null

echo ""
echo -e "${GREEN}Migración de repositorios completada.${NC}"
echo -e "${YELLOW}A continuación, se recomienda:${NC}"
echo "1. Verificar que todos los archivos se hayan migrado correctamente"
echo "2. Ajustar manualmente las importaciones en los archivos Python si es necesario"
echo "3. Ejecutar pruebas para verificar que todo funciona correctamente"
echo ""

# Preguntar si desea conectar con un repositorio remoto en GitHub
echo -e "${BLUE}¿Desea conectar con un repositorio remoto en GitHub? (s/n)${NC}"
read -p "> " CONNECT_REMOTE

if [[ "$CONNECT_REMOTE" == "s" || "$CONNECT_REMOTE" == "S" ]]; then
    read -p "URL del repositorio remoto (ejemplo: https://github.com/tu-usuario/TalentekIA.git): " REMOTE_URL
    
    if [ -n "$REMOTE_URL" ]; then
        echo -e "${GREEN}Conectando con repositorio remoto...${NC}"
        git remote add origin "$REMOTE_URL"
        git push -u origin main || git push -u origin master
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Repositorio conectado y código subido a GitHub.${NC}"
        else
            echo -e "${RED}Error al conectar con el repositorio remoto.${NC}"
            echo "Asegúrese de que el repositorio existe y tiene permisos de acceso."
        fi
    else
        echo -e "${YELLOW}No se proporcionó una URL de repositorio remoto.${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Proceso de migración finalizado.${NC}"
echo -e "${BLUE}Puede ejecutar './start_talentek.sh' para iniciar el sistema unificado.${NC}"