import streamlit as st
import pandas as pd
import pdfplumber
import re
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="IBAI VITICULTORES",
    layout="wide"
)

# ==========================================
# TÍTULO
# ==========================================

st.title("🍷 IBAI VITICULTORES — Dashboard 2026")

# ==========================================
# EXCEL
# ==========================================

excel = "Dashboard_Bodega_Completo_2026.xlsx"

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
# KPIs
# ==========================================

ventas = ingresos["Total"].sum()

gastos_total = gastos["Total"].sum()

beneficio = ventas - gastos_total

iva_rep = ingresos["IVA"].sum()

iva_sop = gastos["IVA"].sum()

# ==========================================
# MÉTRICAS PRINCIPALES
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
# VENTAS POR CLIENTE
# ==========================================

st.subheader("📈 Ventas por cliente")

clientes = (
    ingresos
    .groupby("Cliente")["Total"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(clientes)

# ==========================================
# GASTOS POR CATEGORÍA
# ==========================================

st.subheader("📦 Gastos por categoría")

categorias = (
    gastos
    .groupby("Categoria")["Total"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(categorias)

# ==========================================
# VENTAS POR TRIMESTRE
# ==========================================

st.subheader("📊 Ventas por trimestre")

ventas_trim = (
    ingresos
    .groupby("Trimestre")["Total"]
    .sum()
)

st.bar_chart(ventas_trim)

# ==========================================
# IVA TRIMESTRAL
# ==========================================

st.subheader("💰 IVA trimestral")

iva_trim = (
    ingresos
    .groupby("Trimestre")["IVA"]
    .sum()
)

st.line_chart(iva_trim)

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
# SUBIR FACTURAS PDF
# ==========================================

st.header("📄 Subir factura PDF")

pdf_file = st.file_uploader(
    "Sube una factura PDF",
    type=["pdf"]
)

if pdf_file is not None:

    # Guardar temporalmente

    with open(pdf_file.name, "wb") as f:
        f.write(pdf_file.getbuffer())

    texto = ""

    # Leer PDF

    with pdfplumber.open(pdf_file.name) as pdf:

        for pagina in pdf.pages:

            contenido = pagina.extract_text()

            if contenido:
                texto += contenido

    st.success("✅ PDF leído correctamente")

    # ==========================================
    # EXTRAER DATOS
    # ==========================================

    factura = re.search(
        r'Factura\\s*(\\d+)|Número de Factura\\s*(\\d+)',
        texto,
        re.IGNORECASE
    )

    base = re.search(
        r'Base imponible\\s*([\\d\\.,]+)',
        texto,
        re.IGNORECASE
    )

    iva = re.search(
        r'Cuota IVA\\s*([\\d\\.,]+)',
        texto,
        re.IGNORECASE
    )

    total = re.search(
        r'Importe total\\s*([\\d\\.,]+)',
        texto,
        re.IGNORECASE
    )

    # ==========================================
    # RESULTADOS
    # ==========================================

    numero_factura = (
        factura.group(1)
        if factura and factura.group(1)
        else "No detectado"
    )

    base_imponible = (
        base.group(1)
        if base
        else "No detectado"
    )

    cuota_iva = (
        iva.group(1)
        if iva
        else "No detectado"
    )

    total_factura = (
        total.group(1)
        if total
        else "No detectado"
    )

    # ==========================================
    # MOSTRAR DATOS
    # ==========================================

    st.subheader("📋 Datos detectados")

    st.write(
        "Número factura:",
        numero_factura
    )

    st.write(
        "Base imponible:",
        base_imponible
    )

    st.write(
        "IVA:",
        cuota_iva
    )

    st.write(
        "Total:",
        total_factura
    )

    # ==========================================
    # MOSTRAR TEXTO EXTRAÍDO
    # ==========================================

    with st.expander("Ver texto PDF"):

        st.text(texto[:5000])
