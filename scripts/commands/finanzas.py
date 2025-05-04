#!/usr/bin/env python3
"""
Script para acceder a información financiera y generar reportes.
Este script es utilizado por el comando /finanzas en Anything LLM.
"""

import os
import sys
import json
import datetime
import argparse
import random  # Solo para generar datos de ejemplo

def generar_datos_ejemplo():
    """Genera datos financieros de ejemplo para demostración."""
    return {
        "ingresos": {
            "q1": round(random.uniform(50000, 150000), 2),
            "q2": round(random.uniform(60000, 170000), 2),
            "q3": round(random.uniform(70000, 190000), 2),
            "q4": round(random.uniform(80000, 210000), 2)
        },
        "gastos": {
            "q1": round(random.uniform(40000, 100000), 2),
            "q2": round(random.uniform(45000, 110000), 2),
            "q3": round(random.uniform(50000, 120000), 2),
            "q4": round(random.uniform(55000, 130000), 2)
        },
        "metricas": {
            "cac": round(random.uniform(100, 500), 2),
            "ltv": round(random.uniform(1000, 5000), 2),
            "churn": round(random.uniform(0.01, 0.1), 3),
            "mrr": round(random.uniform(10000, 50000), 2)
        }
    }

def main():
    """Función principal que genera reportes financieros."""
    parser = argparse.ArgumentParser(description="Accede a información financiera y genera reportes")
    parser.add_argument("--tipo", choices=["resumen", "detallado", "proyeccion", "metricas"], 
                      default="resumen", help="Tipo de reporte financiero")
    parser.add_argument("--periodo", choices=["mensual", "trimestral", "anual"], 
                      default="trimestral", help="Periodo del reporte")
    parser.add_argument("--formato", choices=["texto", "json"], 
                      default="texto", help="Formato de salida")
    
    args = parser.parse_args()
    
    print(f"💰 Generando reporte financiero - Tipo: {args.tipo}, Periodo: {args.periodo}")
    
    # En una implementación real, aquí se conectaría con APIs financieras o bases de datos
    # Por ahora, generamos datos de ejemplo
    datos = generar_datos_ejemplo()
    
    # Generar reporte según el tipo solicitado
    if args.tipo == "resumen":
        total_ingresos = sum(datos["ingresos"].values())
        total_gastos = sum(datos["gastos"].values())
        beneficio = total_ingresos - total_gastos
        margen = (beneficio / total_ingresos) * 100 if total_ingresos > 0 else 0
        
        if args.formato == "texto":
            reporte = f"""
📊 RESUMEN FINANCIERO {datetime.datetime.now().strftime('%Y')}

Ingresos Totales: {total_ingresos:.2f} €
Gastos Totales: {total_gastos:.2f} €
Beneficio Neto: {beneficio:.2f} €
Margen de Beneficio: {margen:.2f}%

Desglose por Trimestre:
- Q1: {datos["ingresos"]["q1"]:.2f} € (ingresos) / {datos["gastos"]["q1"]:.2f} € (gastos)
- Q2: {datos["ingresos"]["q2"]:.2f} € (ingresos) / {datos["gastos"]["q2"]:.2f} € (gastos)
- Q3: {datos["ingresos"]["q3"]:.2f} € (ingresos) / {datos["gastos"]["q3"]:.2f} € (gastos)
- Q4: {datos["ingresos"]["q4"]:.2f} € (ingresos) / {datos["gastos"]["q4"]:.2f} € (gastos)

Generado el {datetime.datetime.now().strftime('%d-%m-%Y')} a las {datetime.datetime.now().strftime('%H:%M:%S')}
"""
        else:  # json
            reporte = json.dumps({
                "resumen": {
                    "ingresos_totales": total_ingresos,
                    "gastos_totales": total_gastos,
                    "beneficio_neto": beneficio,
                    "margen_beneficio": margen
                },
                "desglose_trimestral": {
                    "q1": {"ingresos": datos["ingresos"]["q1"], "gastos": datos["gastos"]["q1"]},
                    "q2": {"ingresos": datos["ingresos"]["q2"], "gastos": datos["gastos"]["q2"]},
                    "q3": {"ingresos": datos["ingresos"]["q3"], "gastos": datos["gastos"]["q3"]},
                    "q4": {"ingresos": datos["ingresos"]["q4"], "gastos": datos["gastos"]["q4"]}
                },
                "generado": datetime.datetime.now().isoformat()
            }, indent=2)
    
    elif args.tipo == "metricas":
        if args.formato == "texto":
            reporte = f"""
🔍 MÉTRICAS FINANCIERAS CLAVE

CAC (Coste de Adquisición de Cliente): {datos["metricas"]["cac"]:.2f} €
LTV (Valor de Vida del Cliente): {datos["metricas"]["ltv"]:.2f} €
Ratio LTV/CAC: {datos["metricas"]["ltv"] / datos["metricas"]["cac"]:.2f}
Churn Rate: {datos["metricas"]["churn"] * 100:.2f}%
MRR (Ingresos Mensuales Recurrentes): {datos["metricas"]["mrr"]:.2f} €
ARR (Ingresos Anuales Recurrentes): {datos["metricas"]["mrr"] * 12:.2f} €

Generado el {datetime.datetime.now().strftime('%d-%m-%Y')} a las {datetime.datetime.now().strftime('%H:%M:%S')}
"""
        else:  # json
            reporte = json.dumps({
                "metricas": {
                    "cac": datos["metricas"]["cac"],
                    "ltv": datos["metricas"]["ltv"],
                    "ltv_cac_ratio": datos["metricas"]["ltv"] / datos["metricas"]["cac"],
                    "churn_rate": datos["metricas"]["churn"] * 100,
                    "mrr": datos["metricas"]["mrr"],
                    "arr": datos["metricas"]["mrr"] * 12
                },
                "generado": datetime.datetime.now().isoformat()
            }, indent=2)
    
    else:  # proyeccion o detallado
        reporte = "Tipo de reporte no implementado completamente en esta versión de demostración."
    
    # Imprimir reporte generado
    print("\n" + reporte + "\n")
    
    print("✅ Reporte financiero generado correctamente.")
    
    # En una implementación real, este reporte podría ser devuelto a Anything LLM
    # o guardado en un archivo para su posterior consulta

if __name__ == "__main__":
    main()