"""
transform.py
-----------------------------------------
Calcula todos los KPIs del proyecto.
"""

import pandas as pd
from database import get_db1_engine
from database import get_db2_engine


def obtener_parametros():

    engine = get_db2_engine()

    parametros = pd.read_sql(
        "SELECT nombre,valor FROM parametros",
        engine
    )

    return dict(zip(parametros.nombre, parametros.valor))


def leer_dataset():

    engine = get_db1_engine()

    return pd.read_sql(
        "SELECT * FROM fifa_dataset",
        engine
    )


def calcular_kpi1():

    parametros = obtener_parametros()

    top = int(parametros["top_n"])

    df = leer_dataset()

    df["matches"] = (
        df["wins_last_4y"]
        + df["draws_last_4y"]
        + df["losses_last_4y"]
    )

    df["win_percentage"] = (
        df["wins_last_4y"]
        / df["matches"]
        * 100
    ).round(2)

    kpi = (
        df[
            [
                "team",
                "wins_last_4y",
                "matches",
                "win_percentage",
            ]
        ]
        .sort_values(
            "wins_last_4y",
            ascending=False,
        )
        .head(top)
    )

    return kpi.rename(
        columns={
            "wins_last_4y": "wins"
        }
    )


def calcular_kpi2():

    parametros = obtener_parametros()

    minimo = float(parametros["min_avg_goals"])

    df = leer_dataset()

    partidos = (
        df["wins_last_4y"]
        + df["draws_last_4y"]
        + df["losses_last_4y"]
    )

    df["avg_goals"] = (
        df["goals_scored_last_4y"]
        / partidos
    ).round(2)

    return (
        df[
            ["team", "avg_goals"]
        ]
        .query("avg_goals>@minimo")
        .sort_values(
            "avg_goals",
            ascending=False
        )
    )


def calcular_kpi3():

    df = leer_dataset()

    return (
        df.groupby("version")
        .agg(
            total_goals=(
                "goals_scored_last_4y",
                "sum",
            ),
            avg_goals=(
                "goals_scored_last_4y",
                "mean",
            ),
            teams=(
                "team",
                "count",
            ),
        )
        .reset_index()
    )


def calcular_kpi4():

    df = leer_dataset()

    partidos = (
        df["wins_last_4y"]
        + df["draws_last_4y"]
        + df["losses_last_4y"]
    )

    df["performance_index"] = (
        (
            df["wins_last_4y"] * 3
            + df["draws_last_4y"]
        )
        / partidos
    ).round(3)

    return (
        df[
            [
                "team",
                "performance_index",
            ]
        ]
        .sort_values(
            "performance_index",
            ascending=False,
        )
        .head(5)
    )

