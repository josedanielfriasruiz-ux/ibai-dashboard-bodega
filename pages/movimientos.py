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

st.header("➕ Nuevo movimiento")

with st.form("nuevo_movimiento"):

    fecha = st.date_input(
        "Fecha"
    )

    lote = st.selectbox(
        "Lote",
        lista_lotes
    )

    tipo = st.selectbox(

        "Tipo movimiento",

        [

            "Trasiego",
            "Movimiento interno",
            "Corrección",
            "Merma"

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
# GUARDAR
# ==========================================

if guardar:

    cursor.execute("""

    INSERT INTO movimientos (

        fecha,
        lote,
        tipo,
        origen,
        destino,
        litros,
        observaciones

    )

    VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        str(fecha),
        lote,
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
# HISTORICO
# ==========================================

st.header("📦 Histórico movimientos")

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

st.header("📊 Resumen")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Movimientos",
    len(movimientos)
)

c2.metric(
    "Litros movidos",
    f"{movimientos['litros'].sum():,.0f} L"
)

c3.metric(
    "Lotes activos",
    movimientos["lote"].nunique()
)

conn.close()
