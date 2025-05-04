# Migración y Unificación de Repositorios TalentekIA

## Descripción del Proceso

Este documento describe el proceso de migración y unificación de múltiples repositorios de TalentekIA en un único repositorio centralizado. La unificación se realizó para simplificar el mantenimiento, mejorar la coherencia del código y facilitar la integración entre los diferentes agentes de IA.

## Repositorios Originales

Los siguientes repositorios se unificaron en este repositorio centralizado:

1. **talentek-gpt**: Repositorio original con funcionalidades básicas de interacción con GPT
2. **TalentekIA**: Repositorio con implementaciones de agentes específicos
3. **talentekia-agentes-ia**: Repositorio final unificado (este repositorio)

## Estructura Unificada

La estructura del repositorio unificado sigue una organización modular y coherente:

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

## Proceso de Migración

La migración se realizó siguiendo estos pasos:

1. **Preparación**: Se creó un script de migración (`scripts/migrate_repositories.sh`) para facilitar la transferencia de código entre repositorios.

2. **Unificación de código**: Se consolidó el código de todos los agentes en una estructura común bajo `src/agents/`.

3. **Resolución de conflictos**: Se resolvieron conflictos en archivos clave como `README.md`, `requirements.txt`, `src/agents/base_agent.py` y `start_talentek.sh`.

4. **Limpieza de estructura**: Se eliminaron carpetas redundantes y se reorganizaron los scripts para mantener una estructura coherente.

5. **Pruebas**: Se verificó que todas las funcionalidades siguieran funcionando correctamente en el repositorio unificado.

6. **Finalización**: Se archivaron los repositorios antiguos para mantenerlos como referencia histórica.

## Optimizaciones para Mac M2

Este repositorio incluye optimizaciones específicas para equipos con Apple Silicon (M1/M2):

- Detección automática de la arquitectura
- Configuración óptima de parámetros de rendimiento
- Utilización de MPS (Metal Performance Shaders) cuando está disponible
- Variables de entorno específicas para mejorar el rendimiento en Apple Silicon

## Uso del Sistema Unificado

Para utilizar el sistema unificado:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/PGQ888/talentekia-agentes-ia.git
   cd talentekia-agentes-ia
   ```

2. Ejecuta el script de inicio:
   ```bash
   chmod +x start_talentek.sh
   ./start_talentek.sh
   ```

3. Sigue las instrucciones en pantalla para inicializar el sistema y ejecutar los agentes deseados.

## Notas Adicionales

- Los repositorios originales han sido archivados y son de solo lectura.
- Todas las nuevas características y correcciones deben realizarse en este repositorio unificado.
- Se recomienda seguir las convenciones de código establecidas en este repositorio para mantener la coherencia.

## Fecha de Migración

La migración y unificación se completó el 4 de mayo de 2025.