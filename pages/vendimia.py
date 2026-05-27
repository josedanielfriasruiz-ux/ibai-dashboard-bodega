import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Vendimia",
    layout="wide"
)

st.title("🍇 Vendimia")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

# ==========================================
# LOTES
# ==========================================

lotes = pd.read_sql_query(
    "SELECT * FROM lotes",
    conn
)

lista_lotes = lotes["lote"].tolist()

# ==========================================
# DEPOSITOS
# ==========================================

depositos = pd.read_sql_query(
    "SELECT * FROM depositos",
    conn
)

lista_depositos = depositos["nombre"].tolist()

# ==========================================
# FORMULARIO
# ==========================================

st.header("➕ Entrada vendimia")

with st.form("nueva_vendimia"):

    fecha = st.date_input(
        "Fecha"
    )

    lote = st.selectbox(
        "Lote",
        lista_lotes
    )

    parcela = st.text_input(
        "Parcela"
    )

    variedad = st.selectbox(

        "Variedad",

        [

            "Tempranillo",
            "Viura",
            "Garnacha",
            "Graciano",
            "Mazuelo"

        ]

    )

    kg = st.number_input(
        "Kg uva",
        min_value=0.0
    )

    deposito = st.selectbox(
        "Depósito",
        lista_depositos
    )

    guardar = st.form_submit_button(
        "Guardar entrada"
    )

# ==========================================
# GUARDAR
# ==========================================

if guardar:

    cursor.execute("""

    INSERT INTO vendimia (

        fecha,
        lote,
        parcela,
        variedad,
        kg,
        deposito

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        str(fecha),
        lote,
        parcela,
        variedad,
        kg,
        deposito

    ))

    conn.commit()

    st.success(
        "✅ Vendimia registrada"
    )

# ==========================================
# HISTORICO
# ==========================================

st.header("📦 Histórico vendimia")

vendimia = pd.read_sql_query(
    "SELECT * FROM vendimia",
    conn
)

st.dataframe(
    vendimia,
    use_container_width=True
)

# ==========================================
# KPIS
# ==========================================

st.header("📊 Resumen")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Entradas",
    len(vendimia)
)

c2.metric(
    "Kg totales",
    f"{vendimia['kg'].sum():,.0f} kg"
)

c3.metric(
    "Lotes",
    vendimia["lote"].nunique()
)

conn.close()
