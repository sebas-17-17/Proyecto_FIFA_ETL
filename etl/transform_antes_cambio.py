"""
transform.py
-----------------------------------------
Calcula todos los KPIs del proyecto FIFA.
"""

import pandas as pd

from database import get_db1_engine
from database import get_db2_engine


# ============================================================
# OBTENER PARÁMETROS
# ============================================================

def obtener_parametros():

    engine = get_db2_engine()

    parametros = pd.read_sql(
        "SELECT nombre, valor FROM parametros",
        engine
    )

    return dict(
        zip(
            parametros["nombre"],
            parametros["valor"]
        )
    )


# ============================================================
# LEER DATASET
# ============================================================

def leer_dataset():

    engine = get_db1_engine()

    return pd.read_sql(
        "SELECT * FROM fifa_dataset",
        engine
    )


# ============================================================
# KPI 1 - RANKING HISTÓRICO
# ============================================================

def calcular_kpi1():

    parametros = obtener_parametros()

    top = int(parametros["top_n"])

    df = leer_dataset()

    # Agrupar por equipo para evitar equipos repetidos.
    # Se suman las victorias, empates y derrotas
    # de todas las ediciones disponibles.

    ranking = (
        df.groupby("team", as_index=False)
        .agg(
            wins=(
                "wins_last_4y",
                "sum"
            ),
            draws=(
                "draws_last_4y",
                "sum"
            ),
            losses=(
                "losses_last_4y",
                "sum"
            )
        )
    )

    ranking["matches"] = (
        ranking["wins"]
        + ranking["draws"]
        + ranking["losses"]
    )

    ranking["win_percentage"] = (
        ranking["wins"]
        / ranking["matches"]
        * 100
    ).round(2)

    return (
        ranking[
            [
                "team",
                "wins",
                "matches",
                "win_percentage"
            ]
        ]
        .sort_values(
            "wins",
            ascending=False
        )
        .head(top)
        .reset_index(drop=True)
    )


# ============================================================
# KPI 2 - OFENSIVA
# ============================================================

def calcular_kpi2():

    parametros = obtener_parametros()

    minimo = float(
        parametros["min_avg_goals"]
    )

    df = leer_dataset()

    # Agrupar por equipo para obtener
    # un promedio histórico consolidado.

    ofensiva = (
        df.groupby("team", as_index=False)
        .agg(
            goals_scored=(
                "goals_scored_last_4y",
                "sum"
            ),
            wins=(
                "wins_last_4y",
                "sum"
            ),
            draws=(
                "draws_last_4y",
                "sum"
            ),
            losses=(
                "losses_last_4y",
                "sum"
            )
        )
    )

    ofensiva["matches"] = (
        ofensiva["wins"]
        + ofensiva["draws"]
        + ofensiva["losses"]
    )

    ofensiva["avg_goals"] = (
        ofensiva["goals_scored"]
        / ofensiva["matches"]
    ).round(2)

    return (
        ofensiva[
            [
                "team",
                "avg_goals"
            ]
        ]
        .query(
            "avg_goals > @minimo"
        )
        .sort_values(
            "avg_goals",
            ascending=False
        )
        .reset_index(drop=True)
    )


# ============================================================
# KPI 3 - EVOLUCIÓN HISTÓRICA
# ============================================================

def calcular_kpi3():

    df = leer_dataset()

    return (
        df.groupby("version")
        .agg(
            total_goals=(
                "goals_scored_last_4y",
                "sum"
            ),
            avg_goals=(
                "goals_scored_last_4y",
                "mean"
            ),
            teams=(
                "team",
                "count"
            )
        )
        .reset_index()
        .sort_values("version")
    )


# ============================================================
# KPI 4 - RENDIMIENTO
# ============================================================

def calcular_kpi4():

    df = leer_dataset()

    # Consolidar resultados por equipo.

    rendimiento = (
        df.groupby("team", as_index=False)
        .agg(
            wins=(
                "wins_last_4y",
                "sum"
            ),
            draws=(
                "draws_last_4y",
                "sum"
            ),
            losses=(
                "losses_last_4y",
                "sum"
            )
        )
    )

    rendimiento["matches"] = (
        rendimiento["wins"]
        + rendimiento["draws"]
        + rendimiento["losses"]
    )

    rendimiento["performance_index"] = (
        (
            rendimiento["wins"] * 3
            + rendimiento["draws"]
        )
        / rendimiento["matches"]
    ).round(3)

    return (
        rendimiento[
            [
                "team",
                "performance_index"
            ]
        ]
        .sort_values(
            "performance_index",
            ascending=False
        )
        .head(5)
        .reset_index(drop=True)
    )
