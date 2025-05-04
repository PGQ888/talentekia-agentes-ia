# Configuración optimizada para Mac con Apple Silicon (M1/M2/M3)

# Variables de entorno para optimización de rendimiento
PYTORCH_ENABLE_MPS_FALLBACK=1
TF_ENABLE_ONEDNN_OPTS=0
XLA_FLAGS=--xla_gpu_cuda_data_dir=/opt/homebrew/opt/cuda

# Configuración de memoria y caché
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
TF_FORCE_GPU_ALLOW_GROWTH=true
TRANSFORMERS_CACHE=~/.cache/huggingface/transformers
SENTENCE_TRANSFORMERS_HOME=~/.cache/torch/sentence_transformers

# Configuración de paralelismo
OMP_NUM_THREADS=8
MKL_NUM_THREADS=8
OPENBLAS_NUM_THREADS=8
VECLIB_MAXIMUM_THREADS=8
NUMEXPR_NUM_THREADS=8

# Configuración de logging
TF_CPP_MIN_LOG_LEVEL=2
TOKENIZERS_PARALLELISM=true

# Configuración de API Keys
# IMPORTANTE: Reemplaza estos valores con tus propias claves API
OPENAI_API_KEY=tu_clave_api_aqui
ANTHROPIC_API_KEY=tu_clave_api_aqui
HUGGINGFACE_API_KEY=tu_clave_api_aqui
LINKEDIN_CLIENT_ID=tu_cliente_id_aqui
LINKEDIN_CLIENT_SECRET=tu_cliente_secreto_aqui

# Configuración específica de TalentekIA
TALENTEK_MODE=optimized
TALENTEK_LOG_LEVEL=INFO
TALENTEK_DATA_DIR=./data
TALENTEK_CONFIG_PATH=./config/talentek_config.toml
TALENTEK_USE_MPS=true
TALENTEK_BATCH_SIZE=16
TALENTEK_MAX_WORKERS=8