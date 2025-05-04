#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for TalentekIA.
"""

import os
import re
from setuptools import setup, find_packages

# Leer la versión desde un archivo de versión
with open(os.path.join('src', '__init__.py'), 'r') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.1.0'  # Versión por defecto si no se encuentra

# Leer el contenido del README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Dependencias principales
REQUIRED = [
    'python-dotenv>=1.0.0',
    'requests>=2.31.0',
    'pandas>=2.0.3',
    'numpy>=1.26.0',
    'toml>=0.10.2',
    'pydantic>=2.3.0,<3.0.0',
    'matplotlib>=3.7.2',
    'seaborn>=0.12.2',
    'openpyxl>=3.1.2',
    'beautifulsoup4>=4.12.2',
    'lxml>=4.9.3',
    'scikit-learn>=1.3.0',
    'nltk>=3.8.0',
    'qdrant-client>=1.6.0',
    'sentence-transformers>=2.2.2',
    'torch>=2.0.1',
    'transformers>=4.31.0',
    'langchain>=0.0.267',
    'langchain-openai>=0.0.5',
    'openai>=1.0.0',
    'huggingface-hub>=0.19.0',
    'selenium>=4.11.2',
    'webdriver-manager>=4.0.0',
    'python-linkedin-v2>=0.9.4',
    'streamlit>=1.25.0',
    'plotly>=5.16.0',
    'schedule>=1.2.0',
    'aiohttp>=3.8.5',
    'asyncio>=3.4.3',
    'apscheduler>=3.10.0',
    'gitpython>=3.1.30',
    'pygithub>=1.59.0',
    'psutil>=5.9.0',
    'GPUtil>=1.4.0',
    'tqdm>=4.66.1',
    'colorama>=0.4.6',
    'markdown>=3.4.4',
]

# Dependencias extras
EXTRAS = {
    'dev': [
        'pytest>=7.3.1',
        'black>=23.3.0',
        'isort>=5.12.0',
        'flake8>=6.0.0',
    ],
    'docs': [
        'sphinx>=7.0.0',
        'sphinx-rtd-theme>=1.3.0',
    ],
    'm2': [
        'tensorflow-macos>=2.12.0',
        'tensorflow-metal>=1.0.0',
    ],
}

setup(
    name='talentekia',
    version=version,
    description='Sistema de agentes de IA personalizados para automatización y análisis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pablo Giraldez',
    author_email='pablo@talentek.io',
    url='https://github.com/PGQ888/talentekia-agentes-ia',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    include_package_data=True,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    entry_points={
        'console_scripts': [
            'talentekia=src.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
)