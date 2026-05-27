import streamlit as st
import database
import pandas as pd
import pdfplumber
import re
from io import BytesIO

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="IBAI VITICULTORES",
    layout="wide"
)

# ==========================================
# TITULO
# ==========================================

st.title("🍷 IBAI VITICULTORES — ERP Bodega")

# ==========================================
# SUBIR EXCEL
# ==========================================

st.sidebar.header("📂 Excel maestro")

excel_file = st.sidebar.file_uploader(
    "Sube tu Excel de contabilidad",
    type=["xlsx"]
)

if excel_file is None:

    st.warning(
        "⬅️ Sube primero tu Excel maestro"
    )

    st.stop()

# ==========================================
# LEER EXCEL
# ==========================================

ingresos = pd.read_excel(
    excel_file,
    sheet_name="Ingresos"
)

gastos = pd.read_excel(
    excel_file,
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
# NUMERICOS
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
# FECHAS
# ==========================================

ingresos["Fecha"] = pd.to_datetime(
    ingresos["Fecha"],
    errors="coerce"
)

gastos["Fecha"] = pd.to_datetime(
    gastos["Fecha"],
    errors="coerce"
)

# ==========================================
# CREAR TRIMESTRES
# ==========================================

ingresos["Trimestre"] = (
    ingresos["Fecha"]
    .dt.quarter
    .astype(str)
    + "T"
)

gastos["Trimestre"] = (
    gastos["Fecha"]
    .dt.quarter
    .astype(str)
    + "T"
)

# ==========================================
# DICCIONARIO PROVEEDORES
# ==========================================

proveedores = {

    "BRAIZU": {
        "categoria": "Botellas",
        "concepto": "Botellas Borgoña + palet",
        "tipo": "Producción",
        "iva": 0.21
    },

    "VINVENTIONS": {
        "categoria": "Corchos",
        "concepto": "Corchos microaglomerados",
        "tipo": "Producción",
        "iva": 0.21
    },

    "SOLGE": {
        "categoria": "Etiquetas",
        "concepto": "Etiquetas vino",
        "tipo": "Producción",
        "iva": 0.21
    },

    "CAVATAP": {
        "categoria": "Packaging",
        "concepto": "Cápsulas y packaging",
        "tipo": "Producción",
        "iva": 0.21
    },

    "ECUTRANS": {
        "categoria": "Transporte",
        "concepto": "Transporte pallet",
        "tipo": "Logística",
        "iva": 0.21
    },

    "MOVISTAR": {
        "categoria": "Telefonía",
        "concepto": "Telefonía empresa",
        "tipo": "Servicios",
        "iva": 0.21
    }

}

# ==========================================
# SUBIR FACTURA PDF
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

    tipo_detectado = "General"

    iva_detectado = 0.21

    for proveedor in proveedores:

        if proveedor in texto_upper:

            proveedor_detectado = proveedor

            categoria_detectada = proveedores[proveedor]["categoria"]

            concepto_detectado = proveedores[proveedor]["concepto"]

            tipo_detectado = proveedores[proveedor]["tipo"]

            iva_detectado = proveedores[proveedor]["iva"]

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
    # NUMERO FACTURA
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
    st.write("Tipo:", tipo_detectado)
    st.write("Factura:", numero_factura)
    st.write("Fecha:", fecha_factura)
    st.write("Base:", base)
    st.write("IVA:", iva)
    st.write("Total:", total)

    # ==========================================
    # EVITAR DUPLICADOS
    # ==========================================

    duplicado = False

    if (
        "Proveedor" in gastos.columns
        and
        "Factura" in gastos.columns
    ):

        coincidencias = gastos[
            (
                gastos["Proveedor"]
                .astype(str)
                ==
                proveedor_detectado
            )
            &
            (
                gastos["Factura"]
                .astype(str)
                ==
                numero_factura
            )
        ]

        if len(coincidencias) > 0:

            duplicado = True

    if duplicado:

        st.warning(
            "⚠️ Esta factura ya existe"
        )

    else:

        if st.button("➕ Añadir factura a gastos"):

            nueva_fila = pd.DataFrame({

                "Fecha": [fecha_factura],

                "Trimestre": [
                    f"{((fecha_factura.month - 1)//3)+1}T"
                ],

                "Proveedor": [proveedor_detectado],

                "Categoría": [categoria_detectada],

                "Concepto": [concepto_detectado],

                "Tipo": [tipo_detectado],

                "Factura": [numero_factura],

                "Base Imponible": [base],

                "IVA %": [iva_detectado],

                "IVA (€)": [iva],

                "Total (€)": [total],

                "Pagado": ["No"],

                "Cuenta": ["Banco"]

            })

            gastos = pd.concat(
                [gastos, nueva_fila],
                ignore_index=True
            )

            st.success(
                "✅ Factura añadida correctamente"
            )

# ==========================================
# KPIs GENERALES
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
# RESUMEN FINANCIERO
# ==========================================

st.header("📊 Resumen financiero")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Ventas Totales",
    f"{ventas:,.2f} €"
)

c2.metric(
    "Gastos Totales",
    f"{gastos_total:,.2f} €"
)

c3.metric(
    "Beneficio",
    f"{beneficio:,.2f} €"
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "IVA Repercutido",
    f"{iva_rep:,.2f} €"
)

c5.metric(
    "IVA Soportado",
    f"{iva_sop:,.2f} €"
)

c6.metric(
    "Resultado IVA",
    f"{resultado_iva:,.2f} €"
)

# ==========================================
# RESUMEN TRIMESTRAL
# ==========================================

st.header("📅 Resumen trimestral")

resumen_excel = pd.DataFrame({

    "Trimestre": ["1T", "2T", "3T", "4T"]

})

# ==========================================
# INGRESOS TRIMESTRALES
# ==========================================

ingresos_trim = (
    ingresos
    .groupby("Trimestre")
    .agg({
        "Base Imponible": "sum",
        "IVA (€)": "sum",
        "Total (€)": "sum"
    })
    .reset_index()
)

# ==========================================
# GASTOS TRIMESTRALES
# ==========================================

gastos_trim = (
    gastos
    .groupby("Trimestre")
    .agg({
        "Base Imponible": "sum",
        "IVA (€)": "sum",
        "Total (€)": "sum"
    })
    .reset_index()
)

# ==========================================
# UNIR INGRESOS
# ==========================================

resumen_excel = resumen_excel.merge(

    ingresos_trim[
        [
            "Trimestre",
            "Base Imponible",
            "IVA (€)",
            "Total (€)"
        ]
    ],

    on="Trimestre",

    how="left"

)

resumen_excel.columns = [

    "Trimestre",

    "Base Ingresos",

    "IVA Repercutido",

    "Ventas Totales"

]

# ==========================================
# UNIR GASTOS
# ==========================================

resumen_excel = resumen_excel.merge(

    gastos_trim[
        [
            "Trimestre",
            "Base Imponible",
            "IVA (€)",
            "Total (€)"
        ]
    ],

    on="Trimestre",

    how="left"

)

resumen_excel.columns = [

    "Trimestre",

    "Base Ingresos",

    "IVA Repercutido",

    "Ventas Totales",

    "Base Gastos",

    "IVA Soportado",

    "Gastos Totales"

]

# ==========================================
# RELLENAR VACIOS
# ==========================================

resumen_excel = resumen_excel.fillna(0)

# ==========================================
# BENEFICIO
# ==========================================

resumen_excel["Beneficio"] = (

    resumen_excel["Base Ingresos"]

    -

    resumen_excel["Base Gastos"]

)

# ==========================================
# RESULTADO IVA
# ==========================================

resumen_excel["Resultado IVA"] = (

    resumen_excel["IVA Repercutido"]

    -

    resumen_excel["IVA Soportado"]

)

# ==========================================
# MOSTRAR RESUMEN
# ==========================================

st.dataframe(
    resumen_excel,
    use_container_width=True
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
# EXPORTAR EXCEL
# ==========================================

output = BytesIO()

with pd.ExcelWriter(
    output,
    engine="openpyxl"
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

    resumen_excel.to_excel(
        writer,
        sheet_name="Resumen_Trimestral",
        index=False
    )

st.download_button(
    label="⬇️ Descargar Excel actualizado",
    data=output.getvalue(),
    file_name="Contabilidad_Bodega_2026_COMPLETA_ACTUALIZADA.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
