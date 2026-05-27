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
# TABLA
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS elaboracion (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    deposito TEXT,

    fase TEXT,

    dato1 REAL,
    dato2 REAL,
    dato3 REAL,
    dato4 REAL,
    dato5 REAL,
    dato6 REAL,
    dato7 REAL,
    dato8 REAL,
    dato9 REAL,
    dato10 REAL,

    texto1 TEXT,
    texto2 TEXT

)

""")

conn.commit()

# ==========================================
# DEPOSITOS
# ==========================================

depositos = pd.read_sql_query(
    "SELECT * FROM depositos",
    conn
)

lista_depositos = depositos["nombre"].tolist()

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
            texto1

        )

        VALUES (?, ?, ?, ?, ?)

        """, (

            str(fecha),
            deposito,
            fase,
            gap,
            origen

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

        conn.commit()

        st.success(
            "✅ FA guardada"
        )

# ==========================================
# FERMENTACION MALOLACTICA
# ==========================================

elif fase == "Fermentación maloláctica":

    malico = st.number_input(
        "Ácido málico"
    )

    acetico = st.number_input(
        "Ácido acético"
    )

    sulfuroso_libre = st.number_input(
        "Sulfuroso libre"
    )

    sulfuroso_total = st.number_input(
        "Sulfuroso total"
    )

    guardar = st.button(
        "Guardar FML"
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
            dato4

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            str(fecha),
            deposito,
            fase,
            malico,
            acetico,
            sulfuroso_libre,
            sulfuroso_total

        ))

        conn.commit()

        st.success(
            "✅ FML guardada"
        )

# ==========================================
# FINAL FML
# ==========================================

elif fase == "Final fermentación maloláctica":

    alcohol = st.number_input(
        "Grado alcohólico"
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

    sulfuroso_libre = st.number_input(
        "Sulfuroso libre"
    )

    sulfuroso_total = st.number_input(
        "Sulfuroso total"
    )

    intensidad = st.number_input(
        "Intensidad color"
    )

    ipt = st.number_input(
        "IPT"
    )

    malico = st.number_input(
        "Málico"
    )

    azucares = st.number_input(
        "Azúcares"
    )

    guardar = st.button(
        "Guardar final FML"
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
            dato9,
            dato10

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            str(fecha),
            deposito,
            fase,
            alcohol,
            ph,
            at,
            acetico,
            sulfuroso_libre,
            sulfuroso_total,
            intensidad,
            ipt,
            malico,
            azucares

        ))

        conn.commit()

        st.success(
            "✅ Final FML guardado"
        )

# ==========================================
# CRIANZA
# ==========================================

elif fase == "Crianza":

    acetico = st.number_input(
        "Ácido acético"
    )

    sulfuroso_libre = st.number_input(
        "Sulfuroso libre"
    )

    sulfuroso_total = st.number_input(
        "Sulfuroso total"
    )

    brett = st.number_input(
        "Brett"
    )

    guardar = st.button(
        "Guardar crianza"
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
            dato4

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            str(fecha),
            deposito,
            fase,
            acetico,
            sulfuroso_libre,
            sulfuroso_total,
            brett

        ))

        conn.commit()

        st.success(
            "✅ Crianza guardada"
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

conn.close()
