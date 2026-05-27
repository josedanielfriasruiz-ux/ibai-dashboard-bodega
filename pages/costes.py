import streamlit as st
import pandas as pd

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Costes",
    layout="wide"
)

st.title("💰 Coste real botella")

# ==========================================
# FORMULARIO
# ==========================================

st.header("➕ Costes producción")

with st.form("costes_botella"):

    coste_vino_litro = st.number_input(
        "Coste vino €/L",
        min_value=0.0,
        value=1.20
    )

    coste_botella = st.number_input(
        "Coste botella €",
        min_value=0.0,
        value=0.75
    )

    coste_corcho = st.number_input(
        "Coste corcho €",
        min_value=0.0,
        value=0.45
    )

    coste_capsula = st.number_input(
        "Coste cápsula €",
        min_value=0.0,
        value=0.18
    )

    coste_etiqueta = st.number_input(
        "Coste etiqueta €",
        min_value=0.0,
        value=0.22
    )

    coste_caja = st.number_input(
        "Coste caja €",
        min_value=0.0,
        value=0.80
    )

    formato = st.selectbox(

        "Formato botella",

        [
            0.75,
            1.5,
            0.375
        ]

    )

    precio_venta = st.number_input(
        "Precio venta botella €",
        min_value=0.0,
        value=12.0
    )

    calcular = st.form_submit_button(
        "Calcular coste"
    )

# ==========================================
# CALCULOS
# ==========================================

if calcular:

    coste_vino = (
        coste_vino_litro
        *
        formato
    )

    coste_total = (

        coste_vino

        +

        coste_botella

        +

        coste_corcho

        +

        coste_capsula

        +

        coste_etiqueta

        +

        (coste_caja / 6)

    )

    margen = (
        precio_venta
        -
        coste_total
    )

    margen_pct = 0

    if precio_venta > 0:

        margen_pct = (
            margen
            /
            precio_venta
        ) * 100

    # ======================================
    # KPIS
    # ======================================

    st.header("📊 Resultado")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Coste botella",
        f"{coste_total:.2f} €"
    )

    c2.metric(
        "Margen botella",
        f"{margen:.2f} €"
    )

    c3.metric(
        "Margen %",
        f"{margen_pct:.1f}%"
    )

    # ======================================
    # DESGLOSE
    # ======================================

    desglose = pd.DataFrame({

        "Concepto": [

            "Vino",
            "Botella",
            "Corcho",
            "Cápsula",
            "Etiqueta",
            "Caja"

        ],

        "Coste (€)": [

            coste_vino,
            coste_botella,
            coste_corcho,
            coste_capsula,
            coste_etiqueta,
            coste_caja / 6

        ]

    })

    st.header("📦 Desglose costes")

    st.dataframe(
        desglose,
        use_container_width=True
    )

    # ======================================
    # GRAFICO
    # ======================================

    st.header("📈 Distribución costes")

    grafico = desglose.set_index(
        "Concepto"
    )[
        "Coste (€)"
    ]

    st.bar_chart(grafico)
