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
# PRODUCTOS ENOLOGICOS
# ==========================================

productos = pd.read_sql_query(
    "SELECT * FROM enologicos",
    conn
)

lista_productos = productos["producto"].unique().tolist()

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
    "Dosis",
    min_value=0.0
)

unidad_dosis = st.selectbox(

    "Unidad",

    [

        "g/hL",
        "mL/hL",
        "mg/L",
        "g/L"

    ]

)

# ==========================================
# RECEPCION
# ==========================================

if fase == "Recepción":

    origen = st.text_input(
        "Origen uva"
    )

    gap = st.number_input(
        "GAP"
    )

    sulfuroso = st.number_input(
        "Sulfuroso"
    )

    guardar = st.button(
        "Guardar recepción"
    )

    if guardar:

        cursor.execute("""

        INSERT INTO elaboracion (

            fecha,
            deposito,
            fase,
            dato1,
            dato2,
            texto1

        )

        VALUES (?, ?, ?, ?, ?, ?)

        """, (

            str(fecha),
            deposito,
            fase,
            gap,
            sulfuroso,
            origen

        ))

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

        conn.commit()

        st.success(
            "✅ Recepción guardada"
        )

# ==========================================
# FERMENTACION ALCOHOLICA
# ==========================================

elif fase == "Fermentación alcohólica":

    densidad = st.number_input(
        "Densidad"
    )

    temperatura = st.number_input(
        "Temperatura"
    )

    ph = st.number_input(
        "pH"
    )

    at = st.number_input(
        "Acidez total"
    )

    acetico = st.number_input(
        "Ácido acético"
    )

    sulfuroso_total = st.number_input(
        "Sulfuroso total"
    )

    glucosa_fructosa = st.number_input(
        "Glucosa/Fructosa"
    )

    ipt = st.number_input(
        "IPT"
    )

    ic = st.number_input(
        "IC"
    )

    guardar = st.button(
        "Guardar FA"
    )

    if guardar:

        cursor.execute("""

        INSERT INTO elaboracion (

            fecha,
            deposito,
            fase,
            dato1,
            dato2,
            dato3,
            dato4,
            dato5,
            dato6,
            dato7,
            dato8,
            dato9

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            str(fecha),
            deposito,
            fase,
            densidad,
            temperatura,
            ph,
            at,
            acetico,
            sulfuroso_total,
            glucosa_fructosa,
            ipt,
            ic

        ))

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

        conn.commit()

        st.success(
            "✅ FA guardada"
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
# CONSUMOS ENOLOGICOS
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
