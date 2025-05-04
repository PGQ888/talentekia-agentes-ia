archivo# 🛠️ Guía de Desarrollo - TalentekIA

Esta guía está dirigida a desarrolladores que deseen contribuir al proyecto TalentekIA o extender su funcionalidad.

## Arquitectura del Sistema

TalentekIA está estructurado siguiendo un patrón modular con los siguientes componentes principales:

### 1. Agentes

Los agentes son el núcleo del sistema. Cada agente es una clase Python que hereda de `BaseAgent` y se encarga de realizar una tarea específica. Los agentes están ubicados en `src/agents/`.

```
src/agents/
├── base_agent.py       # Clase base para todos los agentes
├── agent_manager.py    # Gestor centralizado de agentes
├── config.py           # Configuración específica de agentes
├── linkedin_agent.py   # Agente para análisis de LinkedIn
└── ...                 # Otros agentes específicos
```

### 2. Interfaz de Usuario

La interfaz de usuario está desarrollada con Streamlit y se encuentra en `src/interface/`.

```
src/interface/
└── streamlit_app.py    # Aplicación principal de Streamlit
```

### 3. Utilidades

Las funciones y clases de utilidad se encuentran en `src/utils/`.

```
src/utils/
├── helpers.py          # Funciones auxiliares generales
├── env_loader.py       # Cargador de variables de entorno
├── weekly_summary.py   # Generador de resúmenes semanales
└── ...                 # Otras utilidades
```

## Creación de un Nuevo Agente

Para crear un nuevo agente, sigue estos pasos:

1. Crea un nuevo archivo en `src/agents/`, por ejemplo `mi_agente.py`
2. Define una clase que herede de `BaseAgent`
3. Implementa los métodos requeridos: `run()`, `process_data()` y `generate_report()`
4. Registra el agente en `config/settings.py`

### Ejemplo de un Nuevo Agente

```python
# src/agents/mi_agente.py
from typing import Dict, List, Any, Optional
import pandas as pd
from src.agents.base_agent import BaseAgent

class MiAgente(BaseAgent):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("mi_agente", config)
    
    def run(self):
        """Método principal que ejecuta el agente"""
        self.logger.info("Iniciando ejecución de MiAgente")
        
        # Lógica principal del agente
        data = self._recopilar_datos()
        
        # Procesar los datos
        df = self.process_data(data)
        
        # Generar informe
        report = self.generate_report(df)
        
        # Guardar resultados
        self.save_results(df, report)
        
        return True
    
    def _recopilar_datos(self):
        """Método privado para recopilar datos"""
        # Implementación específica
        return [{"campo1": "valor1", "campo2": "valor2"}]
    
    def process_data(self, data: List[Dict[str, Any]]):
        """Procesa los datos recopilados"""
        return pd.DataFrame(data)
    
    def generate_report(self, df: pd.DataFrame):
        """Genera un informe basado en los datos procesados"""
        return f"""# Informe de MiAgente
        
## Resumen
        
Se han procesado {len(df)} registros.
        
## Detalles
        
{df.describe().to_markdown()}
        
## Conclusiones
        
Este es un informe de ejemplo generado por MiAgente.
"""

# Función para crear una instancia del agente
def create_agent(config=None):
    return MiAgente(config)
```

### Registro del Nuevo Agente

Añade la configuración de tu agente en `config/settings.py`:

```python
# En la función create_default_config()
default_config = {
    # ... configuración existente ...
    "agents": {
        # ... otros agentes ...
        "mi_agente": {
            "enabled": True,
            "description": "Descripción de mi agente personalizado",
            "parameters": {
                "param1": "valor1",
                "param2": "valor2"
            }
        }
    }
}
```

## Integración con Servicios Externos

### OpenAI

Para integrar con la API de OpenAI:

```python
from openai import OpenAI
from src.utils.env_loader import EnvLoader

# Obtener la clave API
api_key = EnvLoader().get_api_key("openai")

# Crear cliente
client = OpenAI(api_key=api_key)

# Realizar una llamada a la API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Analiza estos datos y dame un resumen."}
    ]
)

# Procesar la respuesta
result = response.choices[0].message.content
```

### Anthropic

Para integrar con la API de Anthropic:

```python
from anthropic import Anthropic
from src.utils.env_loader import EnvLoader

# Obtener la clave API
api_key = EnvLoader().get_api_key("anthropic")

# Crear cliente
client = Anthropic(api_key=api_key)

# Realizar una llamada a la API
response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Analiza estos datos y dame un resumen."}
    ]
)

# Procesar la respuesta
result = response.content[0].text
```

## Pruebas

Las pruebas se encuentran en el directorio `tests/`. Utilizamos pytest como framework de pruebas.

### Estructura de Pruebas

```
tests/
├── conftest.py         # Configuración y fixtures para pytest
├── test_agents.py      # Pruebas para los agentes
└── test_interface.py   # Pruebas para la interfaz
```

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas específicas
pytest tests/test_agents.py

# Ejecutar con cobertura
pytest --cov=src tests/
```

## Estilo de Código

Seguimos las convenciones de estilo PEP 8 para Python. Utilizamos las siguientes herramientas para mantener la calidad del código:

- **Black**: Formateador de código
- **isort**: Ordenador de importaciones
- **flake8**: Linter de código

### Formatear el Código

```bash
# Usando make
make format

# Manualmente
black src/ tests/
isort src/ tests/
```

### Verificar el Estilo

```bash
# Usando make
make lint

# Manualmente
flake8 src/ tests/
```

## Flujo de Trabajo de Desarrollo

1. **Configurar el entorno de desarrollo**:
   ```bash
   make install-dev
   ```

2. **Crear una rama para tu funcionalidad**:
   ```bash
   git checkout -b feature/mi-funcionalidad
   ```

3. **Implementar cambios y pruebas**

4. **Formatear y verificar el código**:
   ```bash
   make format
   make lint
   ```

5. **Ejecutar pruebas**:
   ```bash
   make test
   ```

6. **Commit y push**:
   ```bash
   git add .
   git commit -m "Añadir mi funcionalidad"
   git push origin feature/mi-funcionalidad
   ```

7. **Crear un Pull Request** en GitHub

## Despliegue

### Despliegue Local

```bash
# Instalar el paquete en modo desarrollo
pip install -e .

# Ejecutar la aplicación
talentekia
```

### Despliegue en Servidor

1. Clonar el repositorio en el servidor
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar variables de entorno en `.env`
4. Iniciar la aplicación con un servidor WSGI como Gunicorn:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.interface.api:app
   ```

## Recursos Adicionales

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Documentación de OpenAI](https://platform.openai.com/docs/api-reference)
- [Documentación de Anthropic](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Guía de estilo PEP 8](https://peps.python.org/pep-0008/)
- [Documentación de pytest](https://docs.pytest.org/)