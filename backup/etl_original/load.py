"""
load.py
--------------------------------------
Guarda los KPIs en la base de parámetros.
"""

from database import get_db2_engine


engine = get_db2_engine()


def guardar_kpi1(df):

    df.to_sql(
        "kpi_ranking",
        engine,
        if_exists="replace",
        index=False,
    )


def guardar_kpi2(df):

    df.to_sql(
        "kpi_ofensiva",
        engine,
        if_exists="replace",
        index=False,
    )


def guardar_kpi3(df):

    df.to_sql(
        "kpi_evolucion",
        engine,
        if_exists="replace",
        index=False,
    )


def guardar_kpi4(df):

    df.to_sql(
        "kpi_rendimiento",
        engine,
        if_exists="replace",
        index=False,
    )
