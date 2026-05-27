import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IBAI VITICULTORES",
    layout="wide"
)

st.title("🍷 IBAI VITICULTORES — Dashboard 2026")

excel = "Dashboard_Bodega_Completo_2026.xlsx"

# =========================
# CARGA DATOS
# =========================

ingresos = pd.read_excel(excel, sheet_name="Ingresos")
gastos = pd.read_excel(excel, sheet_name="Gastos")

# =========================
# LIMPIEZA COLUMNAS
# =========================

ingresos.columns = ingresos.columns.str.strip()
gastos.columns = gastos.columns.str.strip()

# =========================
# KPIs
# =========================

ventas = ingresos["Total"].sum()
gastos_total = gastos["Total"].sum()

beneficio = ventas - gastos_total

iva_rep = ingresos["IVA"].sum()
iva_sop = gastos["IVA"].sum()

# =========================
# CABECERA
# =========================

st.title("🍷 Dashboard Financiero — IBAI VITICULTORES")

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

# =========================
# VENTAS CLIENTES
# =========================

st.subheader("📈 Ventas por cliente")

clientes = (
    ingresos.groupby("Cliente")["Total"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(clientes)

# =========================
# GASTOS CATEGORÍA
# =========================

st.subheader("📦 Gastos por categoría")

categorias = (
    gastos.groupby("Categoria")["Total"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(categorias)

# =========================
# VENTAS TRIMESTRALES
# =========================

st.subheader("📊 Ventas por trimestre")

ventas_trim = (
    ingresos.groupby("Trimestre")["Total"]
    .sum()
)

st.bar_chart(ventas_trim)

# =========================
# IVA TRIMESTRAL
# =========================

st.subheader("💰 IVA trimestral")

iva_trim = ingresos.groupby("Trimestre")["IVA"].sum()

st.line_chart(iva_trim)

# =========================
# TABLAS
# =========================

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
