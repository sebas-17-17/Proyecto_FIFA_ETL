"""
main.py
--------------------------------------
Orquestador principal del ETL.
"""

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


print("=" * 60)
print("PROYECTO FIFA ETL")
print("=" * 60)

# EXTRACT
if extract():

    print("\nCalculando KPIs...")

    kpi1 = calcular_kpi1()
    kpi2 = calcular_kpi2()
    kpi3 = calcular_kpi3()
    kpi4 = calcular_kpi4()

    print("Guardando resultados...")

    guardar_kpi1(kpi1)
    guardar_kpi2(kpi2)
    guardar_kpi3(kpi3)
    guardar_kpi4(kpi4)

    print("\nETL FINALIZADO CORRECTAMENTE")

else:

    print("El proceso ETL terminó con errores.")
