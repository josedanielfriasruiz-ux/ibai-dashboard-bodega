import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Depositos",
    layout="wide"
)

st.title("🍷 Gestión depósitos")

conn = sqlite3.connect("bodega.db")

st.header("➕ Nuevo depósito")

with st.form("nuevo_deposito"):

    nombre = st.text_input(
        "Nombre depósito"
    )

    capacidad = st.number_input(
        "Capacidad litros",
        min_value=0
    )

    tipo = st.selectbox(

        "Tipo",

        [
            "Inoxidable",
            "Barrica",
            "Hormigón",
            "Plástico"
        ]

    )

    estado = st.selectbox(

        "Estado",

        [
            "Vacío",
            "Lleno",
            "Fermentando",
            "Limpieza"
        ]

    )

    guardar = st.form_submit_button(
        "Guardar depósito"
    )

if guardar:

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO depositos (

        nombre,
        capacidad_l,
        tipo,
        estado

    )

    VALUES (?, ?, ?, ?)

    """, (

        nombre,
        capacidad,
        tipo,
        estado

    ))

    conn.commit()

    st.success(
        "✅ Depósito guardado"
    )

depositos = pd.read_sql_query(
    "SELECT * FROM depositos",
    conn
)

st.dataframe(
    depositos,
    use_container_width=True
)

conn.close()
