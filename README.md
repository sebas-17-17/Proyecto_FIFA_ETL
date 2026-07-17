# ⚽ Proyecto FIFA ETL + Dashboard BI + Airflow

Proyecto desarrollado para implementar un proceso **ETL (Extract, Transform, Load)** utilizando Python y MySQL, automatizado con Apache Airflow y visualizado mediante un Dashboard desarrollado en Dash.

---

# 📌 Objetivo

Extraer información de un dataset FIFA, calcular indicadores KPI relevantes y visualizarlos mediante un Dashboard interactivo.

---

# 🏗 Arquitectura del Proyecto

```
                Dataset FIFA
                     │
                     ▼
          Base de Negocio (MySQL)
                     │
                     ▼
              ETL (Python)
                     │
                     ▼
       Base de Parámetros (MySQL)
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    Dashboard Dash         Apache Airflow
```

---

# 📂 Estructura del Proyecto

```
Proyecto_FIFA/

├── airflow/
│   └── DAG del proyecto
│
├── config/
│   └── .env
│
├── dashboard/
│   └── app.py
│
├── docs/
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── database.py
│   └── main.py
│
├── sql/
│
├── requirements.txt
│
└── README.md
```

---

# 🛠 Tecnologías Utilizadas

- Python 3
- MySQL
- SQLAlchemy
- Pandas
- Dash
- Plotly
- Apache Airflow

---

# 📊 KPIs Implementados

### KPI 1
Ranking de equipos con mayor porcentaje de victorias.

### KPI 2
Promedio de goles anotados por equipo.

### KPI 3
Evolución histórica del promedio de goles por versión FIFA.

### KPI 4
Índice de rendimiento de los mejores equipos.

---

# ⚙ Requisitos

- Python 3.10 o superior
- MySQL
- Apache Airflow
- Git

---

# 📦 Instalación

## Clonar el repositorio

```bash
git clone https://github.com/Kayden335/Proyecto_FIFA_ETL.git
cd Proyecto_FIFA
```

---

## Crear entorno virtual

```bash
python3 -m venv venv
```

Activar:

Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuración

Crear el archivo:

```
config/.env
```

Ejemplo:

```env
DB1_HOST=localhost
DB1_PORT=3306
DB1_NAME=db_fifa_negocio
DB1_USER=fifa_user
DB1_PASS=Fifa2026!

DB2_HOST=localhost
DB2_PORT=3306
DB2_NAME=db_fifa_parametros
DB2_USER=fifa_user
DB2_PASS=Fifa2026!
```

---

# 🗄 Base de Datos

Crear las siguientes bases:

- db_fifa_negocio
- db_fifa_parametros

Importar el dataset FIFA en la base de negocio.

---

# ▶ Ejecutar el ETL

```bash
cd etl
python main.py
```

Este proceso:

- Extrae el dataset.
- Calcula los KPIs.
- Guarda los resultados en la base de parámetros.

---

# 📈 Ejecutar Dashboard

```bash
cd dashboard
python app.py
```

Abrir:

```
http://localhost:8050
```

---

# ⏰ Ejecutar Airflow

Inicializar Airflow.

Iniciar Scheduler:

```bash
airflow scheduler
```

Iniciar Webserver:

```bash
airflow webserver
```

Abrir:

```
http://localhost:8080
```

Ejecutar el DAG para automatizar el ETL.

---

# 📸 Resultados

El Dashboard permite visualizar:

- Ranking de equipos.
- Promedio de goles.
- Índice de rendimiento.
- Evolución histórica.

Toda la información se actualiza automáticamente después de ejecutar el ETL.

---

# 👨‍💻 Autor

Proyecto desarrollado como parte de la asignatura de Inteligencia de Negocios.

Autor:
**Kayden335**

---

# 📄 Licencia

Proyecto desarrollado con fines académicos.
