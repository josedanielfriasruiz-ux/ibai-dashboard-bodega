import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Productos enológicos",
    layout="wide"
)

st.title("🧪 Productos enológicos")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

# ==========================================
# TABLA
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS enologicos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    producto TEXT,

    tipo TEXT,

    proveedor TEXT,

    lote_proveedor TEXT,

    cantidad REAL,

    unidad TEXT,

    coste REAL

)

""")

conn.commit()

# ==========================================
# FORMULARIO
# ==========================================

st.header("➕ Entrada producto enológico")

with st.form("nuevo_producto"):

    fecha = st.date_input(
        "Fecha compra"
    )

    producto = st.text_input(
        "Producto"
    )

    tipo = st.selectbox(

        "Tipo producto",

        [

            "Levadura",
            "Bacteria",
            "Nutriente",
            "Tanino",
            "Enzima",
            "Clarificante",
            "Estabilizante",
            "Sulfuroso",
            "Goma arábiga",
            "Otro"

        ]

    )

    proveedor = st.text_input(
        "Proveedor"
    )

    lote_proveedor = st.text_input(
        "Lote proveedor"
    )

    cantidad = st.number_input(
        "Cantidad",
        min_value=0.0
    )

    unidad = st.selectbox(

        "Unidad",

        [

            "kg",
            "g",
            "L",
            "mL"

        ]

    )

    coste = st.number_input(
        "Coste total €",
        min_value=0.0
    )

    guardar = st.form_submit_button(
        "Guardar producto"
    )

# ==========================================
# GUARDAR
# ==========================================

if guardar:

    cursor.execute("""

    INSERT INTO enologicos (

        fecha,
        producto,
        tipo,
        proveedor,
        lote_proveedor,
        cantidad,
        unidad,
        coste

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        str(fecha),
        producto,
        tipo,
        proveedor,
        lote_proveedor,
        cantidad,
        unidad,
        coste

    ))

    conn.commit()

    st.success(
        "✅ Producto guardado"
    )

# ==========================================
# STOCK
# ==========================================

st.header("📦 Stock productos enológicos")

stock = pd.read_sql_query("""

SELECT

    producto,
    tipo,
    unidad,
    SUM(cantidad) as stock_actual,
    SUM(coste) as coste_total

FROM enologicos

GROUP BY producto, tipo, unidad

""", conn)

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
    "Productos",
    len(stock)
)

c2.metric(
    "Stock total",

    f"{stock['stock_actual'].sum():,.1f}"

)

c3.metric(
    "Valor stock",

    f"{stock['coste_total'].sum():,.2f} €"

)

conn.close()
