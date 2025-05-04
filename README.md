# 🧠 TalentekIA - Plataforma de Agentes IA

Plataforma unificada para gestionar y ejecutar agentes de inteligencia artificial personalizados para diferentes tareas profesionales y personales.

## 📋 Descripción

TalentekIA es una plataforma que integra diversos agentes de IA especializados en diferentes áreas:

- **LinkedIn Pro**: Análisis de ofertas de empleo y tendencias del mercado laboral
- **Estrategia Comercial**: Asistente para desarrollo de estrategias de negocio
- **Finanzas Personales**: Gestión y optimización de finanzas personales
- **Auto Mejora**: Asistente para desarrollo personal y profesional

Todos los agentes se gestionan a través de una interfaz unificada desarrollada con Streamlit.

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Acceso a API keys necesarias (OpenAI, Anthropic, HuggingFace, etc.)

### Pasos de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/PGQ888/talentek-ia.git
   cd talentek-ia
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar el archivo .env con tus API keys y configuraciones
   ```

5. Inicializar el sistema:
   ```bash
   python initialize_system.py
   ```

## 🖥️ Uso

### Iniciar la interfaz de usuario

```bash
streamlit run src/interface/streamlit_app.py
```

### Ejecutar un agente específico

```bash
python -c "from src.agents.agent_manager import execute_agent; execute_agent('linkedin_agent')"
```

### Programar ejecuciones automáticas

```bash
./start_auto_sync.sh
```

## 📁 Estructura del proyecto

```
talentek-ia/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── agents/
│   │   ├── linkedin_agent.py
│   │   ├── estrategia_comercial.py
│   │   ├── finanzas_personales.py
│   │   ├── auto_mejora.py
│   │   ├── base_agent.py
│   │   ├── agent_manager.py
│   │   └── config.py
│   ├── interface/
│   │   └── streamlit_app.py
│   └── utils/
│       ├── helpers.py
│       ├── env_loader.py
│       ├── weekly_summary.py
│       └── github_integration.py
├── data/
│   ├── input/
│   └── output/
├── docs/
│   ├── user_manual.md
│   ├── DESARROLLO.md
│   └── QUICKSTART.md
└── tests/
    ├── test_agents.py
    └── test_interface.py
```

## 📊 Características principales

- **Interfaz unificada**: Gestión centralizada de todos los agentes
- **Automatización**: Programación de tareas y ejecuciones periódicas
- **Informes detallados**: Generación de informes en formato Markdown y datos tabulares
- **Integración con servicios externos**: GitHub, HuggingFace, AnythingLLM
- **Configuración flexible**: Ajuste de parámetros según necesidades

## 🔧 Configuración

La configuración del sistema se realiza a través de:

1. Archivo `.env` para variables de entorno sensibles
2. Interfaz de configuración en la aplicación Streamlit
3. Archivos de configuración en formato JSON para cada agente

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Realiza tus cambios y haz commit (`git commit -m 'Add some amazing feature'`)
4. Sube los cambios a tu fork (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 📞 Contacto

Pablo Giráldez - [@PGQ888](https://twitter.com/PGQ888) - pablo@talentek.es

Link del proyecto: [https://github.com/PGQ888/talentek-ia](https://github.com/PGQ888/talentek-ia)