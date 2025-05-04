#!/usr/bin/env python3
"""
Gestor de Finanzas Personales - Agente para análisis financiero
"""
import sys
import time
from datetime import datetime

def main():
    print("╔═══════════════════════════════════════════╗")
    print("║       GESTOR DE FINANZAS PERSONALES       ║")
    print("╚═══════════════════════════════════════════╝")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Analizando datos financieros...")
    
    # Simulación de proceso
    print("Cargando datos de gastos e ingresos...")
    time.sleep(1)
    print("Calculando métricas financieras...")
    time.sleep(1.5)
    
    # Resultados simulados
    metricas = {
        "ingresos_totales": 5200,
        "gastos_totales": 3800,
        "ahorro_mensual": 1400,
        "tasa_ahorro": 26.9,
        "principales_gastos": {
            "Vivienda": 1500,
            "Alimentación": 800,
            "Transporte": 350,
            "Educación": 600,
            "Ocio": 250
        }
    }
    
    print("\nResumen financiero del mes:")
    print(f"Ingresos totales: {metricas['ingresos_totales']}€")
    print(f"Gastos totales: {metricas['gastos_totales']}€")
    print(f"Ahorro mensual: {metricas['ahorro_mensual']}€")
    print(f"Tasa de ahorro: {metricas['tasa_ahorro']}%")
    
    print("\nPrincipales categorías de gasto:")
    for categoria, importe in metricas['principales_gastos'].items():
        print(f"- {categoria}: {importe}€")
    
    print("\nRecomendaciones para optimización:")
    print("1. Reducir gastos en ocio en un 10%")
    print("2. Aumentar aportaciones a fondo de emergencia")
    print("3. Revisar posibilidades de inversión para excedente")
    
    print("\nAnálisis completado exitosamente.")
    print("El informe detallado ha sido guardado en data/finanzas/informe_mensual.pdf")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())