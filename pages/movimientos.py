import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Movimientos",
    layout="wide"
)

st.title("🍷 Movimientos de vino")

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

lista_depositos = depositos["nombre"].tolist()

# ==========================================
# FORMULARIO
# ==========================================

st.header("➕ Nuevo movimiento")

with st.form("nuevo_movimiento"):

    fecha = st.date_input(
        "Fecha"
    )

    tipo = st.selectbox(

        "Tipo movimiento",

        [
            "Trasiego",
            "Embotellado",
            "Merma",
            "Corrección",
            "Movimiento interno"
        ]

    )

    origen = st.selectbox(
        "Origen",
        lista_depositos
    )

    destino = st.selectbox(
        "Destino",
        lista_depositos
    )

    litros = st.number_input(
        "Litros",
        min_value=0.0
    )

    observaciones = st.text_area(
        "Observaciones"
    )

    guardar = st.form_submit_button(
        "Guardar movimiento"
    )

# ==========================================
# GUARDAR SQLITE
# ==========================================

if guardar:

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO movimientos (

        fecha,
        tipo,
        origen,
        destino,
        litros,
        observaciones

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        str(fecha),
        tipo,
        origen,
        destino,
        litros,
        observaciones

    ))

    conn.commit()

    st.success(
        "✅ Movimiento guardado"
    )

# ==========================================
# TABLA MOVIMIENTOS
# ==========================================

st.header("📦 Movimientos registrados")

movimientos = pd.read_sql_query(
    "SELECT * FROM movimientos",
    conn
)

st.dataframe(
    movimientos,
    use_container_width=True
)

# ==========================================
# KPIS
# ==========================================

st.header("📊 Resumen movimientos")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Número movimientos",
    len(movimientos)
)

c2.metric(
    "Litros movidos",
    f"{movimientos['litros'].sum():,.0f} L"
)

c3.metric(
    "Trasiegos",
    len(
        movimientos[
            movimientos["tipo"]
            ==
            "Trasiego"
        ]
    )
)

conn.close()
