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
# LEER DEPOSITOS
# ==========================================

depositos = pd.read_sql_query(
    "SELECT * FROM depositos",
    conn
)

# ==========================================
# LEER MOVIMIENTOS
# ==========================================

movimientos = pd.read_sql_query(
    "SELECT * FROM movimientos",
    conn
)

# ==========================================
# CALCULAR STOCK
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

    resultado.append({

        "Depósito": nombre,

        "Capacidad": capacidad,

        "Litros actuales": litros_actuales,

        "% Lleno": round(
            porcentaje,
            1
        )

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
# KPIS
# ==========================================

st.header("📊 Resumen")

c1, c2, c3 = st.columns(3)

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

conn.close()
