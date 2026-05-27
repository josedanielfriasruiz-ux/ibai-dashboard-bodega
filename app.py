import streamlit as st
import pandas as pd
import pdfplumber
import re

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="IBAI VITICULTORES",
    layout="wide"
)

# ==========================================
# EXCEL
# ==========================================

excel = "Contabilidad_Bodega_2026_COMPLETA_ACTUALIZADA.xlsx"

# ==========================================
# CARGAR DATOS
# ==========================================

ingresos = pd.read_excel(
    excel,
    sheet_name="Ingresos"
)

gastos = pd.read_excel(
    excel,
    sheet_name="Gastos"
)

# ==========================================
# LIMPIAR COLUMNAS
# ==========================================

ingresos.columns = ingresos.columns.str.strip()
gastos.columns = gastos.columns.str.strip()

# ==========================================
# DETECTAR COLUMNAS AUTOMÁTICAMENTE
# ==========================================

col_total_ingresos = None
col_total_gastos = None
col_iva_ingresos = None
col_iva_gastos = None

for col in ingresos.columns:

    if "total" in col.lower():

        col_total_ingresos = col

    if "iva" in col.lower():

        col_iva_ingresos = col

for col in gastos.columns:

    if "total" in col.lower():

        col_total_gastos = col

    if "iva" in col.lower():

        col_iva_gastos = col

# ==========================================
# KPIs
# ==========================================

ventas = ingresos[col_total_ingresos].sum()

gastos_total = gastos[col_total_gastos].sum()

beneficio = ventas - gastos_total

iva_rep = ingresos[col_iva_ingresos].sum()

iva_sop = gastos[col_iva_gastos].sum()

# ==========================================
# TÍTULO
# ==========================================

st.title("🍷 IBAI VITICULTORES — Dashboard 2026")

# ==========================================
# MÉTRICAS
# ==========================================

st.header("📊 Resumen financiero")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Ventas Totales",
    f"{ventas:,.2f} €"
)

col2.metric(
    "Gastos Totales",
    f"{gastos_total:,.2f} €"
)

col3.metric(
    "Beneficio Estimado",
    f"{beneficio:,.2f} €"
)

col4, col5 = st.columns(2)

col4.metric(
    "IVA Repercutido",
    f"{iva_rep:,.2f} €"
)

col5.metric(
    "IVA Soportado",
    f"{iva_sop:,.2f} €"
)

# ==========================================
# CLIENTES
# ==========================================

st.subheader("📈 Ventas por cliente")

if "Cliente" in ingresos.columns:

    clientes = (
        ingresos
        .groupby("Cliente")[col_total_ingresos]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(clientes)

# ==========================================
# CATEGORÍAS
# ==========================================

st.subheader("📦 Gastos por categoría")

if "Categoría" in gastos.columns:

    categorias = (
        gastos
        .groupby("Categoría")[col_total_gastos]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(categorias)

# ==========================================
# TABLAS
# ==========================================

st.subheader("🧾 Ingresos")

st.dataframe(
    ingresos,
    use_container_width=True
)

st.subheader("💸 Gastos")

st.dataframe(
    gastos,
    use_container_width=True
)

# ==========================================
# SUBIR PDF
# ==========================================

st.header("📄 Subir factura PDF")

pdf_file = st.file_uploader(
    "Sube una factura PDF",
    type=["pdf"]
)

if pdf_file is not None:

    texto = ""

    with pdfplumber.open(pdf_file) as pdf:

        for pagina in pdf.pages:

            contenido = pagina.extract_text()

            if contenido:

                texto += contenido

    st.success("✅ PDF leído correctamente")

    st.subheader("📄 Texto detectado")

    st.text(texto[:5000])
