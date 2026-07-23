"""
load.py
-----------------------------------------
Carga los resultados de los KPIs en la
base de datos de parámetros.

Cada tabla KPI se reemplaza completamente
en cada ejecución del ETL, garantizando
que no se acumulen resultados antiguos.
"""

from database import get_db2_engine


# ============================================================
# CONEXIÓN
# ============================================================

engine = get_db2_engine()


# ============================================================
# FUNCIÓN GENERAL DE CARGA
# ============================================================

def guardar_kpi(df, tabla):

    if df is None:

        raise ValueError(
            f"El resultado de {tabla} es None."
        )

    if df.empty:

        print(
            f"[WARNING] {tabla} no tiene registros."
        )

        return

    print(
        f"[LOAD] Actualizando tabla {tabla}..."
    )

    df.to_sql(
        tabla,
        engine,
        if_exists="replace",
        index=False,
    )

    print(
        f"[LOAD] {tabla} actualizada correctamente."
    )

    print(
        f"[LOAD] Registros: {len(df)}"
    )


# ============================================================
# KPI 1
# ============================================================

def guardar_kpi1(df):

    guardar_kpi(
        df,
        "kpi_ranking"
    )


# ============================================================
# KPI 2
# ============================================================

def guardar_kpi2(df):

    guardar_kpi(
        df,
        "kpi_ofensiva"
    )


# ============================================================
# KPI 3
# ============================================================

def guardar_kpi3(df):

    guardar_kpi(
        df,
        "kpi_evolucion"
    )


# ============================================================
# KPI 4
# ============================================================

def guardar_kpi4(df):

    guardar_kpi(
        df,
        "kpi_rendimiento"
    )
