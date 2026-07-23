library(shiny)
library(bslib)
library(plotly)
library(DBI)
library(RMariaDB)
library(dotenv)
library(bsicons)

# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR <- normalizePath(
  file.path(getwd(), "../.."),
  mustWork = FALSE
)

ENV_FILE <- file.path(
  BASE_DIR,
  "config",
  ".env"
)

load_dot_env(
  file = ENV_FILE
)

# ============================================================
# CONEXIÓN A MYSQL
# ============================================================

crear_conexion <- function() {

  dbConnect(
    RMariaDB::MariaDB(),
    host = "127.0.0.1",
    port = 3306,
    user = Sys.getenv("DB2_USER"),
    password = Sys.getenv("DB2_PASS"),
    dbname = Sys.getenv("DB2_NAME")
  )

}

# ============================================================
# PALETA DE COLORES
# ============================================================

COLOR_NAVY <- "#183B56"
COLOR_TEXT <- "#425466"
COLOR_BG <- "#EAF6FB"
COLOR_CARD <- "#FFFFFF"

ROJO_PASTEL <- "#FFADAD"
AMARILLO_PASTEL <- "#FFD6A5"
MORADO_PASTEL <- "#BDB2FF"
AZUL_PASTEL <- "#A0C4FF"

# ============================================================
# UI
# ============================================================

ui <- page_navbar(

  title = "Proyecto FIFA",

  id = "navbar",

  theme = bs_theme(
    version = 5,
    bg = COLOR_BG,
    fg = COLOR_TEXT,
    primary = COLOR_NAVY,
    secondary = "#6C7A89",
    base_font = font_google("Inter"),
    heading_font = font_google("Inter")
  ),

  header = tags$head(

    tags$style(HTML("

      body {
        background-color: #EAF6FB !important;
        color: #425466;
      }

      .navbar {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #D9EAF2;
        box-shadow: 0 2px 10px rgba(24, 59, 86, 0.08);
      }

      .navbar-brand {
        color: #183B56 !important;
        font-weight: 700;
        font-size: 1.25rem;
      }

      .nav-link {
        color: #425466 !important;
        font-weight: 500;
      }

      .nav-link.active {
        color: #183B56 !important;
        font-weight: 700;
      }

      .bslib-sidebar-layout {
        background-color: #EAF6FB !important;
      }

      .sidebar {
        background-color: #FFFFFF !important;
        border-right: 1px solid #D9EAF2;
      }

      .dashboard-title {
        color: #183B56;
        font-weight: 700;
        font-size: 2rem;
        margin-top: 5px;
        margin-bottom: 4px;
      }

      .dashboard-subtitle {
        color: #6C7A89;
        font-size: 1rem;
        margin-bottom: 18px;
      }

      .card {
        background-color: #FFFFFF !important;
        border: 1px solid #E1EDF3 !important;
        border-radius: 14px !important;
        box-shadow: 0 5px 18px rgba(24, 59, 86, 0.08) !important;
        overflow: hidden;
      }

      .card-header {
        background-color: #FFFFFF !important;
        color: #183B56 !important;
        font-weight: 700;
        font-size: 1rem;
        border-bottom: 1px solid #EEF3F6 !important;
        padding: 10px 15px !important;
      }

      .value-box {
        background-color: #FFFFFF !important;
        border: 1px solid #E1EDF3 !important;
        border-radius: 14px !important;
        box-shadow: 0 5px 18px rgba(24, 59, 86, 0.08) !important;
      }

      .value-box-title {
        color: #6C7A89 !important;
        font-size: 0.9rem !important;
      }

      .value-box-value {
        color: #183B56 !important;
        font-weight: 700 !important;
        font-size: 1.65rem !important;
      }

      .form-label {
        color: #425466;
        font-weight: 600;
      }

      .selectize-input {
        border-radius: 9px !important;
        border: 1px solid #D5E5ED !important;
        background-color: #FFFFFF !important;
      }

      .btn-primary {
        background-color: #A0C4FF !important;
        border-color: #A0C4FF !important;
        color: #183B56 !important;
        font-weight: 600;
        border-radius: 9px !important;
      }

      .btn-primary:hover {
        background-color: #8DB7F5 !important;
        border-color: #8DB7F5 !important;
      }

      .plotly {
        background-color: #FFFFFF !important;
      }

      /* Altura estable de las gráficas */
      .grafica-dashboard {
        height: 285px !important;
      }

      /* Separación entre filas */
      .fila-graficas {
        margin-bottom: 18px;
      }

      /* Evita espacios verticales excesivos */
      .container-fluid {
        padding-top: 12px !important;
        padding-bottom: 12px !important;
      }

      /* En pantallas algo menores */
      @media (max-width: 1200px) {

        .grafica-dashboard {
          height: 270px !important;
        }

        .dashboard-title {
          font-size: 1.7rem;
        }

        .value-box-value {
          font-size: 1.4rem !important;
        }

      }

    "))

  ),

  # ==========================================================
  # PANEL DASHBOARD
  # ==========================================================

  nav_panel(

    "Dashboard",

    layout_sidebar(

      sidebar = sidebar(

        h5(
          "Filtros",
          style = "color:#183B56; font-weight:700;"
        ),

        selectInput(
          inputId = "equipo",
          label = "Seleccionar equipo:",
          choices = NULL
        ),

        actionButton(
          inputId = "actualizar",
          label = "Actualizar datos",
          class = "btn-primary",
          width = "100%"
        )

      ),

      # ========================================================
      # ENCABEZADO
      # ========================================================

      div(

        class = "dashboard-title text-center",

        "PROYECTO FIFA - DASHBOARD BI"

      ),

      div(

        class = "dashboard-subtitle text-center",

        "Análisis gerencial de rendimiento, ofensiva y evolución histórica"

      ),

      # ========================================================
      # KPIs
      # ========================================================

      layout_column_wrap(

        width = 1/3,

        gap = "15px",

        value_box(

          title = "Porcentaje de Victorias",

          value = textOutput(
            "valor_victorias"
          ),

          showcase = bsicons::bs_icon(
            "trophy",
            size = "1.5em"
          )

        ),

        value_box(

          title = "Promedio de Goles",

          value = textOutput(
            "valor_goles"
          ),

          showcase = bsicons::bs_icon(
            "bullseye",
            size = "1.5em"
          )

        ),

        value_box(

          title = "Índice de Rendimiento",

          value = textOutput(
            "valor_rendimiento"
          ),

          showcase = bsicons::bs_icon(
            "graph-up",
            size = "1.5em"
          )

        )

      ),

      br(),

      # ========================================================
      # FILA 1
      # ========================================================

      div(

        class = "fila-graficas",

        layout_column_wrap(

          width = 1/2,

          gap = "18px",

          # ----------------------------------------------------
          # GRÁFICA 1 - BARRAS
          # ----------------------------------------------------

          card(

            full_screen = TRUE,

            card_header(
              "Porcentaje de Victorias por Equipo"
            ),

            plotlyOutput(
              "grafico_ranking",
              height = "285px"
            )

          ),

          # ----------------------------------------------------
          # GRÁFICA 2 - DONUT
          # ----------------------------------------------------

          card(

            full_screen = TRUE,

            card_header(
              "Distribución del Promedio de Goles"
            ),

            plotlyOutput(
              "grafico_ofensiva",
              height = "285px"
            )

          )

        )

      ),

      # ========================================================
      # FILA 2
      # ========================================================

      div(

        class = "fila-graficas",

        layout_column_wrap(

          width = 1/2,

          gap = "18px",

          # ----------------------------------------------------
          # GRÁFICA 3 - SCATTER
          # ----------------------------------------------------

          card(

            full_screen = TRUE,

            card_header(
              "Relación entre Victorias y Rendimiento"
            ),

            plotlyOutput(
              "grafico_rendimiento",
              height = "285px"
            )

          ),

          # ----------------------------------------------------
          # GRÁFICA 4 - LÍNEAS
          # ----------------------------------------------------

          card(

            full_screen = TRUE,

            card_header(
              "Evolución Histórica de los Mundiales"
            ),

            plotlyOutput(
              "grafico_evolucion",
              height = "285px"
            )

          )

        )

      )

    )

  ),

  # ==========================================================
  # PANEL DATOS
  # ==========================================================

  nav_panel(

    "Datos",

    layout_column_wrap(

      width = 1,

      card(

        card_header(
          "Datos de KPIs"
        ),

        tableOutput(
          "tabla_datos"
        )

      )

    )

  )

)

# ============================================================
# SERVER
# ============================================================

server <- function(input, output, session) {

  # ==========================================================
  # DATOS
  # ==========================================================

  datos <- reactiveValues(

    ranking = NULL,

    ofensiva = NULL,

    evolucion = NULL,

    rendimiento = NULL

  )

  # ==========================================================
  # CARGAR DATOS
  # ==========================================================

  cargar_datos <- function() {

    con <- crear_conexion()

    on.exit(

      dbDisconnect(con),

      add = TRUE

    )

    datos$ranking <- dbGetQuery(

      con,

      "SELECT * FROM kpi_ranking"

    )

    datos$ofensiva <- dbGetQuery(

      con,

      "SELECT * FROM kpi_ofensiva"

    )

    datos$evolucion <- dbGetQuery(

      con,

      "SELECT * FROM kpi_evolucion"

    )

    datos$rendimiento <- dbGetQuery(

      con,

      "SELECT * FROM kpi_rendimiento"

    )

  }

  # ==========================================================
  # CARGA INICIAL
  # ==========================================================

  observe({

    cargar_datos()

    equipos <- sort(

      unique(

        c(

          datos$ranking$team,

          datos$ofensiva$team,

          datos$rendimiento$team

        )

      )

    )

    updateSelectInput(

      session,

      "equipo",

      choices = equipos,

      selected = equipos[1]

    )

  })

  # ==========================================================
  # ACTUALIZAR
  # ==========================================================

  observeEvent(

    input$actualizar,

    {

      cargar_datos()

      equipos <- sort(

        unique(

          c(

            datos$ranking$team,

            datos$ofensiva$team,

            datos$rendimiento$team

          )

        )

      )

      updateSelectInput(

        session,

        "equipo",

        choices = equipos,

        selected = input$equipo

      )

      showNotification(

        "Datos actualizados correctamente.",

        type = "message"

      )

    }

  )

  # ==========================================================
  # KPI VICTORIAS
  # ==========================================================

  output$valor_victorias <- renderText({

    req(input$equipo)

    req(datos$ranking)

    fila <- datos$ranking[

      datos$ranking$team == input$equipo,

      ,

      drop = FALSE

    ]

    if (nrow(fila) == 0) {

      return("N/A")

    }

    paste0(

      round(

        fila$win_percentage[1],

        2

      ),

      "%"

    )

  })

  # ==========================================================
  # KPI GOLES
  # ==========================================================

  output$valor_goles <- renderText({

    req(input$equipo)

    req(datos$ofensiva)

    fila <- datos$ofensiva[

      datos$ofensiva$team == input$equipo,

      ,

      drop = FALSE

    ]

    if (nrow(fila) == 0) {

      return("N/A")

    }

    round(

      fila$avg_goals[1],

      2

    )

  })

  # ==========================================================
  # KPI RENDIMIENTO
  # ==========================================================

  output$valor_rendimiento <- renderText({

    req(input$equipo)

    req(datos$rendimiento)

    fila <- datos$rendimiento[

      datos$rendimiento$team == input$equipo,

      ,

      drop = FALSE

    ]

    if (nrow(fila) == 0) {

      return("N/A")

    }

    round(

      fila$performance_index[1],

      3

    )

  })

  # ==========================================================
  # GRÁFICA 1 - BARRAS
  # Porcentaje de victorias
  # ==========================================================

  output$grafico_ranking <- renderPlotly({

    req(datos$ranking)

    df <- datos$ranking

    df <- df[

      order(

        df$win_percentage,

        decreasing = TRUE

      ),

    ]

    plot_ly(

      data = df,

      x = ~win_percentage,

      y = ~reorder(

        team,

        win_percentage

      ),

      type = "bar",

      orientation = "h",

      marker = list(

        color = AZUL_PASTEL,

        line = list(

          color = "#7FA9D8",

          width = 1

        )

      ),

      text = ~paste0(

        round(

          win_percentage,

          2

        ),

        "%"

      ),

      textposition = "outside",

      hovertemplate = paste(

        "<b>%{y}</b><br>",

        "Victorias: %{x:.2f}%",

        "<extra></extra>"

      )

    ) %>%

      layout(

        margin = list(

          l = 110,

          r = 45,

          t = 10,

          b = 45

        ),

        font = list(

          family = "Inter",

          size = 13,

          color = COLOR_TEXT

        ),

        xaxis = list(

          title = "Porcentaje de Victorias (%)",

          tickfont = list(

            size = 12

          ),

          gridcolor = "#E8F0F5"

        ),

        yaxis = list(

          title = "",

          tickfont = list(

            size = 12

          )

        ),

        plot_bgcolor = "#FFFFFF",

        paper_bgcolor = "#FFFFFF",

        hoverlabel = list(

          bgcolor = "#FFFFFF",

          font = list(

            size = 13

          )

        )

      )

  })

  # ==========================================================
  # GRÁFICA 2 - DONUT
  # Promedio de goles
  # ==========================================================

  output$grafico_ofensiva <- renderPlotly({

    req(datos$ofensiva)

    df <- datos$ofensiva

    plot_ly(

      data = df,

      labels = ~team,

      values = ~avg_goals,

      type = "pie",

      hole = 0.48,

      sort = FALSE,

      textinfo = "label+percent",

      textposition = "outside",

      marker = list(

        colors = c(

          ROJO_PASTEL,

          AMARILLO_PASTEL,

          MORADO_PASTEL,

          AZUL_PASTEL

        ),

        line = list(

          color = "#FFFFFF",

          width = 2

        )

      ),

      hovertemplate = paste(

        "<b>%{label}</b><br>",

        "Promedio de goles: %{value:.2f}",

        "<extra></extra>"

      )

    ) %>%

      layout(

        margin = list(

          l = 25,

          r = 25,

          t = 10,

          b = 20

        ),

        font = list(

          family = "Inter",

          size = 13,

          color = COLOR_TEXT

        ),

        showlegend = TRUE,

        legend = list(

          orientation = "v",

          font = list(

            size = 11

          )

        ),

        plot_bgcolor = "#FFFFFF",

        paper_bgcolor = "#FFFFFF"

      )

  })

  # ==========================================================
  # GRÁFICA 3 - SCATTER
  # Victorias vs rendimiento
  # ==========================================================

  output$grafico_rendimiento <- renderPlotly({

    req(datos$ranking)

    req(datos$rendimiento)

    df <- merge(

      datos$ranking,

      datos$rendimiento,

      by = "team"

    )

    plot_ly(

      data = df,

      x = ~win_percentage,

      y = ~performance_index,

      type = "scatter",

      mode = "markers+text",

      text = ~team,

      textposition = "top center",

      marker = list(

        size = 14,

        color = MORADO_PASTEL,

        line = list(

          color = "#887CD6",

          width = 1.5

        )

      ),

      hovertemplate = paste(

        "<b>%{text}</b><br>",

        "Victorias: %{x:.2f}%<br>",

        "Rendimiento: %{y:.3f}",

        "<extra></extra>"

      )

    ) %>%

      layout(

        margin = list(

          l = 65,

          r = 30,

          t = 10,

          b = 60

        ),

        font = list(

          family = "Inter",

          size = 13,

          color = COLOR_TEXT

        ),

        xaxis = list(

          title = "Porcentaje de Victorias (%)",

          tickfont = list(

            size = 12

          ),

          gridcolor = "#E8F0F5"

        ),

        yaxis = list(

          title = "Índice de Rendimiento",

          tickfont = list(

            size = 12

          ),

          gridcolor = "#E8F0F5"

        ),

        plot_bgcolor = "#FFFFFF",

        paper_bgcolor = "#FFFFFF",

        hovermode = "closest"

      )

  })

  # ==========================================================
  # GRÁFICA 4 - LÍNEAS
  # Evolución histórica
  # ==========================================================

  output$grafico_evolucion <- renderPlotly({

    req(datos$evolucion)

    df <- datos$evolucion

    plot_ly(

      data = df,

      x = ~version,

      y = ~total_goals,

      type = "scatter",

      mode = "lines+markers",

      name = "Goles Totales",

      line = list(

        color = AZUL_PASTEL,

        width = 4

      ),

      marker = list(

        color = AZUL_PASTEL,

        size = 9,

        line = list(

          color = "#6E9FD4",

          width = 1

        )

      ),

      hovertemplate = paste(

        "<b>Mundial %{x}</b><br>",

        "Goles totales: %{y}",

        "<extra></extra>"

      )

    ) %>%

      layout(

        margin = list(

          l = 65,

          r = 30,

          t = 10,

          b = 55

        ),

        font = list(

          family = "Inter",

          size = 13,

          color = COLOR_TEXT

        ),

        xaxis = list(

          title = "Año",

          tickmode = "linear",

          dtick = 4,

          tickfont = list(

            size = 12

          )

        ),

        yaxis = list(

          title = "Goles Totales",

          tickfont = list(

            size = 12

          ),

          gridcolor = "#E8F0F5"

        ),

        plot_bgcolor = "#FFFFFF",

        paper_bgcolor = "#FFFFFF",

        hovermode = "x unified"

      )

  })

  # ==========================================================
  # TABLA
  # ==========================================================

  output$tabla_datos <- renderTable({

    req(datos$ranking)

    datos$ranking

  })

}

# ============================================================
# EJECUTAR APP
# ============================================================

shinyApp(

  ui = ui,

  server = server

)
```

