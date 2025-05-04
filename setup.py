"""
Script de instalación para TalentekIA
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="talentekia",
    version="0.1.0",
    author="Pablo Giráldez",
    author_email="pablo@talentek.es",
    description="Plataforma unificada de agentes de IA personalizados",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PGQ888/talentek-ia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "talentekia=src.interface.streamlit_app:main",
        ],
    },
)