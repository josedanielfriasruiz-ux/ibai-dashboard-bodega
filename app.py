import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IBAI VITICULTORES",
    layout="wide"
)

st.title("🍷 IBAI VITICULTORES — Dashboard 2026")

excel = "Dashboard_Bodega_Definitivo_2026.xlsx"

# Cargar datos
ingresos = pd.read_excel(excel, sheet_name="Ingresos")
gastos = pd.read_excel(excel, sheet_name="Gastos")

# KPIs
ventas = ingresos["Total"].sum()
gastos_total = gastos["Total (€)"].sum()
beneficio = ventas - gastos_total

iva_rep = ingresos["IVA"].sum()
iva_sop = gastos["IVA (€)"].sum()

# Métricas
col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", f"{ventas:,.2f} €")
col2.metric("Gastos Totales", f"{gastos_total:,.2f} €")
col3.metric("Beneficio", f"{beneficio:,.2f} €")

col4, col5 = st.columns(2)

col4.metric("IVA Repercutido", f"{iva_rep:,.2f} €")
col5.metric("IVA Soportado", f"{iva_sop:,.2f} €")

# Ventas por cliente
st.subheader("Ventas por cliente")

clientes = ingresos.groupby("Cliente")["Total"].sum().sort_values(ascending=False)

st.bar_chart(clientes)

# Gastos por categoría
st.subheader("Gastos por categoría")

categorias = gastos.groupby("Categoria")["Total (€)"].sum()

st.bar_chart(categorias)

# Tabla ingresos
st.subheader("Ingresos")

st.dataframe(ingresos)

# Tabla gastos
st.subheader("Gastos")

st.dataframe(gastos)
