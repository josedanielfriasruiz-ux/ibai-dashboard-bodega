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
# ARCHIVO EXCEL
# ==========================================

excel = "Contabilidad_Bodega_2026_COMPLETA_ACTUALIZADA.xlsx"

# ==========================================
# LEER EXCEL
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
# ELIMINAR FILAS TOTAL
# ==========================================

if "Concepto" in ingresos.columns:

    ingresos = ingresos[
        ingresos["Concepto"]
        .astype(str)
        .str.upper()
        != "TOTAL"
    ]

if "Concepto" in gastos.columns:

    gastos = gastos[
        gastos["Concepto"]
        .astype(str)
        .str.upper()
        != "TOTAL"
    ]

# ==========================================
# COLUMNAS
# ==========================================

COL_BASE = "Base Imponible"
COL_IVA = "IVA (€)"
COL_TOTAL = "Total (€)"

# ==========================================
# NUMÉRICOS
# ==========================================

for col in [COL_BASE, COL_IVA, COL_TOTAL]:

    ingresos[col] = pd.to_numeric(
        ingresos[col],
        errors="coerce"
    ).fillna(0)

    gastos[col] = pd.to_numeric(
        gastos[col],
        errors="coerce"
    ).fillna(0)

# ==========================================
# KPIs
# ==========================================

ventas = ingresos[COL_TOTAL].sum()

gastos_total = gastos[COL_TOTAL].sum()

ventas_base = ingresos[COL_BASE].sum()

gastos_base = gastos[COL_BASE].sum()

beneficio = ventas_base - gastos_base

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
    "Beneficio antes IVA",
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
        .groupby("Cliente")[COL_TOTAL]
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

    # ==========================================
    # EXTRAER DATOS
    # ==========================================

    base_match = re.search(
        r'Base imponible\s*([\d\.,]+)',
        texto,
        re.IGNORECASE
    )

    iva_match = re.search(
        r'IVA.*?([\d\.,]+)',
        texto,
        re.IGNORECASE
    )

    total_match = re.search(
        r'TOTAL FACTURA\s*([\d\.,]+)',
        texto,
        re.IGNORECASE
    )

    base = 0
    iva = 0
    total = 0

    try:

        if base_match:
            base = float(
                base_match.group(1)
                .replace(".", "")
                .replace(",", ".")
            )

        if iva_match:
            iva = float(
                iva_match.group(1)
                .replace(".", "")
                .replace(",", ".")
            )

        if total_match:
            total = float(
                total_match.group(1)
                .replace(".", "")
                .replace(",", ".")
            )

    except:
        pass

    st.write("Base:", base)
    st.write("IVA:", iva)
    st.write("Total:", total)

    # ==========================================
    # AÑADIR FACTURA
    # ==========================================

    if st.button("➕ Añadir factura a gastos"):

        nueva_fila = pd.DataFrame({

            "Fecha": [pd.Timestamp.today()],

            "Proveedor": ["PDF AUTO"],

            "Categoría": ["Pendiente"],

            "Concepto": ["Factura PDF"],

            "Base Imponible": [base],

            "IVA %": [0.21],

            "IVA (€)": [iva],

            "Total (€)": [total],

            "Pagado": ["No"],

            "Cuenta": ["Banco"]

        })

        gastos_actualizados = pd.concat(
            [gastos, nueva_fila],
            ignore_index=True
        )

        with pd.ExcelWriter(
            excel,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace"
        ) as writer:

            ingresos.to_excel(
                writer,
                sheet_name="Ingresos",
                index=False
            )

            gastos_actualizados.to_excel(
                writer,
                sheet_name="Gastos",
                index=False
            )

        st.success(
            "✅ Factura añadida correctamente"
        )

        st.rerun()

    # ==========================================
    # TEXTO PDF
    # ==========================================

    st.subheader("📄 Texto detectado")

    st.text(texto[:5000])
