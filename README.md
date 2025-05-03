# TalentekIA - Panel Inteligente de Agentes

## 📋 Descripción

TalentekIA es una aplicación multiagente personal que utiliza inteligencia artificial para automatizar y optimizar diversas tareas profesionales. La plataforma integra varios agentes especializados que trabajan en conjunto para proporcionar información valiosa y automatizar procesos repetitivos.

## ✨ Características

- **🔍 Agente LinkedIn Pro**: Escanea LinkedIn en busca de oportunidades de trabajo y candidatos potenciales
- **📊 Agente de Estrategia Comercial**: Analiza tendencias del mercado y genera estrategias comerciales personalizadas
- **💵 Agente de Finanzas Personales**: Analiza tus finanzas y proporciona recomendaciones personalizadas
- **⚙️ Agente de Auto Mejora**: Analiza tu rendimiento y proporciona recomendaciones para mejorar
- **📋 Resumen Semanal**: Genera informes semanales consolidando la información de todos los agentes
- **⚙️ Configuración**: Panel de configuración para personalizar el comportamiento de los agentes

## 🚀 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/PGQ888/talentekia-agentes-ia.git
cd talentekia-agentes-ia
```

2. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita el archivo .env con tus claves API
```

## 💻 Uso

Para iniciar la aplicación:

```bash
streamlit run streamlit_app_fixed.py
```

La aplicación estará disponible en http://localhost:8501

## 📁 Estructura del Proyecto

```
talentekia-agentes-ia/
├── docs/                    # Archivos generados por los agentes
│   ├── linkedin_ofertas.csv # Datos de ofertas de LinkedIn
│   └── linkedin_ofertas.md  # Resumen en Markdown de las ofertas
├── scripts/                 # Módulos de la aplicación
│   ├── weekly_summary.py    # Generador de resúmenes semanales
│   ├── config_tab_fixed.py  # Panel de configuración
│   └── run_weekly_summary.py # Script para ejecutar resúmenes programados
├── agents/                  # Implementación de los agentes
├── config/                  # Archivos de configuración
├── streamlit_app_fixed.py   # Aplicación principal Streamlit
└── README.md                # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Python**: Lenguaje principal de desarrollo
- **Streamlit**: Framework para la interfaz de usuario
- **Pandas**: Procesamiento y análisis de datos
- **LangChain**: Framework para agentes de IA
- **OpenAI API**: Motor de IA para los agentes

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

- **Pablo Giraldez** - [PGQ888](https://github.com/PGQ888)