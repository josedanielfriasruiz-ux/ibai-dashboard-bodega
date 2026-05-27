import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Stock vino",
    layout="wide"
)

st.title("🍷 Stock de vino")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

# ==========================================
# LEER TABLAS
# ==========================================

depositos = pd.read_sql_query(
    "SELECT * FROM depositos",
    conn
)

movimientos = pd.read_sql_query(
    "SELECT * FROM movimientos",
    conn
)

# ==========================================
# CALCULO STOCK
# ==========================================

resultado = []

for _, dep in depositos.iterrows():

    nombre = dep["nombre"]

    capacidad = dep["capacidad_l"]

    entradas = movimientos[
        movimientos["destino"] == nombre
    ]["litros"].sum()

    salidas = movimientos[
        movimientos["origen"] == nombre
    ]["litros"].sum()

    litros_actuales = entradas - salidas

    porcentaje = 0

    if capacidad > 0:

        porcentaje = (
            litros_actuales
            /
            capacidad
        ) * 100

    # ======================================
    # ESTADO
    # ======================================

    estado = "OK"

    if litros_actuales < 0:

        estado = "ERROR"

    elif porcentaje > 100:

        estado = "SOBRECAPACIDAD"

    elif litros_actuales == 0:

        estado = "VACIO"

    elif porcentaje > 90:

        estado = "LLENO"

    resultado.append({

        "Depósito": nombre,

        "Capacidad": capacidad,

        "Litros actuales": round(
            litros_actuales,
            0
        ),

        "% Lleno": round(
            porcentaje,
            1
        ),

        "Estado": estado

    })

# ==========================================
# DATAFRAME
# ==========================================

stock = pd.DataFrame(resultado)

# ==========================================
# MOSTRAR
# ==========================================

st.header("📦 Estado depósitos")

st.dataframe(
    stock,
    use_container_width=True
)

# ==========================================
# ALERTAS
# ==========================================

st.header("🚨 Alertas")

errores = stock[
    stock["Estado"] == "ERROR"
]

sobrecapacidad = stock[
    stock["Estado"] == "SOBRECAPACIDAD"
]

if len(errores) > 0:

    st.error(
        "❌ Hay depósitos con litros negativos"
    )

if len(sobrecapacidad) > 0:

    st.warning(
        "⚠️ Hay depósitos sobre capacidad"
    )

if (
    len(errores) == 0
    and
    len(sobrecapacidad) == 0
):

    st.success(
        "✅ Sin incidencias"
    )

# ==========================================
# KPIS
# ==========================================

st.header("📊 Resumen")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Depósitos",
    len(stock)
)

c2.metric(
    "Litros totales",
    f"{stock['Litros actuales'].sum():,.0f} L"
)

c3.metric(
    "Capacidad total",
    f"{stock['Capacidad'].sum():,.0f} L"
)

c4.metric(
    "% ocupación",

    f"{(stock['Litros actuales'].sum() / stock['Capacidad'].sum()) * 100:.1f}%"

    if stock['Capacidad'].sum() > 0

    else "0%"

)

# ==========================================
# GRAFICO
# ==========================================

st.header("📈 Ocupación depósitos")

grafico = stock.set_index(
    "Depósito"
)[
    "Litros actuales"
]

st.bar_chart(grafico)

conn.close()
