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

st.title("🍇 Entradas de vendimia")

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

st.header("➕ Nueva entrada")

with st.form("entrada_vendimia"):

    fecha = st.date_input(
        "Fecha"
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
        "Kg vendimiados",
        min_value=0.0
    )

    deposito = st.selectbox(
        "Depósito destino",
        lista_depositos
    )

    guardar = st.form_submit_button(
        "Guardar entrada"
    )

# ==========================================
# GUARDAR
# ==========================================

if guardar:

    cursor = conn.cursor()

    # ======================================
    # INSERT VENDIMIA
    # ======================================

    cursor.execute("""

    INSERT INTO vendimia (

        fecha,
        parcela,
        variedad,
        kg,
        deposito

    )

    VALUES (?, ?, ?, ?, ?)

    """, (

        str(fecha),
        parcela,
        variedad,
        kg,
        deposito

    ))

    # ======================================
    # CALCULO LITROS
    # ======================================

    litros_estimados = round(
        kg * 0.70,
        0
    )

    # ======================================
    # INSERT MOVIMIENTO
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

        "Entrada vendimia",

        parcela,

        deposito,

        litros_estimados,

        f"{kg} kg {variedad}"

    ))

    conn.commit()

    st.success(
        "✅ Entrada vendimia guardada"
    )

    st.info(
        f"🍷 Litros estimados: {litros_estimados:.0f} L"
    )

# ==========================================
# TABLA VENDIMIA
# ==========================================

st.header("📦 Entradas registradas")

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

st.header("📊 Resumen vendimia")

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
    "Litros estimados",
    f"{vendimia['kg'].sum() * 0.70:,.0f} L"
)

conn.close()
