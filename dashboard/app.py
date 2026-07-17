from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://fifa_user:Fifa2026!@localhost:3306/db_fifa_parametros"
)

ranking = pd.read_sql("SELECT * FROM kpi_ranking", engine)
ofensiva = pd.read_sql("SELECT * FROM kpi_ofensiva", engine)
evolucion = pd.read_sql("SELECT * FROM kpi_evolucion", engine)
rendimiento = pd.read_sql("SELECT * FROM kpi_rendimiento", engine)

equipos = sorted(ranking["team"].dropna().unique())

app = Dash(__name__)
app.title = "Proyecto FIFA"

app.layout = html.Div(

    style={
        "backgroundColor": "#111111",
        "padding": "25px",
        "fontFamily": "Arial",
        "minHeight": "100vh"
    },

    children=[

        html.H1(
            "⚽ PROYECTO FIFA - DASHBOARD BI",
            style={
                "color": "white",
                "textAlign": "center",
                "marginBottom": "30px"
            }
        ),

        html.H3(
            "Seleccionar Equipo",
            style={"color": "white"}
        ),

        dcc.Dropdown(
            id="equipo",
            options=[{"label": x, "value": x} for x in equipos],
            value=equipos[0],
            clearable=False,
            searchable=True,
            style={
                "width": "55%",
                "color": "black",
                "marginBottom": "30px"
            }
        ),

        html.Div(

            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "25px"
            },

            children=[

                dcc.Graph(id="grafico_ranking"),
                dcc.Graph(id="grafico_ofensiva"),
                dcc.Graph(id="grafico_rendimiento"),
                dcc.Graph(id="grafico_evolucion"),

            ]

        )

    ]

)

@app.callback(

    Output("grafico_ranking", "figure"),
    Output("grafico_ofensiva", "figure"),
    Output("grafico_rendimiento", "figure"),
    Output("grafico_evolucion", "figure"),

    Input("equipo", "value")

)

def actualizar(equipo):

    r = ranking[ranking["team"] == equipo]
    o = ofensiva[ofensiva["team"] == equipo]
    p = rendimiento[rendimiento["team"] == equipo]

    fig1 = px.bar(
        r,
        x="team",
        y="win_percentage",
        text=r["win_percentage"].round(2),
        title="🏆 Porcentaje de Victorias"
    )
    fig1.update_traces(marker_color="#1f77b4", textposition="outside")

    fig2 = px.bar(
        o,
        x="team",
        y="avg_goals",
        text=o["avg_goals"].round(2),
        title="⚽ Promedio de Goles"
    )
    fig2.update_traces(marker_color="#2ca02c", textposition="outside")

    fig3 = px.bar(
        p,
        x="team",
        y="performance_index",
        text=p["performance_index"].round(2),
        title="📈 Índice de Rendimiento"
    )
    fig3.update_traces(marker_color="#ff7f0e", textposition="outside")

    fig4 = px.line(
        evolucion,
        x="version",
        y="avg_goals",
        markers=True,
        title="🌍 Evolución Histórica"
    )
    fig4.update_traces(
        line_color="#00bfff",
        line_width=3,
        marker_size=9
    )

    for fig in [fig1, fig2, fig3, fig4]:

        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            title={"x": 0.5, "font": {"size": 20}},
            xaxis_title="",
            margin=dict(l=40, r=40, t=70, b=40),
            showlegend=False
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#444444")

    return fig1, fig2, fig3, fig4


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )
