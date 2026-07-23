"""
extract.py
-----------------------------------------
Extrae los datos desde el archivo CSV
y los carga en la base de datos de negocio.

El proceso es idempotente:
antes de cargar los datos nuevos,
se elimina el contenido anterior de la tabla
fifa_dataset.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from database import get_db1_engine


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "train.csv"


# ============================================================
# EXTRACT
# ============================================================

def extract():

    try:

        print("\n" + "=" * 60)
        print("[EXTRACT] INICIANDO EXTRACCIÓN")
        print("=" * 60)

        # ----------------------------------------------------
        # VALIDAR CSV
        # ----------------------------------------------------

        if not CSV_FILE.exists():

            raise FileNotFoundError(
                f"No se encontró el archivo CSV: {CSV_FILE}"
            )

        print(f"[EXTRACT] Archivo encontrado: {CSV_FILE}")

        # ----------------------------------------------------
        # LEER CSV
        # ----------------------------------------------------

        df = pd.read_csv(CSV_FILE)

        if df.empty:

            raise ValueError(
                "El archivo CSV está vacío."
            )

        print(
            f"[EXTRACT] Registros encontrados: "
            f"{len(df)}"
        )

        # ----------------------------------------------------
        # CONECTAR A BASE DE NEGOCIO
        # ----------------------------------------------------

        engine = get_db1_engine()

        # ----------------------------------------------------
        # LIMPIAR TABLA DESTINO
        # ----------------------------------------------------

        print(
            "[EXTRACT] Eliminando datos anteriores "
            "de fifa_dataset..."
        )

        with engine.begin() as connection:

            connection.execute(
                text(
                    "DROP TABLE IF EXISTS fifa_dataset"
                )
            )

        # ----------------------------------------------------
        # CARGAR NUEVOS DATOS
        # ----------------------------------------------------

        print(
            "[EXTRACT] Cargando nuevos datos..."
        )

        df.to_sql(
            "fifa_dataset",
            con=engine,
            if_exists="replace",
            index=False
        )

        print(
            "[EXTRACT] Dataset cargado correctamente."
        )

        print(
            f"[EXTRACT] Registros cargados: "
            f"{len(df)}"
        )

        return True

    except Exception as e:

        print(
            "\n[ERROR] Error durante Extract:"
        )

        print(e)

        return False
