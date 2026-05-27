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
# COLUMNAS
# ==========================================

COL_TOTAL = "Total (€)"
COL_IVA = "IVA (€)"

# ==========================================
# LIMPIAR FILAS VACÍAS
# ==========================================

ingresos = ingresos.dropna(
    subset=[COL_TOTAL]
)

gastos = gastos.dropna(
    subset=[COL_TOTAL]
)

# ==========================================
# CONVERTIR A NUMÉRICO
# ==========================================

for col in [COL_TOTAL, COL_IVA]:

    ingresos[col] = pd.to_numeric(
        ingresos[col],
        errors="coerce"
    ).fillna(0)

    gastos[col] = pd.to_numeric(
        gastos[col],
        errors="coerce"
    ).fillna(0)

# ==========================================
# ELIMINAR TOTALES Y RESÚMENES
# ==========================================

if "Cliente" in ingresos.columns:

    ingresos = ingresos[
        ~ingresos["Cliente"]
        .astype(str)
        .str.contains(
            "TOTAL|RESUMEN",
            case=False,
            na=False
        )
    ]

if "Proveedor" in gastos.columns:

    gastos = gastos[
        ~gastos["Proveedor"]
        .astype(str)
        .str.contains(
            "TOTAL|RESUMEN",
            case=False,
            na=False
        )
    ]

# ==========================================
# KPIs
# ==========================================

ventas = ingresos[COL_TOTAL].sum()

gastos_total = gastos[COL_TOTAL].sum()

beneficio = ventas - gastos_total

iva_rep = ingresos[COL_IVA].sum()

iva_sop = gastos[COL_IVA].sum()

resultado_iva = iva_rep - iva_sop

# ==========================================
# DASHBOARD
# ==========================================

st.title("🍷 IBAI VITICULTORES — Dashboard 2026")

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
# CLIENTES
# ==========================================

if "Cliente" in ingresos.columns:

    st.subheader("📈 Ventas por cliente")

    clientes = (
        ingresos
        .groupby("Cliente")[COL_TOTAL]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(clientes)

# ==========================================
# CATEGORÍAS
# ==========================================

if "Categoría" in gastos.columns:

    st.subheader("📦 Gastos por categoría")

    categorias = (
        gastos
        .groupby("Categoría")[COL_TOTAL]
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
# PDF
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

    st.text(texto[:5000])
