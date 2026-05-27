import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Embotellado",
    layout="wide"
)

st.title("🍾 Embotellado")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

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

st.header("➕ Nuevo embotellado")

with st.form("nuevo_embotellado"):

    fecha = st.date_input(
        "Fecha"
    )

    lote = st.text_input(
        "Lote"
    )

    deposito = st.selectbox(
        "Depósito origen",
        lista_depositos
    )

    formato = st.selectbox(

        "Formato botella",

        [
            0.75,
            1.5,
            0.375
        ]

    )

    botellas = st.number_input(
        "Número botellas",
        min_value=0
    )

    observaciones = st.text_area(
        "Observaciones"
    )

    guardar = st.form_submit_button(
        "Guardar embotellado"
    )

# ==========================================
# GUARDAR
# ==========================================

if guardar:

    litros = round(
        botellas * formato,
        2
    )

    # ======================================
    # MOVIMIENTO VINO
    # ======================================

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

        "Embotellado",

        deposito,

        "BOTELLAS",

        litros,

        f"Lote {lote}"

    ))

    # ======================================
    # CONSUMO STOCK SECO
    # ======================================

    materiales = [

        "Botella Borgoña",
        "Corcho Natural",
        "Etiqueta",
        "Cápsula"

    ]

    for material in materiales:

        cursor.execute("""

        INSERT INTO stock_seco (

            producto,
            cantidad,
            unidad

        )

        VALUES (?, ?, ?)

        """, (

            material,
            -botellas,
            "uds"

        ))

    conn.commit()

    st.success(
        "✅ Embotellado registrado"
    )

    st.info(
        f"🍷 Litros descontados: {litros} L"
    )

    st.warning(
        f"📦 Material consumido: {botellas} uds"
    )

# ==========================================
# TABLA EMBOTELLADOS
# ==========================================

st.header("📦 Embotellados")

embotellados = pd.read_sql_query("""

SELECT *

FROM movimientos

WHERE tipo = 'Embotellado'

""", conn)

st.dataframe(
    embotellados,
    use_container_width=True
)

# ==========================================
# KPIS
# ==========================================

st.header("📊 Resumen")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Embotellados",
    len(embotellados)
)

c2.metric(
    "Litros embotellados",
    f"{embotellados['litros'].sum():,.0f} L"
)

c3.metric(
    "Botellas estimadas",

    f"{(embotellados['litros'].sum() / 0.75):,.0f}"
)

conn.close()
