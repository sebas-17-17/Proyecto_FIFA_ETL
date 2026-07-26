"""
main.py
-----------------------------------------
Orquestador principal del proceso ETL.

Flujo:

1. Extract
2. Transform
3. Load

El proceso está diseñado para ser
reutilizado manualmente o desde Airflow.
"""
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

from extract import extract

from transform import (
    calcular_kpi1,
    calcular_kpi2,
    calcular_kpi3,
    calcular_kpi4,
)

from load import (
    guardar_kpi1,
    guardar_kpi2,
    guardar_kpi3,
    guardar_kpi4,
)


# ============================================================
# PROCESO ETL
# ============================================================

def ejecutar_etl():

    print("\n")
    print("=" * 60)
    print("PROYECTO FIFA - PROCESO ETL")
    print("=" * 60)

    # --------------------------------------------------------
    # EXTRACT
    # --------------------------------------------------------

    print("\n[1/3] EXTRACT")

    if not extract():

        print(
            "\n[ERROR] El proceso Extract falló."
        )

        return False

    # --------------------------------------------------------
    # TRANSFORM
    # --------------------------------------------------------

    print("\n[2/3] TRANSFORM")

    try:

        print(
            "[TRANSFORM] Calculando KPI 1..."
        )

        kpi1 = calcular_kpi1()

        print(
            "[TRANSFORM] Calculando KPI 2..."
        )

        kpi2 = calcular_kpi2()

        print(
            "[TRANSFORM] Calculando KPI 3..."
        )

        kpi3 = calcular_kpi3()

        print(
            "[TRANSFORM] Calculando KPI 4..."
        )

        kpi4 = calcular_kpi4()

    except Exception as e:

        print(
            "\n[ERROR] Error durante Transform:"
        )

        print(e)

        return False

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    print("\n[3/3] LOAD")

    try:

        guardar_kpi1(kpi1)

        guardar_kpi2(kpi2)

        guardar_kpi3(kpi3)

        guardar_kpi4(kpi4)

    except Exception as e:

        print(
            "\n[ERROR] Error durante Load:"
        )

        print(e)

        return False

    # --------------------------------------------------------
    # FINALIZACIÓN
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("ETL FINALIZADO CORRECTAMENTE")
    print("=" * 60)

    return True


# ============================================================
# EJECUCIÓN MANUAL
# ============================================================

if __name__ == "__main__":

    resultado = ejecutar_etl()

    if resultado:

        print(
            "\nResultado final: SUCCESS"
        )

    else:

        print(
            "\nResultado final: FAILED"
        )
