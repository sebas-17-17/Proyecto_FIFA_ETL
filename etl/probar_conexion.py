from database import get_db1_engine
from database import get_db2_engine

try:

    engine1 = get_db1_engine()

    with engine1.connect():
        print("✅ Conectado a db_fifa_negocio")

except Exception as e:
    print("❌ Error Base Negocio")
    print(e)

try:

    engine2 = get_db2_engine()

    with engine2.connect():
        print("✅ Conectado a db_fifa_parametros")

except Exception as e:
    print("❌ Error Base Parámetros")
    print(e)
