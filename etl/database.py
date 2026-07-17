"""
database.py
--------------------
Módulo encargado de crear las conexiones a las bases de datos.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar variables del archivo .env
load_dotenv("../config/.env")


def get_db1_engine():
    """
    Conexión a la Base de Negocio
    """
    host = os.getenv("DB1_HOST")
    port = os.getenv("DB1_PORT")
    user = os.getenv("DB1_USER")
    password = os.getenv("DB1_PASS")
    database = os.getenv("DB1_NAME")

    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )


def get_db2_engine():
    """
    Conexión a la Base de Parámetros
    """
    host = os.getenv("DB2_HOST")
    port = os.getenv("DB2_PORT")
    user = os.getenv("DB2_USER")
    password = os.getenv("DB2_PASS")
    database = os.getenv("DB2_NAME")

    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )
