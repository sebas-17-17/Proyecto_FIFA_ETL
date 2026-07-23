"""
database.py
-----------------------------------------
Gestiona las conexiones a las bases de datos
del proyecto FIFA.

DB1 = Base de datos de negocio
DB2 = Base de datos de parámetros y KPIs
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# UBICACIÓN DEL PROYECTO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / "config" / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# CREAR CONEXIÓN
# ============================================================

def _crear_engine(prefix):
    """
    Crea una conexión SQLAlchemy utilizando las variables
    de configuración correspondientes a una base de datos.
    """

    host = os.getenv(f"{prefix}_HOST")
    port = os.getenv(f"{prefix}_PORT")
    user = os.getenv(f"{prefix}_USER")
    password = os.getenv(f"{prefix}_PASS")
    database = os.getenv(f"{prefix}_NAME")

    variables = {
        "HOST": host,
        "PORT": port,
        "USER": user,
        "PASS": password,
        "NAME": database,
    }

    faltantes = [
        nombre
        for nombre, valor in variables.items()
        if not valor
    ]

    if faltantes:
        raise ValueError(
            f"Faltan variables de configuración para {prefix}: "
            f"{', '.join(faltantes)}"
        )

    return create_engine(
        f"mysql+pymysql://"
        f"{user}:{password}@{host}:{port}/{database}"
    )


# ============================================================
# BASE DE DATOS DE NEGOCIO
# ============================================================

def get_db1_engine():
    """
    Retorna la conexión a la base de datos de negocio.
    """

    return _crear_engine("DB1")


# ============================================================
# BASE DE DATOS DE PARÁMETROS
# ============================================================

def get_db2_engine():
    """
    Retorna la conexión a la base de datos de parámetros.
    """

    return _crear_engine("DB2")
