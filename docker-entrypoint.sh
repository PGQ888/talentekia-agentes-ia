#!/bin/bash
set -e

# Detectar si estamos en un Mac con Apple Silicon
if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "arm64" ]; then
    echo "🚀 Detectado Mac con Apple Silicon (M1/M2/M3)"
    
    # Configurar variables de entorno optimizadas para M1/M2/M3
    export OPENBLAS_NUM_THREADS=4
    export MKL_NUM_THREADS=4
    export OMP_NUM_THREADS=4
    export VECLIB_MAXIMUM_THREADS=4
    export NUMEXPR_NUM_THREADS=4
    export PYTORCH_ENABLE_MPS_FALLBACK=1
    
    # Configuración de memoria para PyTorch/TensorFlow
    export PYTORCH_CUDA_ALLOC_CONF="max_split_size_mb:512"
    
    echo "✅ Entorno optimizado para Apple Silicon"
fi

# Ejecutar el comando proporcionado
exec "$@"