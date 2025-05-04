# TalentekIA

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/PGQ888/talentekia-agentes-ia/ci.yml?branch=main)
![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema de agentes de IA personalizados para automatización y análisis, optimizado para Mac con Apple Silicon (M1/M2/M3).

## Características

- **Agentes Especializados**: LinkedIn, Finanzas, Estrategia, Auto-optimización y más
- **Optimizado para Apple Silicon**: Aprovecha al máximo el rendimiento de los chips M1/M2/M3
- **Interfaz Unificada**: Gestiona todos los agentes desde una sola interfaz
- **Monitoreo de Rendimiento**: Herramientas específicas para monitorear el uso de recursos
- **Integración con APIs**: Conecta con OpenAI, HuggingFace, LinkedIn y más

## Instalación

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/PGQ888/talentekia-agentes-ia.git
cd talentekia-agentes-ia
```

2. Crear un entorno virtual:

```bash
make venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
# Para instalación básica
make deps

# Para desarrollo
make dev-deps

# Para Mac M1/M2/M3
make m2-deps
```

4. Configurar variables de entorno:

```bash
cp .env.example .env
# Edita el archivo .env con tus claves API
```

## Uso

### Iniciar el sistema

```bash
./start_talentek.sh
```

O usando el Makefile:

```bash
make run
```

### Monitorear rendimiento (Mac M1/M2/M3)

```bash
./scripts/monitor_m2.py --continuous
```

O usando el Makefile:

```bash
make monitor
```

### Opciones disponibles

El script `start_talentek.sh` ofrece varias opciones:

1. **Inicializar el sistema**: Configura el sistema por primera vez
2. **Ejecutar todos los agentes**: Inicia todos los agentes disponibles
3. **Ejecutar agente específico**: Inicia un agente en particular
4. **Sincronizar con GitHub**: Actualiza el código desde el repositorio
5. **Iniciar interfaz web**: Inicia la interfaz de usuario web
6. **Modo optimizado para Mac M2**: Inicia el sistema con optimizaciones específicas para Apple Silicon

## Estructura del proyecto

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
├── docs/                  # Documentación del sistema
├── logs/                  # Archivos de registro
├── scripts/               # Scripts auxiliares
│   └── legacy/            # Scripts antiguos (mantenidos por compatibilidad)
├── tests/                 # Pruebas unitarias y de integración
├── .env                   # Variables de entorno (no se sube a GitHub)
├── README.md              # Documentación principal
├── requirements.txt       # Dependencias del sistema
├── talentek.py            # Punto de entrada principal
└── start_talentek.sh      # Script de inicio rápido
```

## Optimizaciones para Mac M1/M2/M3

Este proyecto incluye optimizaciones específicas para equipos con Apple Silicon:

- Utilización de MPS (Metal Performance Shaders) para aceleración de ML
- Configuraciones específicas para TensorFlow y PyTorch en Apple Silicon
- Herramientas de monitoreo optimizadas para visualizar el rendimiento

Para activar estas optimizaciones:

```bash
# Configurar variables de entorno
export PYTORCH_ENABLE_MPS_FALLBACK=1
export TF_ENABLE_ONEDNN_OPTS=0

# O usar el comando del Makefile
make setup-m2
```

## Desarrollo

### Comandos útiles

```bash
# Formatear código
make format

# Ejecutar linters
make lint

# Ejecutar pruebas
make test

# Generar documentación
make docs
```

### Pre-commit hooks

Este proyecto utiliza pre-commit hooks para mantener la calidad del código:

```bash
# Instalar pre-commit hooks
pre-commit install

# Ejecutar manualmente en todos los archivos
pre-commit run --all-files
```

## Documentación

La documentación completa está disponible en la carpeta `docs/`. Para generarla:

```bash
make docs
```

## Contribuir

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Pablo Giraldez - [@PGQ888](https://github.com/PGQ888) - pablo@talentek.io

Enlace del proyecto: [https://github.com/PGQ888/talentekia-agentes-ia](https://github.com/PGQ888/talentekia-agentes-ia)