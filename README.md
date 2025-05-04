# 🧠 TalentekIA - Sistema Unificado de Agentes IA

Plataforma unificada para gestionar y ejecutar agentes de inteligencia artificial personalizados para diferentes tareas profesionales y personales.

## 📋 Descripción

TalentekIA es una plataforma unificada que integra múltiples agentes de inteligencia artificial especializados en diferentes áreas:

- **LinkedIn Pro**: Análisis de ofertas de empleo y tendencias del mercado laboral
- **Finanzas Personales**: Gestión y optimización de finanzas personales
- **Estrategia Comercial**: Asistente para desarrollo de estrategias de negocio
- **Auto Mejora**: Optimización del rendimiento del sistema y desarrollo personal
- **Email**: Automatización de la gestión de correos electrónicos
- **Resumen**: Generación de resúmenes semanales de actividad

El sistema está diseñado para ser modular, escalable y optimizado para diferentes plataformas, incluyendo optimizaciones específicas para Apple Silicon (M1/M2).

## 📁 Estructura del Proyecto

```
TalentekIA/
├── src/                   # Código fuente principal
│   ├── agents/            # Todos los agentes del sistema
│   │   ├── linkedin/      # Agente de LinkedIn
│   │   ├── finanzas/      # Agente de finanzas personales
│   │   ├── auto_improve/  # Agente de optimización
│   │   ├── estrategia/    # Agente de estrategia comercial
│   │   ├── email/         # Agente de email
│   │   └── resumen/       # Agente de resumen
│   ├── core/              # Componentes centrales del sistema
│   ├── interface/         # Interfaces de usuario
│   └── utils/             # Utilidades compartidas
├── config/                # Configuración centralizada
├── data/                  # Datos generados por los agentes
│   ├── input/             # Datos de entrada
│   └── output/            # Datos de salida
├── docs/                  # Documentación del sistema
├── logs/                  # Archivos de registro
├── scripts/               # Scripts auxiliares
├── tests/                 # Pruebas unitarias y de integración
├── .env                   # Variables de entorno (no se sube a GitHub)
├── .gitignore             # Archivos a ignorar por Git
├── README.md              # Documentación principal
├── requirements.txt       # Dependencias del sistema
├── talentek.py            # Punto de entrada principal
└── start_talentek.sh      # Script de inicio rápido
```

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Acceso a API keys necesarias (OpenAI, Anthropic, HuggingFace, etc.)

### Pasos de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/PGQ888/talentekia-agentes-ia.git
   cd talentekia-agentes-ia
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
   ./start_talentek.sh
   # Seleccionar opción 1 para inicializar el sistema
   ```

## 🖥️ Uso

### Usando el script de inicio

```bash
./start_talentek.sh
```

Este script mostrará un menú con las siguientes opciones:
1. Inicializar el sistema
2. Ejecutar todos los agentes
3. Ejecutar agente específico
4. Sincronizar con GitHub
5. Iniciar interfaz web
6. Salir

### Usando el punto de entrada principal

### Inicializar el sistema

```bash
python talentek.py --init
```

### Ejecutar todos los agentes

```bash
python talentek.py --run all
```

### Ejecutar un agente específico

```bash
python talentek.py --run linkedin
```

### Ejecutar agentes en paralelo

```bash
python talentek.py --run all --parallel
```

### Sincronizar con GitHub

```bash
python talentek.py --sync
```

### Iniciar la interfaz web

```bash
streamlit run src/interface/streamlit_app.py
```

## 📊 Características principales

- **Interfaz unificada**: Gestión centralizada de todos los agentes
- **Automatización**: Programación de tareas y ejecuciones periódicas
- **Informes detallados**: Generación de informes en formato Markdown y datos tabulares
- **Integración con servicios externos**: GitHub, HuggingFace, AnythingLLM
- **Configuración flexible**: Ajuste de parámetros según necesidades

## ⚡ Optimizaciones para Apple Silicon (M1/M2)

El sistema incluye optimizaciones específicas para equipos con Apple Silicon:

- Detección automática de arquitectura
- Configuración óptima de parámetros de rendimiento
- Utilización de MPS (Metal Performance Shaders) cuando está disponible

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

Link del proyecto: [https://github.com/PGQ888/talentekia-agentes-ia](https://github.com/PGQ888/talentekia-agentes-ia)