#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Optimizador para Mac con Apple Silicon (M1/M2/M3)

Este módulo configura automáticamente el entorno para optimizar el rendimiento
de TalentekIA en dispositivos Mac con Apple Silicon.
"""

import os
import platform
import sys
import subprocess
import logging
from typing import Dict, Optional, List, Tuple, Any
import json
import psutil

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("M2Optimizer")


class M2Optimizer:
    """Clase para optimizar el rendimiento en Mac con Apple Silicon (M1/M2/M3)."""

    def __init__(self) -> None:
        """Inicializa el optimizador."""
        self.is_apple_silicon = self._check_apple_silicon()
        self.env_vars: Dict[str, str] = {}
        self.original_env: Dict[str, str] = dict(os.environ)
        self.optimizations_applied = False

    def _check_apple_silicon(self) -> bool:
        """Verifica si el sistema es Mac con Apple Silicon.

        Returns:
            bool: True si es Mac con Apple Silicon, False en caso contrario.
        """
        return platform.system() == "Darwin" and platform.machine() == "arm64"

    def _load_env_file(self, env_file: str = ".env.m2") -> Dict[str, str]:
        """Carga variables de entorno desde un archivo.

        Args:
            env_file: Ruta al archivo de variables de entorno.

        Returns:
            Dict[str, str]: Diccionario con las variables de entorno.
        """
        env_vars = {}
        try:
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
            logger.info(f"Cargadas {len(env_vars)} variables de entorno desde {env_file}")
        except Exception as e:
            logger.warning(f"Error al cargar el archivo de entorno {env_file}: {e}")
        return env_vars

    def _get_optimal_thread_count(self) -> int:
        """Determina el número óptimo de hilos para paralelismo.

        Returns:
            int: Número óptimo de hilos.
        """
        cpu_count = psutil.cpu_count(logical=True)
        physical_cores = psutil.cpu_count(logical=False)
        
        # En Apple Silicon, queremos dejar algunos núcleos libres para el sistema
        if self.is_apple_silicon:
            # Usar 75% de los núcleos físicos para evitar sobrecalentamiento
            optimal = max(1, int(physical_cores * 0.75))
        else:
            # En otros sistemas, usar la mitad de los núcleos lógicos
            optimal = max(1, cpu_count // 2)
            
        return optimal

    def _get_memory_settings(self) -> Dict[str, str]:
        """Determina la configuración óptima de memoria.

        Returns:
            Dict[str, str]: Configuración de memoria.
        """
        total_memory = psutil.virtual_memory().total / (1024 * 1024 * 1024)  # GB
        
        # Ajustar configuración según la memoria disponible
        if total_memory >= 32:
            # Para sistemas con mucha RAM (32GB+)
            return {
                "PYTORCH_CUDA_ALLOC_CONF": "max_split_size_mb:1024",
                "TALENTEK_BATCH_SIZE": "32",
            }
        elif total_memory >= 16:
            # Para sistemas con RAM media (16GB)
            return {
                "PYTORCH_CUDA_ALLOC_CONF": "max_split_size_mb:512",
                "TALENTEK_BATCH_SIZE": "16",
            }
        else:
            # Para sistemas con poca RAM (<16GB)
            return {
                "PYTORCH_CUDA_ALLOC_CONF": "max_split_size_mb:256",
                "TALENTEK_BATCH_SIZE": "8",
            }

    def get_metal_info(self) -> Dict[str, Any]:
        """Obtiene información sobre Metal en macOS.

        Returns:
            Dict[str, Any]: Información sobre Metal.
        """
        if not self.is_apple_silicon:
            return {"error": "No es un sistema Mac con Apple Silicon"}
            
        try:
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType", "-json"],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            return data
        except Exception as e:
            logger.error(f"Error al obtener información de Metal: {e}")
            return {"error": str(e)}

    def optimize(self) -> bool:
        """Aplica optimizaciones para Mac con Apple Silicon.

        Returns:
            bool: True si las optimizaciones se aplicaron correctamente.
        """
        if not self.is_apple_silicon:
            logger.warning("Este sistema no es Mac con Apple Silicon. No se aplicarán optimizaciones.")
            return False
            
        # Cargar variables de entorno predefinidas
        self.env_vars = self._load_env_file()
        
        # Ajustar variables según el hardware específico
        thread_count = self._get_optimal_thread_count()
        memory_settings = self._get_memory_settings()
        
        # Actualizar variables de paralelismo
        parallel_vars = {
            "OMP_NUM_THREADS": str(thread_count),
            "MKL_NUM_THREADS": str(thread_count),
            "OPENBLAS_NUM_THREADS": str(thread_count),
            "VECLIB_MAXIMUM_THREADS": str(thread_count),
            "NUMEXPR_NUM_THREADS": str(thread_count),
            "TALENTEK_MAX_WORKERS": str(thread_count),
        }
        
        # Combinar todas las configuraciones
        self.env_vars.update(parallel_vars)
        self.env_vars.update(memory_settings)
        
        # Aplicar las variables de entorno
        for key, value in self.env_vars.items():
            os.environ[key] = value
            
        logger.info(f"Optimizaciones para Mac M1/M2/M3 aplicadas ({len(self.env_vars)} variables configuradas)")
        logger.info(f"Configuración de paralelismo: {thread_count} hilos")
        
        self.optimizations_applied = True
        return True
        
    def restore_env(self) -> None:
        """Restaura las variables de entorno originales."""
        if self.optimizations_applied:
            os.environ.clear()
            os.environ.update(self.original_env)
            logger.info("Variables de entorno restauradas a su estado original")
            self.optimizations_applied = False
            
    def print_status(self) -> None:
        """Imprime el estado actual de las optimizaciones."""
        if not self.is_apple_silicon:
            print("\n🖥️  Sistema actual: No es Mac con Apple Silicon")
            print("⚠️  Las optimizaciones para M1/M2/M3 no están disponibles en este sistema")
            return
            
        print("\n🖥️  Sistema detectado: Mac con Apple Silicon (M1/M2/M3)")
        
        if self.optimizations_applied:
            print("✅ Optimizaciones aplicadas:")
            
            # Agrupar variables por categoría para mejor visualización
            categories = {
                "PyTorch/TensorFlow": ["PYTORCH_", "TF_", "XLA_"],
                "Paralelismo": ["OMP_", "MKL_", "OPENBLAS_", "VECLIB_", "NUMEXPR_"],
                "Caché": ["TRANSFORMERS_CACHE", "SENTENCE_TRANSFORMERS_HOME"],
                "TalentekIA": ["TALENTEK_"],
            }
            
            for category, prefixes in categories.items():
                vars_in_category = {k: v for k, v in self.env_vars.items() 
                                  if any(k.startswith(p) for p in prefixes)}
                if vars_in_category:
                    print(f"\n📋 {category}:")
                    for k, v in vars_in_category.items():
                        print(f"   {k} = {v}")
        else:
            print("⚠️  Optimizaciones disponibles pero no aplicadas")
            print("   Ejecute optimizer.optimize() para aplicar las optimizaciones")


def apply_optimizations() -> M2Optimizer:
    """Función de conveniencia para aplicar optimizaciones.
    
    Returns:
        M2Optimizer: Instancia del optimizador con las optimizaciones aplicadas.
    """
    optimizer = M2Optimizer()
    optimizer.optimize()
    optimizer.print_status()
    return optimizer


if __name__ == "__main__":
    print("🚀 TalentekIA - Optimizador para Mac M1/M2/M3")
    optimizer = apply_optimizations()
    
    # Si se ejecuta como script, mostrar información adicional
    if optimizer.is_apple_silicon:
        metal_info = optimizer.get_metal_info()
        if "error" not in metal_info:
            try:
                gpu_info = metal_info.get("SPDisplaysDataType", [{}])[0]
                print("\n🔧 Información de GPU:")
                print(f"   Modelo: {gpu_info.get('spdisplays_device-name', 'Desconocido')}")
                print(f"   Tipo: {gpu_info.get('spdisplays_type', 'Integrada')}")
                
                metal_support = gpu_info.get("spdisplays_metal", "No")
                print(f"   Soporte Metal: {metal_support}")
                
                if "spdisplays_vram" in gpu_info:
                    print(f"   VRAM: {gpu_info['spdisplays_vram']}")
            except Exception as e:
                print(f"\n⚠️  Error al procesar información de GPU: {e}")