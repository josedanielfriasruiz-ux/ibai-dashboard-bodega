import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Stock seco",
    layout="wide"
)

st.title("📦 Stock seco")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

# ==========================================
# CREAR TABLA
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS stock_seco (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    producto TEXT,

    cantidad REAL,

    unidad TEXT

)

""")

conn.commit()

# ==========================================
# FORMULARIO
# ==========================================

st.header("➕ Entrada material")

with st.form("nuevo_material"):

    producto = st.selectbox(

        "Producto",

        [
            "Botella Borgoña",
            "Corcho Natural",
            "Etiqueta",
            "Cápsula",
            "Caja 6 botellas"
        ]

    )

    cantidad = st.number_input(
        "Cantidad",
        min_value=0.0
    )

    unidad = st.selectbox(

        "Unidad",

        [
            "uds",
            "cajas",
            "palets"
        ]

    )

    guardar = st.form_submit_button(
        "Guardar material"
    )

# ==========================================
# GUARDAR
# ==========================================

if guardar:

    cursor.execute("""

    INSERT INTO stock_seco (

        producto,
        cantidad,
        unidad

    )

    VALUES (?, ?, ?)

    """, (

        producto,
        cantidad,
        unidad

    ))

    conn.commit()

    st.success(
        "✅ Material añadido"
    )

# ==========================================
# STOCK AGRUPADO
# ==========================================

stock = pd.read_sql_query("""

SELECT

    producto,
    unidad,
    SUM(cantidad) as stock_actual

FROM stock_seco

GROUP BY producto, unidad

""", conn)

# ==========================================
# MOSTRAR
# ==========================================

st.header("📦 Stock actual")

st.dataframe(
    stock,
    use_container_width=True
)

# ==========================================
# KPIS
# ==========================================

st.header("📊 Resumen")

c1, c2 = st.columns(2)

c1.metric(
    "Productos",
    len(stock)
)

c2.metric(
    "Total referencias",
    stock["stock_actual"].sum()
)

conn.close()
