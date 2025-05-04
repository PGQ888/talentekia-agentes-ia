# TalentekSystem Unificado

Sistema integrado de agentes de IA personalizados, optimizado para Mac con chip M2.

## Descripción

TalentekSystem Unificado es una plataforma que integra múltiples agentes de IA para automatizar tareas personales y profesionales. El sistema está diseñado específicamente para funcionar de manera óptima en Mac con chips Apple Silicon (M1/M2).

## Características

- **Optimizado para Apple Silicon**: Aprovecha al máximo el rendimiento de los chips M1/M2
- **Arquitectura modular**: Agentes independientes que pueden ejecutarse por separado o en conjunto
- **Configuración centralizada**: Archivo TOML para gestionar todos los agentes
- **Ejecución paralela o secuencial**: Flexibilidad para ejecutar los agentes según necesidades
- **Logging integrado**: Registro detallado de todas las operaciones

## Agentes disponibles

- **LinkedIn Pro**: Busca ofertas de trabajo, envía mensajes y genera publicaciones estratégicas
- **Gestor de Finanzas Personales**: Analiza gastos, activos, ahorro y propone optimizaciones
- **Auto Improve**: Optimiza el entorno técnico en Mac M2
- **Estrategia Comercial**: Redacta propuestas de valor según cliente y sector
- **Resumen Semanal**: Genera reporte semanal de tareas, eventos y actividad del sistema

## Requisitos

- macOS con chip Apple Silicon (M1/M2)
- Python 3.9+
- pip (gestor de paquetes de Python)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/PGQ888/TalentekSystem.git
   cd TalentekSystemUnified
   ```

2. Ejecuta el script de inicio:
   ```bash
   ./start_talentek.sh
   ```
   Este script creará automáticamente un entorno virtual e instalará todas las dependencias necesarias.

## Uso

### Iniciar el sistema

```bash
./start_talentek.sh
```

El script mostrará un menú con las siguientes opciones:

1. Ejecutar todos los agentes (paralelo)
2. Ejecutar todos los agentes (secuencial)
3. Listar agentes disponibles
4. Ejecutar un agente específico
5. Salir

### Ejecución manual de agentes

También puedes ejecutar los agentes directamente usando el lanzador unificado:

```bash
# Ejecutar todos los agentes en paralelo
python launch_talentek_system.py

# Ejecutar todos los agentes secuencialmente
python launch_talentek_system.py --sequential

# Listar agentes disponibles
python launch_talentek_system.py --list

# Ejecutar un agente específico
python launch_talentek_system.py --agent linkedin
```

## Configuración

La configuración principal se encuentra en `config/talentek_agentes_config.toml`. Este archivo contiene:

- Configuración del entorno
- Personalización del usuario
- Configuración específica de cada agente

## Estructura de directorios

```
TalentekSystemUnified/
├── agents/                # Scripts de los agentes
├── config/               # Archivos de configuración
├── data/                 # Datos generados por los agentes
│   ├── finanzas/         # Datos financieros
│   ├── informes/         # Informes generados
│   ├── plantillas/       # Plantillas para los agentes
│   ├── propuestas/       # Propuestas generadas
│   └── temp/             # Archivos temporales
├── docs/                 # Documentación
├── logs/                 # Archivos de registro
├── scripts/              # Scripts auxiliares
├── utils/                # Utilidades compartidas
├── launch_talentek_system.py  # Lanzador principal
└── start_talentek.sh     # Script de inicio
```

## Personalización

Puedes personalizar el comportamiento de los agentes modificando el archivo `config/talentek_agentes_config.toml`.

## Licencia

Este proyecto es de uso personal para Pablo Giráldez.

## Autor

Pablo Giráldez - Sistema desarrollado por TalentekIA