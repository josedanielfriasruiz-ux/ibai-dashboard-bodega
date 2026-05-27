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
# DICCIONARIO PROVEEDORES
# ==========================================

proveedores = {

    "BRAIZU": {
        "categoria": "Botellas",
        "concepto": "Botellas Borgoña + palet"
    },

    "VINVENTIONS": {
        "categoria": "Corchos",
        "concepto": "Corchos"
    },

    "ECUTRANS": {
        "categoria": "Transporte",
        "concepto": "Transporte pallet"
    },

    "SOLGE": {
        "categoria": "Etiquetas",
        "concepto": "Etiquetas vino"
    },

    "ECOVIDRIO": {
        "categoria": "Cuotas",
        "concepto": "Cuota Ecovidrio"
    }

}

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

    texto_upper = texto.upper()

    # ==========================================
    # DETECTAR PROVEEDOR
    # ==========================================

    proveedor_detectado = "Proveedor desconocido"

    categoria_detectada = "Pendiente"

    concepto_detectado = "Factura PDF"

    for proveedor in proveedores:

        if proveedor in texto_upper:

            proveedor_detectado = proveedor

            categoria_detectada = proveedores[proveedor]["categoria"]

            concepto_detectado = proveedores[proveedor]["concepto"]

    # ==========================================
    # FECHA
    # ==========================================

    fecha_match = re.search(
        r'(\d{2}-\d{2}-\d{4})',
        texto
    )

    fecha_factura = pd.Timestamp.today()

    if fecha_match:

        try:

            fecha_factura = pd.to_datetime(
                fecha_match.group(1),
                dayfirst=True
            )

        except:
            pass

    # ==========================================
    # NÚMERO FACTURA
    # ==========================================

    factura_match = re.search(
        r'Factura Núm[:\s]*([A-Z0-9\-]+)',
        texto,
        re.IGNORECASE
    )

    numero_factura = "SIN NUMERO"

    if factura_match:

        numero_factura = factura_match.group(1)

    # ==========================================
    # BASE
    # ==========================================

    base_match = re.search(
        r'Base imponible\s*([\d\.,]+)',
        texto,
        re.IGNORECASE
    )

    base = 0

    if base_match:

        try:

            base = float(
                base_match.group(1)
                .replace(".", "")
                .replace(",", ".")
            )

        except:
            pass

    # ==========================================
    # IVA
    # ==========================================

    iva_match = re.search(
        r'IVA.*?([\d\.,]+)',
        texto,
        re.IGNORECASE
    )

    iva = 0

    if iva_match:

        try:

            iva = float(
                iva_match.group(1)
                .replace(".", "")
                .replace(",", ".")
            )

        except:
            pass

    # ==========================================
    # TOTAL
    # ==========================================

    total = round(base + iva, 2)

    # ==========================================
    # MOSTRAR DATOS
    # ==========================================

    st.subheader("📋 Datos detectados")

    st.write("Proveedor:", proveedor_detectado)

    st.write("Categoría:", categoria_detectada)

    st.write("Concepto:", concepto_detectado)

    st.write("Factura:", numero_factura)

    st.write("Fecha:", fecha_factura)

    st.write("Base:", base)

    st.write("IVA:", iva)

    st.write("Total:", total)

    # ==========================================
    # EVITAR DUPLICADOS
    # ==========================================

    duplicado = False

    if "Proveedor" in gastos.columns and "Total (€)" in gastos.columns:

        coincidencias = gastos[
            (gastos["Proveedor"] == proveedor_detectado)
            &
            (gastos["Total (€)"] == total)
        ]

        if len(coincidencias) > 0:

            duplicado = True

    if duplicado:

        st.warning(
            "⚠️ Esta factura parece duplicada"
        )

    else:

        # ==========================================
        # BOTÓN AÑADIR
        # ==========================================

        if st.button("➕ Añadir factura a gastos"):

            nueva_fila = pd.DataFrame({

                "Fecha": [fecha_factura],

                "Proveedor": [proveedor_detectado],

                "Categoría": [categoria_detectada],

                "Concepto": [concepto_detectado],

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

    with st.expander("📄 Ver texto detectado"):

        st.text(texto[:5000])
