import streamlit as st
import pandas as pd
import pdfplumber
import re
import os
from openpyxl import load_workbook

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
# KPIs
# ==========================================

ventas = ingresos["Total"].sum()

gastos_total = gastos["Total"].sum()

beneficio = ventas - gastos_total

iva_rep = ingresos["IVA"].sum()

iva_sop = gastos["IVA"].sum()

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
# SUBIR FACTURA PDF
# ==========================================

st.header("📄 Subir factura PDF")

pdf_file = st.file_uploader(
    "Sube una factura PDF",
    type=["pdf"]
)

if pdf_file is not None:

    # ==========================================
    # GUARDAR PDF TEMPORAL
    # ==========================================

    with open(pdf_file.name, "wb") as f:

        f.write(
            pdf_file.getbuffer()
        )

    texto = ""

    # ==========================================
    # LEER PDF
    # ==========================================

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
    # DATOS EXTRAÍDOS
    # ==========================================

    numero_factura = (
        factura.group(1)
        if factura and factura.group(1)
        else "No detectado"
    )

    base_imponible = (
        base.group(1)
        if base
        else "0"
    )

    cuota_iva = (
        iva.group(1)
        if iva
        else "0"
    )

    total_factura = (
        total.group(1)
        if total
        else "0"
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
    # BOTÓN GUARDAR
    # ==========================================

    if st.button("➕ Añadir factura al Excel"):

        try:

            # -------------------------
            # CONVERTIR NÚMEROS
            # -------------------------

            base_float = float(
                base_imponible
                .replace(".", "")
                .replace(",", ".")
            )

            iva_float = float(
                cuota_iva
                .replace(".", "")
                .replace(",", ".")
            )

            total_float = float(
                total_factura
                .replace(".", "")
                .replace(",", ".")
            )

            # -------------------------
            # NUEVA FILA
            # -------------------------

            nueva_fila = {

                "Fecha": pd.Timestamp.today().date(),

                "Trimestre": "2T",

                "Proveedor": "PDF AUTO",

                "Categoria": "Pendiente clasificar",

                "Base": base_float,

                "IVA": iva_float,

                "Total": total_float

            }

            # -------------------------
            # AÑADIR A GASTOS
            # -------------------------

            gastos = pd.concat(
                [
                    gastos,
                    pd.DataFrame([nueva_fila])
                ],
                ignore_index=True
            )

            # -------------------------
            # GUARDAR EXCEL
            # -------------------------

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

                gastos.to_excel(
                    writer,
                    sheet_name="Gastos",
                    index=False
                )

            st.success(
                "✅ Factura añadida automáticamente al Excel"
            )

        except Exception as e:

            st.error(
                f"❌ Error guardando factura: {e}"
            )

    # ==========================================
    # TEXTO EXTRAÍDO
    # ==========================================

    with st.expander("📄 Ver texto extraído del PDF"):

        st.text(
            texto[:5000]
        )
