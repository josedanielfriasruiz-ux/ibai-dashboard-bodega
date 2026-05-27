import streamlit as st
import pandas as pd
import pdfplumber

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="IBAI VITICULTORES",
    layout="wide"
)

# ==========================================
# ARCHIVO EXCEL
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
# COLUMNAS REALES
# ==========================================

# INGRESOS
COL_TOTAL_INGRESOS = "Total (€)"
COL_IVA_INGRESOS = "IVA (€)"

# GASTOS
COL_TOTAL_GASTOS = "Total (€)"
COL_IVA_GASTOS = "IVA (€)"

# ==========================================
# CONVERTIR A NUMÉRICO
# ==========================================

for col in [
    COL_TOTAL_INGRESOS,
    COL_IVA_INGRESOS
]:

    ingresos[col] = pd.to_numeric(
        ingresos[col],
        errors="coerce"
    ).fillna(0)

for col in [
    COL_TOTAL_GASTOS,
    COL_IVA_GASTOS
]:

    gastos[col] = pd.to_numeric(
        gastos[col],
        errors="coerce"
    ).fillna(0)

# ==========================================
# KPIs
# ==========================================

ventas = ingresos[COL_TOTAL_INGRESOS].sum()

gastos_total = gastos[COL_TOTAL_GASTOS].sum()

beneficio = ventas - gastos_total

iva_rep = ingresos[COL_IVA_INGRESOS].sum()

iva_sop = gastos[COL_IVA_GASTOS].sum()

resultado_iva = iva_rep - iva_sop

# ==========================================
# TÍTULO
# ==========================================

st.title("🍷 IBAI VITICULTORES — Dashboard 2026")

# ==========================================
# RESUMEN FINANCIERO
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

col4, col5, col6 = st.columns(3)

col4.metric(
    "IVA Repercutido",
    f"{iva_rep:,.2f} €"
)

col5.metric(
    "IVA Soportado",
    f"{iva_sop:,.2f} €"
)

col6.metric(
    "Resultado IVA",
    f"{resultado_iva:,.2f} €"
)

# ==========================================
# VENTAS POR CLIENTE
# ==========================================

if "Cliente" in ingresos.columns:

    st.subheader("📈 Ventas por cliente")

    clientes = (
        ingresos
        .groupby("Cliente")[COL_TOTAL_INGRESOS]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(clientes)

# ==========================================
# GASTOS POR CATEGORÍA
# ==========================================

if "Categoría" in gastos.columns:

    st.subheader("📦 Gastos por categoría")

    categorias = (
        gastos
        .groupby("Categoría")[COL_TOTAL_GASTOS]
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
