# TalentekIA - Sistema Unificado

Sistema de agentes de IA personalizados para automatización y análisis de datos.

## Descripción

TalentekIA es una plataforma unificada que integra múltiples agentes de inteligencia artificial especializados en diferentes áreas como LinkedIn, finanzas personales, estrategia comercial, y más. El sistema está diseñado para ser modular, escalable y optimizado para diferentes plataformas, incluyendo optimizaciones específicas para Apple Silicon (M1/M2).

## Estructura del Proyecto

```
TalentekIA/
├── src/                   # Código fuente principal
│   ├── agents/            # Todos los agentes del sistema
│   │   ├── linkedin/      # Agente de LinkedIn
│   │   ├── finanzas/      # Agente de finanzas personales
│   │   ├── auto_improve/  # Agente de optimización
│   │   ├── estrategia/    # Agente de estrategia comercial
│   │   └── ...
│   ├── core/              # Componentes centrales del sistema
│   └── utils/             # Utilidades compartidas
├── config/                # Configuración centralizada
├── data/                  # Datos generados por los agentes
├── docs/                  # Documentación del sistema
├── logs/                  # Archivos de registro
├── scripts/               # Scripts auxiliares
├── .env                   # Variables de entorno (no se sube a GitHub)
├── .gitignore             # Archivos a ignorar por Git
├── README.md              # Documentación principal
├── requirements.txt       # Dependencias del sistema
└── talentek.py            # Punto de entrada principal
```

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/TalentekIA.git
   cd TalentekIA
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar .env con tus claves API y configuraciones
   ```

## Uso

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

## Agentes Disponibles

- **LinkedIn**: Busca y analiza ofertas de trabajo en LinkedIn
- **Finanzas**: Analiza y gestiona finanzas personales
- **Estrategia Comercial**: Genera propuestas de estrategia comercial
- **Auto-Mejora**: Optimiza el rendimiento del sistema
- **Email**: Automatiza la gestión de correos electrónicos
- **Resumen**: Genera resúmenes semanales de la actividad

## Optimizaciones para Apple Silicon (M1/M2)

El sistema incluye optimizaciones específicas para equipos con Apple Silicon:

- Detección automática de arquitectura
- Configuración óptima de parámetros de rendimiento
- Utilización de MPS (Metal Performance Shaders) cuando está disponible

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añade nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un nuevo Pull Request

## Licencia

Este proyecto está licenciado bajo [tu licencia] - ver el archivo LICENSE para más detalles.