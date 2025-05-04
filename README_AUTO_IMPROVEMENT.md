# Sistema de Auto-Mejora para TalentekAI Unified

Este sistema de auto-mejora analiza periódicamente el código de la aplicación TalentekAI Unified para detectar problemas, sugerir optimizaciones y mantener las dependencias actualizadas.

## Características principales

- **Análisis de dependencias**: Detecta paquetes y librerías obsoletas y sugiere actualizaciones.
- **Análisis de calidad de código**: Utiliza herramientas como ESLint y Pylint para detectar problemas de calidad.
- **Análisis de rendimiento**: Identifica patrones de código que podrían causar problemas de rendimiento.
- **Generación de reportes**: Crea reportes detallados con todas las mejoras sugeridas.
- **Ejecución programada**: Se puede configurar para ejecutarse automáticamente de forma diaria, semanal o mensual.
- **Notificaciones por email**: Opcionalmente envía los reportes por correo electrónico.
- **Compatibilidad multiplataforma**: Funciona en macOS, Linux y Windows.
- **Integración con GitHub**: Sincroniza automáticamente las mejoras con tu repositorio de GitHub.

## Requisitos previos

- Python 3.6 o superior
- Para análisis de JavaScript/TypeScript: Node.js y ESLint (opcional)
- Para análisis de Python: Pylint (opcional)
- Permisos de administrador para programar tareas (en Windows)
- Repositorio Git configurado con acceso a GitHub (para sincronización)

## Configuración

El sistema utiliza un archivo de configuración ubicado en `config/auto_improvement_config.json`. La primera vez que ejecute cualquiera de los scripts, se creará automáticamente con valores predeterminados.

Opciones de configuración:

```json
{
  "email_notifications": false,
  "email_to": "usuario@ejemplo.com",
  "smtp_server": "smtp.ejemplo.com",
  "smtp_port": 587,
  "smtp_user": "usuario",
  "smtp_password": "contraseña",
  "run_frequency": "weekly",
  "analyze_dependencies": true,
  "analyze_code_quality": true,
  "analyze_performance": true,
  "auto_apply_safe_fixes": false,
  "ignored_directories": ["node_modules", "dist", ".git"],
  "custom_rules": []
}
```

### Configuración de GitHub

Para la integración con GitHub, hay un archivo de configuración separado en `config/git_sync_config.json`:

```json
{
  "github_token": "",
  "repo_owner": "PGQ888",
  "repo_name": "talentekia-agentes-ia",
  "create_pull_requests": true,
  "default_branch": "main",
  "auto_merge": false,
  "commit_message_prefix": "[Auto-mejora] ",
  "labels_for_pr": ["auto-improvement", "maintenance"]
}
```

Deberás configurar tu token de acceso personal de GitHub para habilitar la creación automática de pull requests.

## Uso

### Ejecutar el análisis manualmente

```bash
python scripts/auto_improvement.py
```

Este comando ejecutará el análisis completo según la configuración y generará un reporte en la carpeta `reports`.

### Programar ejecución automática

```bash
python scripts/schedule_auto_improvement.py [opciones]
```

Opciones disponibles:

- `--frequency {daily,weekly,monthly}`: Establece la frecuencia de ejecución
- `--remove`: Elimina la tarea programada
- `--run-now`: Ejecuta el análisis inmediatamente después de programarlo

Ejemplos:

```bash
# Programar ejecución diaria
python scripts/schedule_auto_improvement.py --frequency daily

# Programar ejecución semanal (por defecto)
python scripts/schedule_auto_improvement.py

# Programar ejecución mensual y ejecutar ahora
python scripts/schedule_auto_improvement.py --frequency monthly --run-now

# Eliminar la tarea programada
python scripts/schedule_auto_improvement.py --remove
```

### Sincronizar mejoras con GitHub

```bash
python scripts/git_sync_improvements.py [opciones]
```

Opciones disponibles:

- `--setup`: Configurar credenciales de GitHub
- `--force`: Fuerza la sincronización aunque no haya cambios detectados
- `--no-push`: No hacer push de los cambios (sólo commit local)
- `--no-pr`: No crear pull request

Ejemplos:

```bash
# Configurar el token de GitHub
python scripts/git_sync_improvements.py --setup

# Sincronizar cambios y crear PR
python scripts/git_sync_improvements.py

# Sincronizar cambios sin crear PR
python scripts/git_sync_improvements.py --no-pr
```

Flujo de trabajo sugerido para automatización completa:

```bash
# Analizar, aplicar mejoras y sincronizar con GitHub en un solo paso
python scripts/auto_improvement.py && python scripts/git_sync_improvements.py
```

## Reportes

Los reportes se generan en formato Markdown y se guardan en `reports/auto_improvement_report.md`. Cada reporte incluye:

1. Análisis de dependencias obsoletas
2. Problemas de calidad de código detectados
3. Patrones de rendimiento problemáticos
4. Comandos sugeridos para aplicar las mejoras

## Aplicación automática de mejoras

Si habilita `auto_apply_safe_fixes` en la configuración, el sistema intentará aplicar automáticamente algunas mejoras consideradas seguras, como correcciones automáticas de ESLint.

## Estructura de archivos

```
talentek-ai-unified/
├── scripts/
│   ├── auto_improvement.py         # Script principal de análisis
│   ├── schedule_auto_improvement.py # Script para programar ejecución
│   └── git_sync_improvements.py    # Script para sincronizar con GitHub
├── config/
│   ├── auto_improvement_config.json # Configuración del análisis
│   └── git_sync_config.json        # Configuración de GitHub
├── reports/
│   └── auto_improvement_report.md  # Reportes generados
└── logs/
    ├── auto_improvement.log        # Registros de ejecución
    └── auto_improvement_error.log  # Errores durante la ejecución
```

## Personalización

### Reglas personalizadas

Puede añadir reglas personalizadas para detectar patrones específicos en su código modificando la sección `custom_rules` del archivo de configuración. Cada regla debe incluir un nombre, un patrón regex, una sugerencia y las extensiones de archivo a las que aplicar.

### Directorios ignorados

Modifique la sección `ignored_directories` para excluir directorios del análisis.

## Integración con CI/CD

Para integrar este sistema con un flujo de CI/CD, puede ejecutar el script de análisis y sincronización como parte de su pipeline:

```yaml
# Ejemplo para GitHub Actions
jobs:
  auto-improvement:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run auto improvement
        run: python scripts/auto_improvement.py
      - name: Sync with GitHub
        run: python scripts/git_sync_improvements.py
```

## Solución de problemas

Si encuentra algún problema con la ejecución de los scripts:

1. Verifique los archivos de registro en la carpeta `logs/`
2. Asegúrese de tener los permisos necesarios para programar tareas
3. Verifique que las herramientas de análisis (ESLint, Pylint) estén instaladas si desea usarlas
4. Para problemas con la sincronización de GitHub, verifique el token de acceso y los permisos

## Contribuir

Si desea contribuir al desarrollo de este sistema de auto-mejora, puede:

1. Añadir nuevas reglas de detección de patrones
2. Implementar soporte para herramientas adicionales de análisis estático
3. Mejorar la generación de reportes
4. Optimizar el rendimiento del análisis

---

© TalentekAI Unified - Sistema de Auto-Mejora