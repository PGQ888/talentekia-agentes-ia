#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests básicos para el proyecto TalentekIA
"""

import unittest
import os
import sys

# Añadir el directorio raíz al path para importar módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestBasic(unittest.TestCase):
    """Pruebas básicas para verificar la estructura del proyecto."""

    def test_project_structure(self):
        """Verifica que existan los directorios principales del proyecto."""
        self.assertTrue(os.path.isdir('src'), "El directorio 'src' debe existir")
        self.assertTrue(os.path.isdir('src/agents'), "El directorio 'src/agents' debe existir")

    def test_imports(self):
        """Verifica que se puedan importar los módulos principales."""
        try:
            from src.agents.base_agent import BaseAgent
            self.assertTrue(True, "Se pudo importar BaseAgent correctamente")
        except ImportError as e:
            self.fail(f"No se pudo importar BaseAgent: {e}")


if __name__ == '__main__':
    unittest.main()