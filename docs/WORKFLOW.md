# Flujo de Trabajo de Desarrollo para TalentekIA

Este documento describe el flujo de trabajo recomendado para el desarrollo y contribución al repositorio unificado de TalentekIA.

## Estructura de Ramas

El repositorio sigue un flujo de trabajo basado en GitFlow simplificado:

- **main**: Rama principal que contiene código estable y listo para producción
- **develop**: Rama de desarrollo donde se integran las nuevas características
- **feature/nombre-caracteristica**: Ramas para el desarrollo de nuevas características
- **fix/nombre-error**: Ramas para correcciones de errores
- **release/version**: Ramas para preparar nuevas versiones

## Proceso de Desarrollo

### 1. Iniciar una nueva característica

Para comenzar a trabajar en una nueva característica:

```bash
# Asegúrate de estar en la rama develop actualizada
git checkout develop
git pull origin develop

# Crea una nueva rama para tu característica
git checkout -b feature/nombre-caracteristica

# Desarrolla la característica...
```

### 2. Desarrollo de la característica

Durante el desarrollo:

- Realiza commits frecuentes con mensajes descriptivos
- Sigue las convenciones de código del proyecto
- Asegúrate de que tu código esté bien documentado
- Escribe pruebas para las nuevas funcionalidades

### 3. Integrar la característica

Cuando la característica esté completa:

```bash
# Actualiza tu rama con los últimos cambios de develop
git checkout develop
git pull origin develop
git checkout feature/nombre-caracteristica
git merge develop

# Resuelve cualquier conflicto si es necesario
# Ejecuta las pruebas para asegurarte de que todo funciona
```

### 4. Crear un Pull Request

- Sube tu rama a GitHub:
  ```bash
  git push origin feature/nombre-caracteristica
  ```

- Crea un Pull Request en GitHub desde tu rama `feature/nombre-caracteristica` a `develop`
- Describe claramente los cambios realizados
- Solicita revisión de código

### 5. Revisión y Merge

- Otros desarrolladores revisarán tu código
- Realiza los cambios solicitados si es necesario
- Una vez aprobado, el Pull Request se fusionará en `develop`

### 6. Lanzamiento

Cuando se acumule suficiente funcionalidad en `develop` para un lanzamiento:

```bash
# Crear una rama de lanzamiento
git checkout develop
git checkout -b release/vX.Y.Z

# Realizar ajustes finales, actualizar versiones, etc.
# Ejecutar pruebas finales

# Fusionar en main y develop
git checkout main
git merge release/vX.Y.Z
git tag -a vX.Y.Z -m "Versión X.Y.Z"
git push origin main --tags

git checkout develop
git merge release/vX.Y.Z
git push origin develop

# Eliminar la rama de lanzamiento
git branch -d release/vX.Y.Z
```

## Convenciones de Código

### Estilo de Código

- Sigue PEP 8 para código Python
- Utiliza nombres descriptivos para variables, funciones y clases
- Documenta todas las funciones y clases con docstrings
- Mantén las líneas de código con un máximo de 100 caracteres

### Mensajes de Commit

Utiliza mensajes de commit claros y descriptivos siguiendo el formato:

```
tipo(alcance): descripción corta

Descripción más detallada si es necesario.
```

Donde `tipo` puede ser:
- **feat**: Nueva característica
- **fix**: Corrección de error
- **docs**: Cambios en documentación
- **style**: Cambios que no afectan al significado del código (espacios, formato, etc.)
- **refactor**: Refactorización de código
- **test**: Adición o corrección de pruebas
- **chore**: Cambios en el proceso de construcción, herramientas, etc.

### Ejemplo:

```
feat(linkedin-agent): añadir filtrado por ubicación

- Implementa filtrado de ofertas por ubicación geográfica
- Añade pruebas para el nuevo filtro
- Actualiza documentación con la nueva funcionalidad
```

## Herramientas de Desarrollo

### Formateo de Código

Utiliza `black` para formatear automáticamente el código:

```bash
# Instalar black
pip install black

# Formatear un archivo
black archivo.py

# Formatear todo el proyecto
black .
```

### Linting

Utiliza `flake8` para verificar la calidad del código:

```bash
# Instalar flake8
pip install flake8

# Verificar un archivo
flake8 archivo.py

# Verificar todo el proyecto
flake8
```

### Pruebas

Utiliza `pytest` para ejecutar las pruebas:

```bash
# Instalar pytest
pip install pytest

# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas específicas
pytest tests/test_specific.py
```

## Optimizaciones para Mac M2

Al desarrollar en Mac con Apple Silicon (M1/M2):

1. Asegúrate de utilizar las variables de entorno específicas para M2:
   ```bash
   export PYTORCH_ENABLE_MPS_FALLBACK=1
   export TF_ENABLE_ONEDNN_OPTS=0
   ```

2. Utiliza el modo optimizado para M2 cuando sea posible:
   ```bash
   ./start_talentek.sh
   # Selecciona la opción 6: Modo optimizado para Mac M2
   ```

3. Verifica que las nuevas características funcionen correctamente en arquitectura arm64.

## Integración Continua

El repositorio utiliza GitHub Actions para automatizar las pruebas y verificación de código:

- Las pruebas se ejecutan automáticamente en cada push y pull request
- El formateo y linting se verifican automáticamente
- Los resultados se muestran en la página de pull request

Asegúrate de que tu código pase todas las verificaciones antes de solicitar una revisión.