import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Lotes",
    layout="wide"
)

st.title("🌳 Lotes")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

# ==========================================
# FORMULARIO
# ==========================================

st.header("➕ Nuevo lote")

with st.form("nuevo_lote"):

    lote = st.text_input(
        "Código lote"
    )

    vino = st.selectbox(

        "Tipo vino",

        [

            "Tempranillo",
            "Viura",
            "Garnacha",
            "Graciano",
            "Mazuelo"

        ]

    )

    anada = st.number_input(
        "Añada",
        value=2026
    )

    parcela = st.text_input(
        "Parcela"
    )

    estado = st.selectbox(

        "Estado",

        [

            "Recepción",
            "FA",
            "FML",
            "Crianza",
            "Embotellado",
            "Botella"

        ]

    )

    litros = st.number_input(
        "Litros",
        min_value=0.0
    )

    guardar = st.form_submit_button(
        "Guardar lote"
    )

# ==========================================
# GUARDAR
# ==========================================

if guardar:

    cursor.execute("""

    INSERT INTO lotes (

        lote,
        vino,
        anada,
        parcela,
        estado,
        litros

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        lote,
        vino,
        anada,
        parcela,
        estado,
        litros

    ))

    conn.commit()

    st.success(
        "✅ Lote guardado"
    )

# ==========================================
# TABLA LOTES
# ==========================================

st.header("📦 Lotes registrados")

lotes = pd.read_sql_query(
    "SELECT * FROM lotes",
    conn
)

st.dataframe(
    lotes,
    use_container_width=True
)

# ==========================================
# KPIS
# ==========================================

st.header("📊 Resumen")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Lotes",
    len(lotes)
)

c2.metric(
    "Litros totales",
    f"{lotes['litros'].sum():,.0f} L"
)

c3.metric(
    "Añadas",
    lotes["anada"].nunique()
)

conn.close()
