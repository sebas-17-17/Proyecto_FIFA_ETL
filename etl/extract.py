"""
extract.py
-----------------------------------------
Extrae el dataset CSV y lo carga en la
base de datos de negocio.
"""

import pandas as pd
from database import get_db1_engine


def extract():

    try:

        print("\n[EXTRACT] Leyendo dataset...")

        df = pd.read_csv("../data/train.csv")

        print(f"Registros: {len(df)}")

        engine = get_db1_engine()

        df.to_sql(
            "fifa_dataset",
            con=engine,
            if_exists="replace",
            index=False
        )

        print("Dataset cargado correctamente.")

        return True

    except Exception as e:

        print("Error en Extract")

        print(e)

        return False
