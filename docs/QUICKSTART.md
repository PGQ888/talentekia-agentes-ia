# 🚀 Guía Rápida de Inicio - TalentekIA

Esta guía te ayudará a poner en marcha rápidamente la plataforma TalentekIA en tu entorno local.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- Claves API para servicios externos (opcional, pero recomendado)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/PGQ888/talentek-ia.git
cd talentek-ia
```

### 2. Configurar el entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
```

### 3. Instalar dependencias y configurar el sistema

```bash
# Método 1: Usando make
make setup

# Método 2: Manualmente
python initialize_system.py
```

### 4. Configurar las claves API

Edita el archivo `.env` con tus claves API:

```bash
# Abrir el archivo .env con tu editor preferido
nano .env
```

Asegúrate de configurar al menos la clave API de OpenAI:

```
OPENAI_API_KEY=tu_clave_api_openai
```

## Uso Básico

### Iniciar la aplicación

```bash
# Método 1: Usando make
make run

# Método 2: Directamente con streamlit
streamlit run src/interface/streamlit_app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado, generalmente en http://localhost:8501

### Navegación por la interfaz

La interfaz de TalentekIA está organizada en las siguientes secciones:

1. **Dashboard**: Vista general del sistema y estado de los agentes
2. **Agentes**: Gestión y ejecución de agentes individuales
3. **Resultados**: Visualización de los datos e informes generados
4. **Configuración**: Ajustes del sistema y de los agentes
5. **Documentación**: Guías y documentación del sistema

## Ejecutar un Agente

1. Navega a la sección "Agentes" en el menú lateral
2. Selecciona el agente que deseas ejecutar
3. Haz clic en el botón "Ejecutar [nombre del agente]"
4. Espera a que el agente complete su ejecución
5. Los resultados se mostrarán automáticamente o puedes verlos en la sección "Resultados"

## Configuración de Agentes

Cada agente puede configurarse individualmente:

1. Ve a la sección "Configuración"
2. Ajusta los parámetros según tus necesidades
3. Guarda la configuración

## Programación de Ejecuciones Automáticas

Para configurar ejecuciones automáticas de los agentes:

```bash
# Iniciar sincronización automática
./start_auto_sync.sh
# o
make sync-start

# Detener sincronización automática
./stop_auto_sync.sh
# o
make sync-stop
```

## Solución de Problemas Comunes

### Error al conectar con las APIs

Verifica que las claves API en el archivo `.env` sean correctas y estén activas.

### La aplicación no se inicia

Asegúrate de que todas las dependencias estén instaladas correctamente:

```bash
pip install -r requirements.txt
```

### Errores en la ejecución de los agentes

Revisa los logs en la carpeta `logs/` para obtener más información sobre los errores.

## Siguientes Pasos

Una vez que tengas la plataforma funcionando:

1. Explora los diferentes agentes disponibles
2. Personaliza la configuración según tus necesidades
3. Consulta la documentación completa en la sección "Documentación"
4. Considera contribuir al desarrollo del proyecto

## Recursos Adicionales

- [Documentación completa](docs/DESARROLLO.md)
- [GitHub del proyecto](https://github.com/PGQ888/talentek-ia)
- [Reportar problemas](https://github.com/PGQ888/talentek-ia/issues)