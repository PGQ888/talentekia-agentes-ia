# Usar imagen base optimizada para ARM64 (M1/M2/M3)
FROM --platform=linux/arm64 python:3.10-slim

# Configurar variables de entorno para optimización
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    # Optimizaciones para M1/M2/M3
    OPENBLAS_NUM_THREADS=4 \
    MKL_NUM_THREADS=4 \
    OMP_NUM_THREADS=4 \
    VECLIB_MAXIMUM_THREADS=4 \
    NUMEXPR_NUM_THREADS=4 \
    PYTORCH_ENABLE_MPS_FALLBACK=1

WORKDIR /app

# Instalar dependencias del sistema - minimizadas para lo esencial
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear y activar un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Actualizar pip y herramientas básicas
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copiar requirements primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Instalar el paquete en modo desarrollo
RUN pip install -e .

# Puerto para API/servicios web
EXPOSE 8000

# Script de entrada para configurar el entorno antes de ejecutar
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "-m", "src"]