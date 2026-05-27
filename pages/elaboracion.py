import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Elaboración",
    layout="wide"
)

st.title("🍷 Elaboración")

# ==========================================
# SQLITE
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

# ==========================================
# DEPOSITOS
# ==========================================

depositos = pd.read_sql_query(
    "SELECT * FROM depositos",
    conn
)

lista_depositos = depositos["nombre"].tolist()

# ==========================================
# PRODUCTOS
# ==========================================

productos = pd.read_sql_query(
    "SELECT * FROM enologicos",
    conn
)

lista_productos = productos[
    "producto"
].unique().tolist()

# ==========================================
# FASE
# ==========================================

fase = st.selectbox(

    "Fase elaboración",

    [

        "Recepción",
        "Fermentación alcohólica",
        "Fermentación maloláctica",
        "Final fermentación maloláctica",
        "Crianza",
        "Clarificación",
        "Estabilización",
        "Embotellado",
        "Crianza botella"

    ]

)

# ==========================================
# COMUNES
# ==========================================

fecha = st.date_input(
    "Fecha"
)

deposito = st.selectbox(
    "Depósito",
    lista_depositos
)

# ==========================================
# PRODUCTO ENOLOGICO
# ==========================================

st.header("🧪 Producto enológico")

producto_enologico = st.selectbox(

    "Producto",

    ["Ninguno"] + lista_productos

)

dosis = st.number_input(
    "Cantidad usada",
    min_value=0.0
)

unidad_dosis = st.selectbox(

    "Unidad",

    [

        "kg",
        "g",
        "L",
        "mL"

    ]

)

# ==========================================
# OBSERVACIONES
# ==========================================

observaciones = st.text_area(
    "Observaciones"
)

# ==========================================
# GUARDAR SIMPLE
# ==========================================

guardar = st.button(
    "Guardar elaboración"
)

if guardar:

    # ======================================
    # ELABORACION
    # ======================================

    cursor.execute("""

    INSERT INTO elaboracion (

        fecha,
        deposito,
        fase,
        texto1

    )

    VALUES (?, ?, ?, ?)

    """, (

        str(fecha),
        deposito,
        fase,
        observaciones

    ))

    # ======================================
    # CONSUMO ENOLOGICO
    # ======================================

    if producto_enologico != "Ninguno":

        cursor.execute("""

        INSERT INTO consumos_enologicos (

            fecha,
            deposito,
            fase,
            producto,
            dosis,
            unidad

        )

        VALUES (?, ?, ?, ?, ?, ?)

        """, (

            str(fecha),
            deposito,
            fase,
            producto_enologico,
            dosis,
            unidad_dosis

        ))

        # ==================================
        # DESCONTAR STOCK
        # ==================================

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
            producto_enologico,
            "CONSUMO",
            "",
            "",
            -dosis,
            unidad_dosis,
            0

        ))

    conn.commit()

    st.success(
        "✅ Elaboración guardada"
    )

# ==========================================
# HISTORICO
# ==========================================

st.header("📦 Histórico elaboración")

historico = pd.read_sql_query(
    "SELECT * FROM elaboracion",
    conn
)

st.dataframe(
    historico,
    use_container_width=True
)

# ==========================================
# CONSUMOS
# ==========================================

st.header("🧪 Consumos enológicos")

consumos = pd.read_sql_query(
    "SELECT * FROM consumos_enologicos",
    conn
)

st.dataframe(
    consumos,
    use_container_width=True
)

conn.close()
