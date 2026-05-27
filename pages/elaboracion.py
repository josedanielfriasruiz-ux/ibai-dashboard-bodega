import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Trazabilidad",
    layout="wide"
)

st.title("🌳 Árbol de trazabilidad")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

# ==========================================
# LOTES
# ==========================================

lotes = pd.read_sql_query(
    "SELECT * FROM lotes",
    conn
)

lista_lotes = lotes["lote"].tolist()

# ==========================================
# SELECCION LOTE
# ==========================================

lote = st.selectbox(
    "Seleccionar lote",
    lista_lotes
)

# ==========================================
# INFO LOTE
# ==========================================

st.header("🍷 Información lote")

info_lote = pd.read_sql_query(

    f"""

    SELECT *

    FROM lotes

    WHERE lote = '{lote}'

    """,

    conn

)

st.dataframe(
    info_lote,
    use_container_width=True
)

# ==========================================
# VENDIMIA
# ==========================================

st.header("🍇 Vendimia")

vendimia = pd.read_sql_query(

    f"""

    SELECT *

    FROM vendimia

    WHERE lote = '{lote}'

    """,

    conn

)

st.dataframe(
    vendimia,
    use_container_width=True
)

# ==========================================
# MOVIMIENTOS
# ==========================================

st.header("🍷 Movimientos")

movimientos = pd.read_sql_query(

    f"""

    SELECT *

    FROM movimientos

    WHERE lote = '{lote}'

    """,

    conn

)

st.dataframe(
    movimientos,
    use_container_width=True
)

# ==========================================
# ELABORACION
# ==========================================

st.header("🧪 Elaboración")

elaboracion = pd.read_sql_query(

    f"""

    SELECT *

    FROM elaboracion

    WHERE lote = '{lote}'

    """,

    conn

)

st.dataframe(
    elaboracion,
    use_container_width=True
)

# ==========================================
# CONSUMOS ENOLOGICOS
# ==========================================

st.header("🧪 Productos enológicos")

consumos = pd.read_sql_query(

    f"""

    SELECT *

    FROM consumos_enologicos

    WHERE lote = '{lote}'

    """,

    conn

)

st.dataframe(
    consumos,
    use_container_width=True
)

# ==========================================
# EMBOTELLADOS
# ==========================================

st.header("🍾 Embotellados")

embotellados = pd.read_sql_query(

    f"""

    SELECT *

    FROM movimientos

    WHERE lote = '{lote}'

    AND tipo = 'Embotellado'

    """,

    conn

)

st.dataframe(
    embotellados,
    use_container_width=True
)

# ==========================================
# RESUMEN
# ==========================================

st.header("📊 Resumen lote")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Movimientos",
    len(movimientos)
)

c2.metric(
    "Procesos elaboración",
    len(elaboracion)
)

c3.metric(
    "Productos enológicos",
    len(consumos)
)

conn.close()
