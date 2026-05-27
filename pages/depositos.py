import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Depósitos",
    layout="wide"
)

st.title("🍷 Gestión de depósitos")

# ==========================================
# CONEXION SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

# ==========================================
# FORMULARIO NUEVO DEPOSITO
# ==========================================

st.header("➕ Nuevo depósito")

with st.form("nuevo_deposito"):

    nombre = st.text_input("Nombre depósito")

    capacidad = st.number_input(
        "Capacidad litros",
        min_value=0
    )

    tipo = st.selectbox(

        "Tipo depósito",

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

# ==========================================
# GUARDAR SQLITE
# ==========================================

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

# ==========================================
# MOSTRAR DEPOSITOS
# ==========================================

st.header("📦 Depósitos")

depositos = pd.read_sql_query(

    "SELECT * FROM depositos",

    conn

)

st.dataframe(
    depositos,
    use_container_width=True
)

# ==========================================
# KPIS
# ==========================================

st.header("📊 Resumen")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Número depósitos",
    len(depositos)
)

c2.metric(
    "Capacidad total",
    f"{depositos['capacidad_l'].sum():,.0f} L"
)

c3.metric(
    "Depósitos fermentando",
    len(
        depositos[
            depositos["estado"]
            ==
            "Fermentando"
        ]
    )
)

conn.close()
